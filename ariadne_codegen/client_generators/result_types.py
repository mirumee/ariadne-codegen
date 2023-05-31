import ast
from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple, cast

from graphql import (
    DirectiveNode,
    ExecutableDefinitionNode,
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    GraphQLAbstractType,
    GraphQLEnumType,
    GraphQLField,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLSchema,
    GraphQLUnionType,
    InlineFragmentNode,
    NameNode,
    OperationDefinitionNode,
    OperationType,
    SelectionNode,
    SelectionSetNode,
    StringValueNode,
    Visitor,
    is_abstract_type,
    print_ast,
    visit,
)

from ..codegen import (
    generate_ann_assign,
    generate_class_def,
    generate_constant,
    generate_expr,
    generate_import_from,
    generate_method_call,
    generate_module,
    generate_pass,
    generate_pydantic_field,
)
from ..exceptions import NotSupported, ParsingError
from ..plugins.manager import PluginManager
from ..utils import process_name, str_to_pascal_case
from .constants import (
    ALIAS_KEYWORD,
    ANNOTATED,
    ANY,
    BASE_MODEL_CLASS_NAME,
    DISCRIMINATOR_KEYWORD,
    FIELD_CLASS,
    LIST,
    LITERAL,
    MIXIN_FROM_NAME,
    MIXIN_IMPORT_NAME,
    MIXIN_NAME,
    OPTIONAL,
    PYDANTIC_MODULE,
    TYPENAME_ALIAS,
    TYPENAME_FIELD_NAME,
    TYPING_MODULE,
    UNION,
    UPDATE_FORWARD_REFS_METHOD,
)
from .result_fields import FieldNames, is_union, parse_operation_field
from .scalars import ScalarData, generate_scalar_imports
from .types import CodegenResultFieldType


