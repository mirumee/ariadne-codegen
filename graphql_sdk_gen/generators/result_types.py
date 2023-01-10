import ast
from typing import Optional, cast

from graphql import (
    DirectiveNode,
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    GraphQLEnumType,
    GraphQLField,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLSchema,
    InlineFragmentNode,
    NameNode,
    OperationDefinitionNode,
    SelectionNode,
    SelectionSetNode,
    StringValueNode,
    print_ast,
)

from ..exceptions import NotSupported, ParsingError
from .codegen import (
    generate_ann_assign,
    generate_class_def,
    generate_expr,
    generate_field_with_alias,
    generate_import_from,
    generate_method_call,
    generate_module,
)
from .constants import (
    ANY,
    BASE_MODEL_CLASS_NAME,
    FIELD_CLASS,
    MIXIN_FROM_NAME,
    MIXIN_IMPORT_NAME,
    MIXIN_NAME,
    OPTIONAL,
    PYDANTIC_MODULE,
    TYPENAME_FIELD_NAME,
    TYPING_MODULE,
    UNION,
    UPDATE_FORWARD_REFS_METHOD,
)
from .result_fields import FieldNames, parse_operation_field
from .types import CodegenResultFieldType
from .utils import str_to_pascal_case, str_to_snake_case


class ResultTypesGenerator:
    def __init__(
        self,
        schema: GraphQLSchema,
        operation_definition: OperationDefinitionNode,
        enums_module_name: str,
        fragments_definitions: Optional[dict[str, FragmentDefinitionNode]] = None,
        base_model_import: Optional[ast.ImportFrom] = None,
        convert_to_snake_case: bool = True,
    ) -> None:
        self.schema = schema
        self.operation_definition = operation_definition
        if not self.operation_definition.name:
            raise NotSupported("Operations without name are not supported.")

        self.enums_module_name = enums_module_name
        self.fragments_definitions = (
            fragments_definitions if fragments_definitions else {}
        )
        self.convert_to_snake_case = convert_to_snake_case

        self._imports: list[ast.ImportFrom] = [
            generate_import_from([OPTIONAL, UNION, ANY], TYPING_MODULE),
            generate_import_from([FIELD_CLASS], PYDANTIC_MODULE),
            base_model_import
            or generate_import_from([BASE_MODEL_CLASS_NAME], PYDANTIC_MODULE),
        ]
        self._public_names: list[str] = []
        self._class_defs: list[ast.ClassDef] = []
        self._used_enums: list[str] = []
        self._used_fragments_names: set[str] = set()

        self._class_defs = self._parse_type_definition(
            class_name=str_to_pascal_case(self.operation_definition.name.value),
            type_name=self.operation_definition.operation.value.capitalize(),
            selection_set=self.operation_definition.selection_set,
        )

    def generate(self) -> ast.Module:
        if self._used_enums:
            self._imports.append(
                generate_import_from(self._used_enums, self.enums_module_name, 1)
            )
        update_forward_refs_calls = [
            generate_expr(
                generate_method_call(class_def.name, UPDATE_FORWARD_REFS_METHOD)
            )
            for class_def in self._class_defs
        ]
        module_body = (
            cast(list[ast.stmt], self._imports)
            + cast(list[ast.stmt], self._class_defs)
            + cast(list[ast.stmt], update_forward_refs_calls)
        )

        return generate_module(module_body)

    def get_operation_as_str(self) -> str:
        operation_str = print_ast(self.operation_definition)
        if self._used_fragments_names:
            for used_fragment in sorted(self._used_fragments_names):
                operation_str += "\n\n" + print_ast(
                    self.fragments_definitions[used_fragment]
                )

        return operation_str

    def get_generated_public_names(self) -> list[str]:
        return self._public_names

    def _parse_type_definition(
        self,
        class_name: str,
        type_name: str,
        selection_set: SelectionSetNode,
        add_typename: bool = False,
        extra_bases: Optional[list[str]] = None,
    ) -> list[ast.ClassDef]:
        class_bases = [BASE_MODEL_CLASS_NAME]
        if extra_bases:
            class_bases.extend(extra_bases)
        class_def = generate_class_def(class_name, class_bases)

        if class_def.name in self._public_names:
            return []
        self._public_names.append(class_def.name)

        extra_classes = []
        resolved_selection_set = self._resolve_selection_set(selection_set, type_name)
        if add_typename:
            (
                resolved_selection_set,
                selection_set.selections,
            ) = self._add_typename_field_to_selections(
                resolved_selection_set, selection_set
            )
        for lineno, field in enumerate(
            resolved_selection_set,
            start=1,
        ):
            field_name = self._get_field_name(field)
            name = self._process_field_name(field_name)
            field_definition = self._get_field_from_schema(type_name, field.name.value)
            annotation, field_types_names = parse_operation_field(
                type_=cast(CodegenResultFieldType, field_definition.type),
                directives=field.directives,
                class_name=class_name + str_to_pascal_case(name),
            )

            field_implementation = generate_ann_assign(
                target=name,
                annotation=annotation,
                lineno=lineno,
            )
            if name != field_name:
                field_implementation.value = generate_field_with_alias(field_name)

            class_def.body.append(field_implementation)

            extra_classes.extend(
                self._parse_field_selection_set_types(
                    selection_set=field.selection_set,
                    field_types_names=field_types_names,
                    extra_bases=self._parse_mixin_directives(field),
                )
            )
            self._save_used_enums(field_types_names)
        return [class_def] + extra_classes

    def _resolve_selection_set(
        self, selection_set: SelectionSetNode, root_type: str = ""
    ) -> list[FieldNode]:
        fields = []
        for selection in selection_set.selections:
            if isinstance(selection, FieldNode):
                fields.append(selection)
            elif isinstance(selection, FragmentSpreadNode):
                self._used_fragments_names.add(selection.name.value)
                fields.extend(
                    self._resolve_selection_set(
                        self.fragments_definitions[selection.name.value].selection_set,
                        root_type,
                    )
                )
            elif isinstance(selection, InlineFragmentNode):
                if selection.type_condition.name.value == root_type:
                    fields.extend(
                        self._resolve_selection_set(selection.selection_set, root_type)
                    )
        return fields

    def _add_typename_field_to_selections(
        self, resolved_fields: list[FieldNode], selection_set: SelectionSetNode
    ) -> tuple[list[FieldNode], tuple[SelectionNode, ...]]:
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

    def _process_field_name(self, name: str) -> str:
        if self.convert_to_snake_case:
            if name == TYPENAME_FIELD_NAME:
                return "__typename__"
            return str_to_snake_case(name)
        return name

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

    def _parse_mixin_directives(self, field: FieldNode) -> list[str]:
        if not field.directives:
            return []
        directives = [
            d for d in field.directives if d.name and d.name.value == MIXIN_NAME
        ]
        extra_base_classes: list[str] = []
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
        field_types_names: list[FieldNames],
        extra_bases: Optional[list[str]] = None,
    ) -> list[ast.ClassDef]:
        if selection_set:
            generated_classes = []
            add_typename = len(field_types_names) > 1
            for field_type_names in field_types_names:
                generated_classes.extend(
                    self._parse_type_definition(
                        class_name=field_type_names.class_name,
                        type_name=field_type_names.type_name,
                        selection_set=selection_set,
                        add_typename=add_typename,
                        extra_bases=extra_bases,
                    )
                )
            return generated_classes
        return []

    def _save_used_enums(self, field_types_names: list[FieldNames]):
        for field_type_names in field_types_names:
            if isinstance(
                self.schema.type_map.get(field_type_names.type_name), GraphQLEnumType
            ):
                self._used_enums.append(field_type_names.type_name)
