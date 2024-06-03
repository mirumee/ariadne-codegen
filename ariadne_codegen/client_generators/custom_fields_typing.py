import ast
from typing import List, cast

from ariadne_codegen.client_generators.utils import get_final_type
from graphql import GraphQLObjectType, GraphQLSchema

from ..codegen import generate_class_def, generate_module
from .constants import BASE_OPERATION_FILE_PATH, OPERATION_TYPES


class CustomFieldsTypingGenerator:
    def __init__(
        self,
        schema: GraphQLSchema,
    ) -> None:
        self.schema = schema
        self.graphql_field_import = ast.ImportFrom(
            module=BASE_OPERATION_FILE_PATH.stem,
            names=[ast.alias("GraphQLField")],
            level=1,
        )
        self._public_names: List[str] = []
        self._class_defs: List[ast.ClassDef] = [
            self._generate_field_class(d) for d in self._filter_types()
        ]

    def generate(self) -> ast.Module:
        return generate_module(
            body=(
                cast(List[ast.stmt], [self.graphql_field_import])
                + cast(List[ast.stmt], [self._class_defs])
            )
        )

    def _filter_types(self):
        return [
            get_final_type(definition)
            for name, definition in self.schema.type_map.items()
            if isinstance(definition, GraphQLObjectType)
            and not name.startswith("__")
            and name not in OPERATION_TYPES
        ]

    def _generate_field_class(self, class_def: ast.ClassDef) -> ast.ClassDef:
        class_name = f"{class_def.name}GraphQLField"
        if class_name not in self._public_names:
            self._public_names.append(class_name)
        field_class_def = generate_class_def(
            name=class_name,
            base_names=["GraphQLField"],
            body=[ast.Pass()],
        )
        return field_class_def

    def get_generated_public_names(self) -> List[str]:
        return self._public_names