class ResultTypesGenerator:
    def __init__(
        self,
        schema: GraphQLSchema,
        operation_definition: ExecutableDefinitionNode,
        enums_module_name: str,
        fragments_module_name: Optional[str] = None,
        fragments_definitions: Optional[Dict[str, FragmentDefinitionNode]] = None,
        base_model_import: Optional[ast.ImportFrom] = None,
        convert_to_snake_case: bool = True,
        custom_scalars: Optional[Dict[str, ScalarData]] = None,
        plugin_manager: Optional[PluginManager] = None,
    ) -> None:
        self.schema = schema
        self.operation_definition = operation_definition
        if not self.operation_definition.name:
            raise NotSupported("Operations without name are not supported.")
        self._operation_name = self.operation_definition.name.value

        self.enums_module_name = enums_module_name
        self.fragments_module_name = fragments_module_name
        self.fragments_definitions = (
            fragments_definitions if fragments_definitions else {}
        )
        self.custom_scalars = custom_scalars if custom_scalars else {}
        self.convert_to_snake_case = convert_to_snake_case
        self.plugin_manager = plugin_manager

        self._imports: List[ast.ImportFrom] = [
            generate_import_from(
                [OPTIONAL, UNION, ANY, LIST, LITERAL, ANNOTATED], TYPING_MODULE
            ),
            generate_import_from([FIELD_CLASS], PYDANTIC_MODULE),
            base_model_import
            or generate_import_from([BASE_MODEL_CLASS_NAME], PYDANTIC_MODULE),
        ]
        self._public_names: List[str] = []
        self._used_enums: List[str] = []
        self._used_scalars: List[str] = []
        self._fragments_used_as_mixins: Set[str] = set()
        self._unpacked_fragments: Set[str] = set()

        if isinstance(
            self.operation_definition, FragmentDefinitionNode
        ) and self._unpack_fragment(self.operation_definition):
            self._class_defs = []
        else:
            self._class_defs = self._parse_type_definition(
                class_name=str_to_pascal_case(self._operation_name),
                type_name=self._get_operation_type_name(self.operation_definition),
                selection_set=self.operation_definition.selection_set,
            )

        self._add_enums_scalars_fragments_imports()

    def _get_operation_type_name(self, definition: ExecutableDefinitionNode) -> str:
        if isinstance(definition, FragmentDefinitionNode):
            return definition.type_condition.name.value

        if (
            isinstance(definition, OperationDefinitionNode)
            and definition.operation == OperationType.QUERY
            and self.schema.query_type
        ):
            return self.schema.query_type.name

        if (
            isinstance(definition, OperationDefinitionNode)
            and definition.operation == OperationType.MUTATION
            and self.schema.mutation_type
        ):
            return self.schema.mutation_type.name

        if (
            isinstance(definition, OperationDefinitionNode)
            and definition.operation == OperationType.SUBSCRIPTION
            and self.schema.subscription_type
        ):
            return self.schema.subscription_type.name

        raise NotSupported(f"Not supported operation type: {definition}")

    def generate(self) -> ast.Module:
        update_forward_refs_calls = [
            generate_expr(
                generate_method_call(class_def.name, UPDATE_FORWARD_REFS_METHOD)
            )
            for class_def in self._class_defs
        ]
        module_body = (
            cast(List[ast.stmt], self._imports)
            + cast(List[ast.stmt], self._class_defs)
            + cast(List[ast.stmt], update_forward_refs_calls)
        )

        module = generate_module(module_body)
        if self.plugin_manager:
            module = self.plugin_manager.generate_result_types_module(
                module, operation_definition=self.operation_definition
            )
        return module

    def get_imports(self) -> List[ast.ImportFrom]:
        return self._imports

    def get_classes(self) -> List[ast.ClassDef]:
        return self._class_defs

    def get_operation_as_str(self) -> str:
        operation_str = print_ast(
            self._get_operation_definition_without_mixin_directive()
        )
        if self._fragments_used_as_mixins or self._unpacked_fragments:
            for used_fragment in sorted(self._get_all_related_fragments()):
                operation_str += "\n\n" + print_ast(
                    self.fragments_definitions[used_fragment]
                )

        if self.plugin_manager:
            operation_str = self.plugin_manager.generate_operation_str(
                operation_str, operation_definition=self.operation_definition
            )
        return operation_str

    def get_generated_public_names(self) -> List[str]:
        return self._public_names

    def get_unpacked_fragments(self) -> Set[str]:
        return self._unpacked_fragments

    def get_fragments_used_as_mixins(self) -> Set[str]:
        return self._fragments_used_as_mixins

    def _parse_type_definition(
        self,
        class_name: str,
        type_name: str,
        selection_set: SelectionSetNode,
        add_typename: bool = False,
        extra_bases: Optional[List[str]] = None,
        typename_values: Optional[List[str]] = None,
    ) -> List[ast.ClassDef]:
        if class_name in self._public_names:
            return []
        self._public_names.append(class_name)

        resolved_selection_set, fragments = self._resolve_selection_set(
            selection_set, type_name
        )
        if add_typename:
            (
                resolved_selection_set,
                selection_set.selections,
            ) = self._add_typename_field_to_selections(
                resolved_selection_set, selection_set
            )

        if fragments:
            class_bases = [str_to_pascal_case(f) for f in sorted(fragments)]
        else:
            class_bases = [BASE_MODEL_CLASS_NAME]
        if extra_bases:
            class_bases.extend(extra_bases)
        class_def = generate_class_def(class_name, class_bases)

        extra_classes = []
        for lineno, field in enumerate(
            resolved_selection_set,
            start=1,
        ):
            field_name = self._get_field_name(field)
            name = self._process_field_name(field_name, field=field)
            field_definition = self._get_field_from_schema(type_name, field.name.value)
            annotation, field_types_names = parse_operation_field(
                field=field,
                type_=cast(CodegenResultFieldType, field_definition.type),
                directives=field.directives,
                class_name=class_name + str_to_pascal_case(name),
                typename_values=typename_values,
                custom_scalars=self.custom_scalars,
                fragments_definitions=self.fragments_definitions,
            )

            field_implementation = generate_ann_assign(
                target=name,
                annotation=annotation,
                lineno=lineno,
            )
            field_implementation = self._process_field_implementation(
                field_implementation, field_schema_name=field_name, field=field
            )

            class_def.body.append(field_implementation)

            extra_classes.extend(
                self._parse_field_selection_set_types(
                    selection_set=field.selection_set,
                    field_types_names=field_types_names,
                    extra_bases=self._parse_mixin_directives(field),
                )
            )
            self._save_used_enums(field_types_names)
            self._save_used_scalars(field_types_names)

        if not class_def.body:
            class_def.body.append(generate_pass())

        if self.plugin_manager:
            class_def = self.plugin_manager.generate_result_class(
                class_def,
                operation_definition=self.operation_definition,
                selection_set=selection_set,
            )

        return [class_def] + extra_classes

    def _resolve_selection_set(
        self, selection_set: SelectionSetNode, root_type: str = ""
    ) -> Tuple[List[FieldNode], Set[str]]:
        fields = []
        fragments = set()
        for selection in selection_set.selections:
            if isinstance(selection, FieldNode):
                fields.append(selection)
            elif isinstance(selection, FragmentSpreadNode):
                fragment_def = self.fragments_definitions[selection.name.value]
                if not self._unpack_fragment(fragment_def):
                    fragments.add(selection.name.value)
                else:
                    self._unpacked_fragments.add(selection.name.value)
                    sub_fields, sub_fragments = self._resolve_selection_set(
                        fragment_def.selection_set, root_type
                    )
                    fields.extend(sub_fields)
                    fragments = fragments.union(sub_fragments)
            elif isinstance(selection, InlineFragmentNode):
                if selection.type_condition.name.value == root_type:
                    sub_fields, sub_fragments = self._resolve_selection_set(
                        selection.selection_set, root_type
                    )
                    fields.extend(sub_fields)
                    fragments = fragments.union(sub_fragments)
        self._fragments_used_as_mixins = self._fragments_used_as_mixins.union(
            set(fragments)
        )
        return fields, fragments

    def _unpack_fragment(self, fragment_def: FragmentDefinitionNode) -> bool:
        if fragment_def.name and isinstance(
            self.schema.type_map.get(fragment_def.type_condition.name.value),
            GraphQLUnionType,
        ):
            return True
        for fragment_selection in fragment_def.selection_set.selections:
            if isinstance(fragment_selection, InlineFragmentNode):
                return True
        return False

    def _add_typename_field_to_selections(
        self, resolved_fields: List[FieldNode], selection_set: SelectionSetNode
    ) -> Tuple[List[FieldNode], Tuple[SelectionNode, ...]]:
        field_names = {f.name.value for f in resolved_fields}
        if TYPENAME_FIELD_NAME not in field_names:
            typename_field = FieldNode(name=NameNode(value=TYPENAME_FIELD_NAME))
            return [typename_field, *resolved_fields], (
                typename_field,
                *selection_set.selections,
            )
        return resolved_fields, selection_set.selections

    def _get_field_name(self, field: FieldNode) -> str:
        if field.alias:
            return field.alias.value
        return field.name.value

    def _process_field_name(self, name: str, field: FieldNode) -> str:
        if name == TYPENAME_FIELD_NAME:
            return TYPENAME_ALIAS
        return process_name(
            name,
            convert_to_snake_case=self.convert_to_snake_case,
            plugin_manager=self.plugin_manager,
            node=field,
            trim_leading_underscore=True,
        )

    def _get_field_from_schema(self, type_name: str, field_name: str) -> GraphQLField:
        try:
            return cast(GraphQLObjectType, self.schema.type_map[type_name]).fields[
                field_name
            ]
        except KeyError as exc:
            if field_name == TYPENAME_FIELD_NAME:
                return GraphQLField(
                    type_=GraphQLNonNull(type_=GraphQLScalarType(name="String"))
                )
            raise ParsingError(
                f"Field {field_name} not found in type {type_name}."
            ) from exc

    def _process_field_implementation(
        self,
        field_implementation: ast.AnnAssign,
        field_schema_name: str,
        field: FieldNode,
    ) -> ast.AnnAssign:
        keywords: Dict[str, ast.expr] = {}

        if (
            isinstance(field_implementation.target, ast.Name)
            and field_implementation.target.id != field_schema_name
        ):
            keywords[ALIAS_KEYWORD] = generate_constant(field_schema_name)

        if is_union(field_implementation.annotation):
            keywords[DISCRIMINATOR_KEYWORD] = generate_constant(TYPENAME_ALIAS)

        if keywords:
            field_implementation.value = generate_pydantic_field(keywords)

        if self.plugin_manager:
            field_implementation = self.plugin_manager.generate_result_field(
                field_implementation,
                operation_definition=self.operation_definition,
                field=field,
            )

        return field_implementation

    def _parse_mixin_directives(self, field: FieldNode) -> List[str]:
        if not field.directives:
            return []
        directives = [
            d for d in field.directives if d.name and d.name.value == MIXIN_NAME
        ]
        extra_base_classes: List[str] = []
        for directive in directives:
            arguments = self._parse_mixin_arguments(directive)
            self._imports.append(
                generate_import_from(
                    names=[arguments[MIXIN_IMPORT_NAME]],
                    from_=arguments[MIXIN_FROM_NAME],
                )
            )
            extra_base_classes.append(arguments[MIXIN_IMPORT_NAME])
        return extra_base_classes

    def _parse_mixin_arguments(self, directive: DirectiveNode):
        arguments = {}
        for arg in directive.arguments:
            if not (
                isinstance(arg.name, NameNode)
                and isinstance(arg.value, StringValueNode)
            ):
                msg = (
                    f"Arguments passed to {MIXIN_NAME} have to be strings."
                    f"Passed argument: {print_ast(arg)}"
                )
                raise ParsingError(msg)
            arguments[arg.name.value] = arg.value.value

        if MIXIN_FROM_NAME not in arguments or MIXIN_IMPORT_NAME not in arguments:
            msg = "Required arguments ({}, {}) not found."
            raise ParsingError(msg.format(MIXIN_FROM_NAME, MIXIN_IMPORT_NAME))
        return arguments

    def _parse_field_selection_set_types(
        self,
        selection_set: Optional[SelectionSetNode],
        field_types_names: List[FieldNames],
        extra_bases: Optional[List[str]] = None,
    ) -> List[ast.ClassDef]:
        if selection_set:
            generated_classes = []
            add_typename = len(field_types_names) > 1
            typename_values = self._get_typename_values(field_types_names)
            for field_type_names in field_types_names:
                generated_classes.extend(
                    self._parse_type_definition(
                        class_name=field_type_names.class_name,
                        type_name=field_type_names.type_name,
                        selection_set=selection_set,
                        add_typename=add_typename,
                        extra_bases=extra_bases,
                        typename_values=typename_values[field_type_names.type_name],
                    )
                )
            return generated_classes
        return []

    def _get_typename_values(
        self, field_types_names: List[FieldNames]
    ) -> Dict[str, List[str]]:
        types_names = [n.type_name for n in field_types_names]
        result = {name: [name] for name in types_names}

        schema_types = [self.schema.type_map[n] for n in types_names]
        abstract_type = next(filter(is_abstract_type, schema_types), None)
        abstract_type = cast(GraphQLAbstractType, abstract_type)
        if not abstract_type:
            return result

        possible_types = self.schema.get_possible_types(abstract_type)
        possible_types_names = [t.name for t in possible_types]
        types_without_class = list(set(possible_types_names) - set(types_names))

        result[abstract_type.name].extend(types_without_class)
        return result

    def _save_used_enums(self, field_types_names: List[FieldNames]):
        for field_type_name in field_types_names:
            if isinstance(
                self.schema.type_map.get(field_type_name.type_name), GraphQLEnumType
            ):
                self._used_enums.append(field_type_name.type_name)

    def _save_used_scalars(self, field_types_names: List[FieldNames]):
        for field_type_name in field_types_names:
            if field_type_name.type_name in self.custom_scalars:
                self._used_scalars.append(field_type_name.type_name)

    def _add_enums_scalars_fragments_imports(self):
        if self._used_enums:
            self._imports.append(
                generate_import_from(self._used_enums, self.enums_module_name, 1)
            )
        if self._used_scalars:
            for scalar_name in self._used_scalars:
                scalar_data = self.custom_scalars[scalar_name]
                self._imports.extend(generate_scalar_imports(scalar_data))

        if (
            isinstance(self.operation_definition, OperationDefinitionNode)
            and self._fragments_used_as_mixins
            and self.fragments_module_name
        ):
            self._imports.append(
                generate_import_from(
                    [str_to_pascal_case(f) for f in self._fragments_used_as_mixins],
                    self.fragments_module_name,
                    1,
                )
            )

    def _get_all_related_fragments(self) -> Set[str]:
        fragments_names: Set[str] = self._fragments_used_as_mixins.copy()
        for fragment_name in self._fragments_used_as_mixins:
            fragment_def = self.fragments_definitions[fragment_name]
            fragments_names = fragments_names.union(
                self._get_fragments_names(fragment_def.selection_set)
            )
        return fragments_names.union(self._unpacked_fragments)

    def _get_fragments_names(self, selection_set: SelectionSetNode) -> Set[str]:
        names: Set[str] = set()
        for node in selection_set.selections:
            if isinstance(node, FragmentSpreadNode):
                name = node.name.value
                names.add(name)
                names = names.union(
                    self._get_fragments_names(
                        self.fragments_definitions[name].selection_set
                    )
                )
            elif isinstance(node, FieldNode) and node.selection_set:
                names = names.union(self._get_fragments_names(node.selection_set))
        return names

    def _get_operation_definition_without_mixin_directive(self):
        class RemoveMixinVisitor(Visitor):
            @staticmethod
            def enter_field(node: FieldNode, *_args: Any) -> FieldNode:
                node.directives = tuple(
                    d for d in node.directives or [] if d.name.value != MIXIN_NAME
                )
                return node

        operation_def = deepcopy(self.operation_definition)
        visit(operation_def, RemoveMixinVisitor())
        return operation_def
