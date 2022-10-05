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
    parse_field_type,
)
from .constants import OPTIONAL, ClassType


class SchemaTypesGenerator:
    def __init__(self, schema: GraphQLSchema) -> None:
        self.schema = schema
        self.types_to_parse = self._filter_schema_types()

        self.public_names: list[str] = []
        self.class_defs: list[ast.ClassDef] = []
        self.fields: dict[str, dict[str, Union[ast.AnnAssign, ast.Assign]]] = {}
        self.class_types: dict[str, ClassType] = {}

        self.imports = [
            generate_import_from(["Enum"], "enum"),
            generate_import_from([OPTIONAL, "Any", "Union"], "typing"),
            generate_import_from(["BaseModel"], "pydantic"),
        ]

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

    def _parse_type_definition(self, definition: GraphQLNamedType):
        if definition.name in self.public_names:
            return
        self.public_names.append(definition.name)

        if isinstance(definition, GraphQLEnumType):
            class_def = self._parse_enum_definition(definition)
            self.class_types[class_def.name] = ClassType.ENUM
        elif isinstance(definition, GraphQLInputObjectType):
            class_def = self._parse_object_input_or_interface_definition(definition)
            self.class_types[class_def.name] = ClassType.INPUT
        elif isinstance(definition, GraphQLInterfaceType):
            class_def = self._parse_object_input_or_interface_definition(definition)
            self.class_types[class_def.name] = ClassType.INTERFACE
        elif isinstance(definition, GraphQLObjectType):
            class_def = self._parse_object_input_or_interface_definition(definition)
            if definition.interfaces:
                interfaces_names = self._parse_interfaces(definition)
                class_def.bases.extend(interfaces_names)
            self.class_types[class_def.name] = ClassType.OBJECT
        else:
            raise NotSupported("Not supported type.")

        self.class_defs.append(class_def)

    def _parse_interfaces(self, definition: GraphQLObjectType) -> list[ast.Name]:
        result = []
        for interface in definition.interfaces:
            if interface.name not in self.public_names:
                self._parse_type_definition(interface)
            result.append(ast.Name(id=interface.name))
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
            field_def = generate_ann_assign(name, parse_field_type(field.type), lineno)
            class_def.body.append(field_def)
            self.fields[definition.name][name] = field_def
        return class_def

    def generate(self) -> ast.Module:
        module = ast.Module(body=self.imports, type_ignores=[])
        for lineno, class_def in enumerate(
            self.class_defs, start=len(self.imports) + 1
        ):
            class_def.lineno = lineno
            module.body.append(class_def)
        return module
