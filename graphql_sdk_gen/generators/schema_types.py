import ast
from collections import defaultdict
from typing import Optional, Union

from graphql import (
    BooleanValueNode,
    EnumValueNode,
    FloatValueNode,
    GraphQLEnumType,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLNamedType,
    GraphQLObjectType,
    GraphQLSchema,
    IntValueNode,
    ListValueNode,
    NullValueNode,
    ObjectValueNode,
    StringValueNode,
)

from ..exceptions import NotSupported
from .codegen import (
    generate_ann_assign,
    generate_arguments,
    generate_assign,
    generate_call,
    generate_class_def,
    generate_constant,
    generate_dict,
    generate_expr,
    generate_field_with_alias,
    generate_import_from,
    generate_keyword,
    generate_lambda,
    generate_list,
    generate_method_call,
    generate_name,
    parse_field_type,
)
from .constants import (
    ANY,
    BASE_MODEL_CLASS_NAME,
    FIELD_CLASS,
    OPTIONAL,
    PYDANTIC_MODULE,
    TYPING_MODULE,
    UNION,
    UPDATE_FORWARD_REFS_METHOD,
    ClassType,
)
from .utils import str_to_snake_case


class SchemaTypesGenerator:
    def __init__(
        self,
        schema: GraphQLSchema,
        convert_to_snake_case: bool = True,
        base_model_import: Optional[ast.ImportFrom] = None,
    ) -> None:
        self.schema = schema
        self.types_to_parse = self._filter_schema_types()

        self.fields: dict[str, dict[str, ast.AnnAssign]] = {}
        self.class_types: dict[str, ClassType] = {}

        self.enums: list[str] = []
        self.input_types: list[str] = []
        self.schema_types: list[str] = []

        self.enums_classes: list[ast.ClassDef] = []
        self.input_types_classes: list[ast.ClassDef] = []
        self.schema_types_classes: list[ast.ClassDef] = []

        self.input_types_dependencies: dict[str, list[str]] = defaultdict(list)
        self.convert_to_snake_case = convert_to_snake_case
        self.base_model_import = base_model_import or generate_import_from(
            [BASE_MODEL_CLASS_NAME], PYDANTIC_MODULE
        )

        for definition in self.types_to_parse:
            self._parse_type_definition(definition)

    def _filter_schema_types(self) -> list[GraphQLNamedType]:
        return [
            definition
            for name, definition in self.schema.type_map.items()
            if isinstance(
                definition,
                (
                    GraphQLEnumType,
                    GraphQLObjectType,
                    GraphQLInputObjectType,
                    GraphQLInterfaceType,
                ),
            )
            and not name.startswith("__")
            and definition not in {self.schema.query_type, self.schema.mutation_type}
        ]

    def _is_name_already_parsed(self, name: str) -> bool:
        return (
            name in self.enums or name in self.input_types or name in self.schema_types
        )

    def _parse_type_definition(self, definition: GraphQLNamedType):
        if self._is_name_already_parsed(definition.name):
            return

        if isinstance(definition, GraphQLEnumType):
            self.enums.append(definition.name)
            class_def = self._parse_enum_definition(definition)
            self.class_types[class_def.name] = ClassType.ENUM
            self.enums_classes.append(class_def)

        elif isinstance(definition, GraphQLInputObjectType):
            self.input_types.append(definition.name)
            class_def = self._parse_object_input_or_interface_definition(definition)
            self.class_types[class_def.name] = ClassType.INPUT
            self.input_types_classes.append(class_def)

        elif isinstance(definition, GraphQLInterfaceType):
            self.schema_types.append(definition.name)
            class_def = self._parse_object_input_or_interface_definition(definition)
            self.class_types[class_def.name] = ClassType.INTERFACE
            self.schema_types_classes.append(class_def)

        elif isinstance(definition, GraphQLObjectType):
            self.schema_types.append(definition.name)
            class_def = self._parse_object_input_or_interface_definition(definition)
            if definition.interfaces:
                interfaces_names = self._parse_interfaces(definition)
                class_def.bases = [generate_name(name) for name in interfaces_names]
            self.class_types[class_def.name] = ClassType.OBJECT
            self.schema_types_classes.append(class_def)
        else:
            raise NotSupported("Not supported type.")

    def _parse_interfaces(self, definition: GraphQLObjectType) -> list[str]:
        result = []
        for interface in definition.interfaces:
            self._parse_type_definition(interface)
            result.append(interface.name)
        return result

    def _parse_enum_definition(self, definition: GraphQLEnumType) -> ast.ClassDef:
        class_def = generate_class_def(name=definition.name, base_names=["str", "Enum"])

        self.fields[definition.name] = {}
        for lineno, (val_name, val_def) in enumerate(
            definition.values.items(), start=1
        ):
            field_def = generate_assign(
                [val_name], generate_constant(val_def.value), lineno
            )
            class_def.body.append(field_def)
        return class_def

    def _parse_object_input_or_interface_definition(
        self,
        definition: Union[
            GraphQLObjectType, GraphQLInputObjectType, GraphQLInterfaceType
        ],
    ) -> ast.ClassDef:
        class_def = generate_class_def(
            name=definition.name, base_names=[BASE_MODEL_CLASS_NAME]
        )

        self.fields[definition.name] = {}
        for lineno, (org_name, field) in enumerate(definition.fields.items(), start=1):
            name = self._process_field_name(org_name)
            field_annotation = parse_field_type(field.type)
            field_def = generate_ann_assign(
                target=name,
                annotation=field_annotation,
                value=self._parse_field_default_value(
                    field, field_annotation, class_def.name
                ),
                lineno=lineno,
            )
            if name != org_name:
                field_def.value = self._generate_alias(field_def, org_name)
            class_def.body.append(field_def)
            self.fields[definition.name][org_name] = field_def
        return class_def

    def _process_field_name(self, name: str) -> str:
        if self.convert_to_snake_case:
            return str_to_snake_case(name)
        return name

    def _generate_alias(self, field_def: ast.AnnAssign, alias: str) -> ast.Call:
        field_with_alias = generate_field_with_alias(alias)
        if field_def.value:
            if (
                isinstance(field_def.value, ast.Call)
                and isinstance(field_def.value.func, ast.Name)
                and field_def.value.func.id == FIELD_CLASS
            ):
                field_with_alias.keywords.extend(field_def.value.keywords)
            else:
                field_with_alias.keywords.append(
                    generate_keyword(
                        arg="default",
                        value=field_def.value,
                    )
                )
        return field_with_alias

    def _parse_field_default_value(
        self, field, field_annotation, class_name
    ) -> Optional[ast.expr]:
        if isinstance(field, GraphQLInputField):
            if field.ast_node and field.ast_node.default_value:
                root_field_type = self._get_type_from_input_field_annotation(
                    field_annotation
                )
                return self._parse_const_value_node(
                    field.ast_node.default_value, root_field_type, class_name
                )
        return None

    # pylint: disable=too-many-return-statements
    def _parse_const_value_node(
        self, node, root_field_type, class_name, nested_list=False, nested_object=False
    ) -> Optional[ast.expr]:
        if isinstance(node, IntValueNode):
            return generate_constant(int(node.value))

        if isinstance(node, FloatValueNode):
            return generate_constant(float(node.value))

        if isinstance(node, StringValueNode):
            return generate_constant(node.value)

        if isinstance(node, BooleanValueNode):
            return generate_constant(bool(node.value))

        if isinstance(node, NullValueNode):
            return generate_constant(None)

        if isinstance(node, EnumValueNode):
            return generate_name(f"{root_field_type}.{node.value}")

        if isinstance(node, ListValueNode):
            list_ = generate_list(
                [
                    self._parse_const_value_node(
                        v,
                        root_field_type,
                        class_name,
                        nested_object=nested_object,
                        nested_list=True,
                    )
                    for v in node.values
                ]
            )
            if not nested_list:
                return self._generate_list_as_default_value(list_)
            return list_

        if isinstance(node, ObjectValueNode):
            dict_ = generate_dict(
                keys=[generate_constant(f.name.value) for f in node.fields],
                values=[
                    self._parse_const_value_node(
                        f.value,
                        root_field_type,
                        class_name,
                        nested_object=True,
                        nested_list=True,
                    )
                    for f in node.fields
                ],
            )
            if not nested_object:
                self.input_types_dependencies[class_name].append(root_field_type)
                return generate_method_call(root_field_type, "parse_obj", [dict_])
            return dict_

        return None

    def _get_type_from_input_field_annotation(self, annotation):
        if isinstance(annotation, ast.Name):
            return annotation.id.replace('"', "")

        return self._get_type_from_input_field_annotation(annotation.slice)

    def _generate_list_as_default_value(self, list_: ast.List):
        return generate_call(
            func=generate_name(FIELD_CLASS),
            keywords=[
                generate_keyword(
                    arg="default_factory",
                    value=generate_lambda(args=generate_arguments(), body=list_),
                )
            ],
        )

    def _generate_module(
        self,
        imports: list[ast.ImportFrom],
        class_defs: list[ast.ClassDef],
        include_update_forward_refs_calls: bool = True,
    ) -> ast.Module:
        module = ast.Module(
            body=imports,
            type_ignores=[],
        )
        for lineno, class_def in enumerate(class_defs, start=len(module.body) + 1):
            class_def.lineno = lineno
            module.body.append(class_def)
        if include_update_forward_refs_calls:
            module.body.extend(
                [
                    generate_expr(
                        generate_method_call(c.name, UPDATE_FORWARD_REFS_METHOD)
                    )
                    for c in class_defs
                ]
            )
        return module

    def _get_sorted_input_class_defs(self):
        input_class_defs_dict_ = {c.name: c for c in self.input_types_classes}

        processed_names = []
        for class_ in self.input_types_classes:
            if class_.name not in processed_names:
                processed_names.extend(self._get_dependant_names(class_.name))
                processed_names.append(class_.name)

        names_without_duplicates = self._get_list_without_duplicates(processed_names)
        return [input_class_defs_dict_[n] for n in names_without_duplicates]

    def _get_dependant_names(self, name):
        result = []
        for dependency_name in self.input_types_dependencies[name]:
            result.extend(self._get_dependant_names(dependency_name))
            result.append(dependency_name)
        return result

    def _get_list_without_duplicates(self, list_):
        seen = set()
        return [x for x in list_ if not (x in seen or seen.add(x))]

    def generate(self) -> tuple[ast.Module, ast.Module, ast.Module]:
        input_types_imports = [
            generate_import_from([OPTIONAL, ANY, UNION], TYPING_MODULE),
            generate_import_from([FIELD_CLASS], PYDANTIC_MODULE),
            self.base_model_import,
        ]
        if self.enums:
            input_types_imports.append(generate_import_from(self.enums, "enums", 1))
        schema_types_imports = [
            generate_import_from([OPTIONAL, ANY, UNION], TYPING_MODULE),
            generate_import_from([FIELD_CLASS], PYDANTIC_MODULE),
            self.base_model_import,
        ]
        if self.enums:
            schema_types_imports.append(generate_import_from(self.enums, "enums", 1))
        return (
            self._generate_module(
                [generate_import_from(["Enum"], "enum")], self.enums_classes, False
            ),
            self._generate_module(
                input_types_imports,
                self._get_sorted_input_class_defs(),
                True,
            ),
            self._generate_module(
                schema_types_imports,
                self.schema_types_classes,
                True,
            ),
        )
