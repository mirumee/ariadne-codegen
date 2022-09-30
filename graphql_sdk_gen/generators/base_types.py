import ast
from typing import Union

from graphql import (
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLSchema,
    GraphQLUnionType,
)

from .constants import LIST, OPTIONAL, SIMPLE_TYPE_MAP
from .utils import generate_import_from


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
        for name, definition in self.types_from_schema.items():
            self.types_definitions[name] = self._parse_type_definition(definition)

    def _parse_type_definition(self, definition) -> ast.ClassDef:
        if isinstance(definition, GraphQLEnumType):
            return self._parse_enum_definition(definition)
        if isinstance(definition, (GraphQLObjectType, GraphQLInputObjectType)):
            return self._parse_object_or_input_definition(definition)
        else:
            raise Exception

    def _parse_enum_definition(self, definition: GraphQLEnumType) -> ast.ClassDef:
        class_def = ast.ClassDef(
            name=definition.name,
            bases=[ast.Name("str"), ast.Name("Enum")],
            keywords=[],
            body=[],
            decorator_list=[],
        )
        for lineno, (val_name, val_def) in enumerate(
            definition.values.items(), start=1
        ):
            class_def.body.append(
                ast.Assign(
                    targets=[ast.Name(id=val_name)],
                    value=ast.Constant(value=val_def.value),
                    lineno=lineno,
                )
            )
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
        for lineno, (name, field) in enumerate(definition.fields.items(), start=1):
            class_def.body.append(
                ast.AnnAssign(
                    target=ast.Name(id=name),
                    annotation=self._parse_field_type(field.type),
                    simple=1,
                    lineno=lineno,
                )
            )
        return class_def

    def _parse_field_type(
        self, type_, nullable: bool = True
    ) -> Union[ast.Name, ast.Subscript]:
        if isinstance(type_, GraphQLScalarType):
            return self._gen_name(SIMPLE_TYPE_MAP.get(type_.name, "Any"), nullable)
        elif isinstance(
            type_,
            (
                GraphQLObjectType,
                GraphQLInputObjectType,
                GraphQLEnumType,
                GraphQLInterfaceType,
            ),
        ):
            return self._gen_name(type_.name, nullable)
        elif isinstance(type_, GraphQLUnionType):
            subtypes = [self._parse_field_type(subtype) for subtype in type_.types]
            return self._gen_union(subtypes, nullable)
        elif isinstance(type_, GraphQLList):
            return self._gen_list(
                self._parse_field_type(type_.of_type, nullable), nullable
            )
        elif isinstance(type_, GraphQLNonNull):
            return self._parse_field_type(type_.of_type, False)
        else:
            raise Exception

    def _nullable(self, slice_: Union[ast.Name, ast.Subscript]) -> ast.Subscript:
        return ast.Subscript(value=ast.Name(id=OPTIONAL), slice=slice_)

    def _gen_name(self, name, nullable: bool = True) -> Union[ast.Name, ast.Subscript]:
        result = ast.Name(id=name)
        return result if not nullable else self._nullable(result)

    def _gen_list(self, slice_: Union[ast.Name, ast.Subscript], nullable: bool = True):
        result = ast.Subscript(value=ast.Name(id=LIST), slice=slice_)
        return result if not nullable else self._nullable(result)

    def _gen_union(
        self, types: list[Union[ast.Name, ast.Subscript]], nullable: bool = True
    ) -> ast.Subscript:
        result = ast.Subscript(value=ast.Name(id="Union"), slice=ast.Tuple(elts=types))
        return result if not nullable else self._nullable(result)

    def generate(self) -> tuple[ast.Module, str]:
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
        return module, "types.py"
