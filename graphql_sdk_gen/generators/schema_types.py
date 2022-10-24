import ast
from typing import Union

from graphql import (
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLNamedType,
    GraphQLObjectType,
    GraphQLSchema,
)

from ..exceptions import NotSupported
from .codegen import (
    generate_ann_assign,
    generate_assign,
    generate_class_def,
    generate_constant,
    generate_import_from,
    generate_method_call,
    generate_name,
    parse_field_type,
)
from .constants import ANY, OPTIONAL, UNION, ClassType


class SchemaTypesGenerator:
    def __init__(self, schema: GraphQLSchema) -> None:
        self.schema = schema
        self.types_to_parse = self._filter_schema_types()

        self.fields: dict[str, dict[str, Union[ast.AnnAssign, ast.Assign]]] = {}
        self.class_types: dict[str, ClassType] = {}

        self.enums: list[str] = []
        self.input_types: list[str] = []
        self.schema_types: list[str] = []

        self.enums_classes: list[ast.ClassDef] = []
        self.input_types_classes: list[ast.ClassDef] = []
        self.schema_types_classes: list[ast.ClassDef] = []

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
            self.fields[definition.name][val_name] = field_def
        return class_def

    def _parse_object_input_or_interface_definition(
        self,
        definition: Union[
            GraphQLObjectType, GraphQLInputObjectType, GraphQLInterfaceType
        ],
    ) -> ast.ClassDef:
        class_def = generate_class_def(name=definition.name, base_names=["BaseModel"])

        self.fields[definition.name] = {}
        for lineno, (name, field) in enumerate(definition.fields.items(), start=1):
            field_def = generate_ann_assign(
                name, parse_field_type(field.type), lineno=lineno
            )
            class_def.body.append(field_def)
            self.fields[definition.name][name] = field_def
        return class_def

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
                    generate_method_call(c.name, "update_forward_refs")
                    for c in class_defs
                ]
            )
        return module

    def generate(self) -> tuple[ast.Module, ast.Module, ast.Module]:
        return (
            self._generate_module(
                [generate_import_from(["Enum"], "enum")], self.enums_classes, False
            ),
            self._generate_module(
                [
                    generate_import_from([OPTIONAL, ANY, UNION], "typing"),
                    generate_import_from(["BaseModel"], "pydantic"),
                    generate_import_from(self.enums, "enums", 1),
                ],
                self.input_types_classes,
                True,
            ),
            self._generate_module(
                [
                    generate_import_from([OPTIONAL, ANY, UNION], "typing"),
                    generate_import_from(["BaseModel"], "pydantic"),
                    generate_import_from(self.enums, "enums", 1),
                ],
                self.schema_types_classes,
                True,
            ),
        )
