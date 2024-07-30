import ast
from collections import defaultdict
from typing import Dict, List, Optional, cast

from graphql import (
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLScalarType,
    GraphQLSchema,
)

from ..codegen import (
    generate_ann_assign,
    generate_class_def,
    generate_constant,
    generate_expr,
    generate_import_from,
    generate_keyword,
    generate_method_call,
    generate_module,
    generate_name,
    generate_pydantic_field,
    model_has_forward_refs,
)
from ..plugins.manager import PluginManager
from ..utils import process_name
from .constants import (
    ALIAS_KEYWORD,
    ANNOTATED,
    ANY,
    BASE_MODEL_CLASS_NAME,
    BASE_MODEL_IMPORT,
    FIELD_CLASS,
    LIST,
    MODEL_REBUILD_METHOD,
    OPTIONAL,
    PLAIN_SERIALIZER,
    PYDANTIC_MODULE,
    TYPING_MODULE,
    UNION,
    UPLOAD_IMPORT,
)
from .input_fields import parse_input_field_default_value, parse_input_field_type
from .scalars import ScalarData, generate_scalar_imports


class InputTypesGenerator:
    def __init__(
        self,
        schema: GraphQLSchema,
        enums_module: str = "enums",
        base_model_import: ast.ImportFrom = BASE_MODEL_IMPORT,
        upload_import: ast.ImportFrom = UPLOAD_IMPORT,
        convert_to_snake_case: bool = True,
        custom_scalars: Optional[Dict[str, ScalarData]] = None,
        plugin_manager: Optional[PluginManager] = None,
    ) -> None:
        self.schema = schema
        self.convert_to_snake_case = convert_to_snake_case
        self.enums_module = enums_module
        self.custom_scalars = custom_scalars if custom_scalars else {}
        self.plugin_manager = plugin_manager

        self._imports = [
            generate_import_from(
                [OPTIONAL, ANY, UNION, LIST, ANNOTATED], TYPING_MODULE
            ),
            generate_import_from([FIELD_CLASS, PLAIN_SERIALIZER], PYDANTIC_MODULE),
            base_model_import,
            upload_import,
        ]
        self._dependencies: Dict[str, List[str]] = defaultdict(list)
        self._used_enums: Dict[str, List[str]] = defaultdict(list)
        self._used_scalars: List[str] = []
        self._class_defs: List[ast.ClassDef] = [
            self._parse_input_definition(d) for d in self._filter_input_types()
        ]
        self._generated_public_names: List[str] = []

    def generate(self, types_to_include: Optional[List[str]] = None) -> ast.Module:
        class_defs = self._filter_class_defs(types_to_include=types_to_include)
        self._generated_public_names = [class_def.name for class_def in class_defs]

        if self._used_enums:
            self._imports.append(
                generate_import_from(self.get_used_enums(), self.enums_module, 1)
            )

        for scalar_name in self._used_scalars:
            scalar_data = self.custom_scalars[scalar_name]
            self._imports.extend(generate_scalar_imports(scalar_data))

        model_rebuild_calls = [
            generate_expr(generate_method_call(class_def.name, MODEL_REBUILD_METHOD))
            for class_def in class_defs
            if model_has_forward_refs(class_def)
        ]

        module_body = (
            cast(List[ast.stmt], self._imports)
            + cast(List[ast.stmt], class_defs)
            + cast(List[ast.stmt], model_rebuild_calls)
        )
        module = generate_module(body=module_body)

        if self.plugin_manager:
            module = self.plugin_manager.generate_inputs_module(module)
        return module

    def get_generated_public_names(self) -> List[str]:
        return self._generated_public_names

    def get_used_enums(self) -> List[str]:
        enums = []
        for input_name in self._generated_public_names:
            enums.extend(self._used_enums[input_name])
        return enums

    def _filter_input_types(self) -> List[GraphQLInputObjectType]:
        return [
            definition
            for name, definition in self.schema.type_map.items()
            if isinstance(definition, GraphQLInputObjectType)
            and not name.startswith("__")
        ]

    def _filter_class_defs(
        self, types_to_include: Optional[List[str]] = None
    ) -> List[ast.ClassDef]:
        if types_to_include is None:
            return self._class_defs

        types_names = set()
        for name in types_to_include:
            types_names.update(self._get_dependencies_of_type(name))

        return [
            class_def for class_def in self._class_defs if class_def.name in types_names
        ]

    def _get_dependencies_of_type(self, type_name: str) -> List[str]:
        visited = set()
        result = []

        def dfs(node):
            if node not in visited:
                visited.add(node)
                result.append(node)

                for neighbor in self._dependencies[node]:
                    dfs(neighbor)

        dfs(type_name)
        return result

    def _parse_input_definition(
        self, definition: GraphQLInputObjectType
    ) -> ast.ClassDef:
        class_def = generate_class_def(
            name=definition.name, base_names=[BASE_MODEL_CLASS_NAME]
        )

        for lineno, (org_name, field) in enumerate(definition.fields.items(), start=1):
            name = process_name(
                org_name,
                convert_to_snake_case=self.convert_to_snake_case,
                plugin_manager=self.plugin_manager,
                node=field,
                trim_leading_underscore=True,
                handle_pydantic_resrved_field_names=True,
            )
            annotation, field_type = parse_input_field_type(
                field.type, custom_scalars=self.custom_scalars
            )
            field_implementation = generate_ann_assign(
                target=generate_name(name),
                annotation=annotation,
                value=parse_input_field_default_value(
                    node=field.ast_node, annotation=annotation, field_type=field_type
                ),
                lineno=lineno,
            )
            if name != org_name:
                field_implementation.value = self._process_field_value(
                    field_implementation=field_implementation, alias=org_name
                )

            if self.plugin_manager:
                field_implementation = self.plugin_manager.generate_input_field(
                    field_implementation, input_field=field, field_name=org_name
                )
            class_def.body.append(field_implementation)
            self._save_dependencies(root_type=definition.name, field_type=field_type)

        if self.plugin_manager:
            class_def = self.plugin_manager.generate_input_class(
                class_def, input_type=definition
            )

        return class_def

    def _process_field_value(
        self,
        field_implementation: ast.AnnAssign,
        alias: str,
    ) -> ast.Call:
        field_with_alias = generate_pydantic_field(
            {ALIAS_KEYWORD: generate_constant(alias)}
        )
        if field_implementation.value:
            if (
                isinstance(field_implementation.value, ast.Call)
                and isinstance(field_implementation.value.func, ast.Name)
                and field_implementation.value.func.id == FIELD_CLASS
            ):
                field_with_alias.keywords.extend(field_implementation.value.keywords)
            else:
                field_with_alias.keywords.append(
                    generate_keyword(value=field_implementation.value, arg="default")
                )
        return field_with_alias

    def _save_dependencies(self, root_type: str, field_type: str = "") -> None:
        if not field_type:
            return
        if isinstance(self.schema.type_map[field_type], GraphQLInputObjectType):
            self._dependencies[root_type].append(field_type)
        elif isinstance(self.schema.type_map[field_type], GraphQLEnumType):
            self._used_enums[root_type].append(field_type)
        elif isinstance(self.schema.type_map[field_type], GraphQLScalarType):
            self._used_scalars.append(field_type)
