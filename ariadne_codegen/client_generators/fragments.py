import ast
from typing import Dict, List, Optional, Set, cast

from graphql import FragmentDefinitionNode, GraphQLSchema

from ..codegen import generate_expr, generate_method_call, generate_module
from ..plugins.manager import PluginManager
from .constants import BASE_MODEL_IMPORT, MODEL_REBUILD_METHOD
from .result_types import ResultTypesGenerator
from .scalars import ScalarData


class FragmentsGenerator:
    def __init__(
        self,
        schema: GraphQLSchema,
        fragments_definitions: Dict[str, FragmentDefinitionNode],
        enums_module_name: str = "enums",
        base_model_import: ast.ImportFrom = BASE_MODEL_IMPORT,
        convert_to_snake_case: bool = True,
        custom_scalars: Optional[Dict[str, ScalarData]] = None,
        plugin_manager: Optional[PluginManager] = None,
    ) -> None:
        self.schema = schema
        self.enums_module_name = enums_module_name
        self.fragments_definitions = fragments_definitions
        self.base_model_import = base_model_import
        self.convert_to_snake_case = convert_to_snake_case
        self.custom_scalars = custom_scalars
        self.plugin_manager = plugin_manager

        self._fragments_names = set(self.fragments_definitions.keys())
        self._generated_public_names: List[str] = []
        self._used_enums: List[str] = []

    def generate(self, exclude_names: Optional[Set[str]] = None) -> ast.Module:
        class_defs_dict: Dict[str, List[ast.ClassDef]] = {}
        imports: List[ast.ImportFrom] = []
        top_level_class_names: List[str] = []
        dependencies_dict: Dict[str, Set[str]] = {}

        names_to_exclude = exclude_names or set()
        self._fragments_names = self._fragments_names - names_to_exclude
        for name in self._fragments_names:
            fragmanet_def = self.fragments_definitions[name]
            generator = ResultTypesGenerator(
                schema=self.schema,
                operation_definition=fragmanet_def,
                enums_module_name=self.enums_module_name,
                fragments_definitions=self.fragments_definitions,
                base_model_import=self.base_model_import,
                convert_to_snake_case=self.convert_to_snake_case,
                custom_scalars=self.custom_scalars,
                plugin_manager=self.plugin_manager,
            )
            imports.extend(generator.get_imports())
            class_defs = generator.get_classes()
            class_defs_dict[name] = class_defs
            if class_defs:
                top_level_class_names.append(class_defs[0].name)
            dependencies_dict[name] = generator.get_fragments_used_as_mixins()
            self._generated_public_names.extend(generator.get_generated_public_names())
            self._used_enums.extend(generator.get_used_enums())

        sorted_class_defs = self._get_sorted_class_defs(
            class_defs_dict=class_defs_dict, dependencies_dict=dependencies_dict
        )
        module = generate_module(
            body=cast(List[ast.stmt], imports)
            + cast(List[ast.stmt], sorted_class_defs)
            + cast(
                List[ast.stmt],
                self._get_model_rebuild_calls(
                    top_level_fragments_names=top_level_class_names,
                    class_defs=sorted_class_defs,
                ),
            )
        )
        if self.plugin_manager:
            module = self.plugin_manager.generate_fragments_module(
                module, fragments_definitions=self.fragments_definitions
            )
        return module

    def get_generated_public_names(self) -> List[str]:
        return self._generated_public_names

    def get_used_enums(self) -> List[str]:
        return self._used_enums

    def _get_sorted_class_defs(
        self,
        class_defs_dict: Dict[str, List[ast.ClassDef]],
        dependencies_dict: Dict[str, Set[str]],
    ) -> List[ast.ClassDef]:
        sorted_class_defs: List[ast.ClassDef] = []

        for name in self._get_sorted_fragments_names(
            fragments_names=self._fragments_names, dependencies_dict=dependencies_dict
        ):
            sorted_class_defs.extend(class_defs_dict[name])

        return sorted_class_defs

    def _get_sorted_fragments_names(
        self, fragments_names: Set[str], dependencies_dict: Dict[str, Set[str]]
    ) -> List[str]:
        sorted_names: List[str] = []
        visited: Set[str] = set()

        def visit(name):
            if name in visited:
                return
            visited.add(name)
            for dep in dependencies_dict[name]:
                visit(dep)
            sorted_names.append(name)

        for name in sorted(fragments_names):
            visit(name)

        return sorted_names

    def _get_model_rebuild_calls(
        self, top_level_fragments_names: List[str], class_defs: List[ast.ClassDef]
    ) -> List[ast.Call]:
        class_names = [c.name for c in class_defs]
        sorted_fragments_names = sorted(
            top_level_fragments_names, key=class_names.index
        )
        return [
            generate_expr(generate_method_call(name, MODEL_REBUILD_METHOD))
            for name in sorted_fragments_names
        ]
