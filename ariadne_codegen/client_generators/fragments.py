import ast
from typing import Dict, List, Optional, Set, cast

from graphql import FragmentDefinitionNode, GraphQLSchema

from ..codegen import generate_expr, generate_method_call, generate_module
from ..plugins.manager import PluginManager
from .constants import UPDATE_FORWARD_REFS_METHOD
from .result_types import ResultTypesGenerator
from .scalars import ScalarData


class FragmentsGenerator:
    def __init__(
        self,
        schema: GraphQLSchema,
        enums_module_name: str,
        fragments_definitions: Dict[str, FragmentDefinitionNode],
        exclude_names: Optional[Set[str]] = None,
        base_model_import: Optional[ast.ImportFrom] = None,
        convert_to_snake_case: bool = True,
        custom_scalars: Optional[Dict[str, ScalarData]] = None,
        plugin_manager: Optional[PluginManager] = None,
    ) -> None:
        self.schema = schema
        self.enums_module_name = enums_module_name
        self.exclude_names = exclude_names or set()
        self.fragments_definitions = fragments_definitions
        self.base_model_import = base_model_import
        self.convert_to_snake_case = convert_to_snake_case
        self.custom_scalars = custom_scalars
        self.plugin_manager = plugin_manager

        self._fragments_names = (
            set(self.fragments_definitions.keys()) - self.exclude_names
        )
        self._generated_public_names: List[str] = []

    def generate(self) -> ast.Module:
        class_defs_dict: Dict[str, List[ast.ClassDef]] = {}
        imports: List[ast.ImportFrom] = []
        dependencies_dict: Dict[str, Set[str]] = {}

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
            class_defs_dict[name] = generator.get_classes()
            dependencies_dict[name] = generator.get_fragments_used_as_mixins()
            self._generated_public_names.extend(generator.get_generated_public_names())

        sorted_class_defs = self._get_sorted_class_defs(
            class_defs_dict=class_defs_dict, dependencies_dict=dependencies_dict
        )
        update_forward_refs_calls = [
            generate_expr(generate_method_call(c.name, UPDATE_FORWARD_REFS_METHOD))
            for c in sorted_class_defs
        ]

        module = generate_module(
            body=cast(List[ast.stmt], imports)
            + cast(List[ast.stmt], sorted_class_defs)
            + cast(List[ast.stmt], update_forward_refs_calls)
        )
        if self.plugin_manager:
            module = self.plugin_manager.generate_fragments_module(
                module, fragments_definitions=self.fragments_definitions
            )
        return module

    def get_generated_public_names(self) -> List[str]:
        return self._generated_public_names

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
