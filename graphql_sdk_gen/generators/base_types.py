import ast
from typing import Union

from graphql import (
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLObjectType,
    GraphQLSchema,
)
from enum import Enum

from .utils import generate_import_from, parse_field_type


class FieldType(str, Enum):
    ENUM = "ENUM"
    INPUT = "INPUT"
    OBJECT = "OBJECT"


class BaseTypesGenerator:
    def __init__(self, schema: GraphQLSchema) -> None:
        self.schema = schema
        self.types_from_schema = {
            name: definition
            for name, definition in schema.type_map.items()
            if isinstance(
                definition, (GraphQLEnumType, GraphQLObjectType, GraphQLInputObjectType)
            )
            and not name.startswith("__")
            and definition not in {schema.query_type, schema.mutation_type}
        }
        self.types_definitions: dict = {}
        self.fields_definitions: dict[
            str, dict[str, Union[ast.AnnAssign, ast.Assign]]
        ] = {}
        self.fields_types: dict[str, FieldType] = {}
        for name, definition in self.types_from_schema.items():
            self.types_definitions[name] = self._parse_type_definition(definition)

    def _parse_type_definition(self, definition) -> ast.ClassDef:
        if isinstance(definition, GraphQLEnumType):
            class_def = self._parse_enum_definition(definition)
            self.fields_types[class_def.name] = FieldType.ENUM
        elif isinstance(definition, GraphQLInputObjectType):
            class_def = self._parse_object_or_input_definition(definition)
            self.fields_types[class_def.name] = FieldType.INPUT
        elif isinstance(definition, GraphQLObjectType):
            class_def = self._parse_object_or_input_definition(definition)
            interfaces = self._parse_interfaces(definition)
            if interfaces:
                class_def.bases = interfaces
            self.fields_types[class_def.name] = FieldType.OBJECT
        else:
            raise Exception

        return class_def

    def _parse_interfaces(self, definition) -> list[ast.Name]:
        return [ast.Name(id=interface.name) for interface in definition.interfaces]

    def _parse_enum_definition(self, definition: GraphQLEnumType) -> ast.ClassDef:
        class_def = ast.ClassDef(
            name=definition.name,
            bases=[ast.Name("str"), ast.Name("Enum")],
            keywords=[],
            body=[],
            decorator_list=[],
        )
        self.fields_definitions[definition.name] = {}
        for lineno, (val_name, val_def) in enumerate(
            definition.values.items(), start=1
        ):
            field_def = ast.Assign(
                targets=[ast.Name(id=val_name)],
                value=ast.Constant(value=val_def.value),
                lineno=lineno,
            )
            class_def.body.append(field_def)
            self.fields_definitions[definition.name][val_name] = field_def
        return class_def

    def _parse_object_or_input_definition(
        self, definition: Union[GraphQLObjectType, GraphQLInputObjectType]
    ) -> ast.ClassDef:
        class_def = ast.ClassDef(
            name=definition.name,
            bases=[ast.Name("BaseModel")],
            keywords=[],
            body=[],
            decorator_list=[],
        )
        self.fields_definitions[definition.name] = {}
        for lineno, (name, field) in enumerate(definition.fields.items(), start=1):
            field_def = ast.AnnAssign(
                target=ast.Name(id=name),
                annotation=parse_field_type(field.type),
                simple=1,
                lineno=lineno,
            )
            class_def.body.append(field_def)
            self.fields_definitions[definition.name][name] = field_def
        return class_def

    def generate(self) -> ast.Module:
        imports = [
            generate_import_from(["Enum"], "enum"),
            generate_import_from(["Optional", "Any", "Union"], "typing"),
            generate_import_from(["BaseModel"], "pydantic"),
        ]
        module = ast.Module(body=imports, type_ignores=[])
        for lineno, (_, class_def) in enumerate(
            self.types_definitions.items(), start=len(imports) + 1
        ):  # TODO: sort definitions to avoid access before declaration
            if class_def and class_def.body:
                class_def.lineno = lineno
                module.body.append(class_def)
        return module
