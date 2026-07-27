"""
Plugin that merges the generated package into a single module.

Configuration:

[tool.ariadne-codegen.single-file-client]
output_file_name = "my_client.py"
should_remove_package = false
import_rename_map = [
    {import_from = "module", imported_name = "Class", new_alias = "ModuleClass"}
]

- output_file_name (defaults: `client.py`) - name of the generated file.
- should_remove_package (defaults to `true`) - if the generated package
    should be deleted from the disk
- import_rename_map - change the imports to aliased imports if the name duplicates.
    By default, the mechanism is used to rename `BaseModel` import from `pydantic`
    into `as PydanticBaseModel` since the `BaseModel` class is already defined
    in the generated code. Use this option if your custom code (e.g. custom base client)
    uses the names used in the generated code.
"""

import ast
import shutil
from graphlib import TopologicalSorter
from pathlib import Path
from typing import cast

from graphql import (
    GraphQLSchema,
)

from ariadne_codegen.codegen import generate_constant, generate_module
from ariadne_codegen.config import get_client_settings
from ariadne_codegen.utils import ast_to_str

from ..plugins.base import Plugin

DEFAULT_OUTPUT_FILE_NAME = "client.py"
DEFAULT_RENAME_MAP = [("pydantic", "BaseModel", "PydanticBaseModel")]


class SingleFileClientPlugin(Plugin):
    """
    Merge generated files into a single module.

    By default, it removes the source files.
    """

    def __init__(self, schema: GraphQLSchema, config_dict: dict) -> None:
        super().__init__(schema, config_dict)
        settings = get_client_settings(config_dict=self.config_dict)

        plugin_config = (
            self.config_dict.get("tool", {})
            .get("ariadne-codegen", {})
            .get("single-file-client", {})
        )

        target_path = settings.target_package_path

        self.package_path = Path(target_path) / settings.target_package_name

        self.module_name = plugin_config.get(
            "output_file_name", DEFAULT_OUTPUT_FILE_NAME
        )
        self.module_path = Path(target_path) / self.module_name

        self.should_remove_package = plugin_config.get("should_remove_package", True)

        rename_map = DEFAULT_RENAME_MAP.copy()
        for import_rename in plugin_config.get("import_rename_map", []):
            rename_map.append(
                (
                    import_rename["import_from"],
                    import_rename["imported_name"],
                    import_rename["new_alias"],
                )
            )
        self.rename_map = rename_map

    def generate_files(self, generated_files: list[str]) -> list[str]:
        code = merge_files(
            [Path(self.package_path) / file for file in generated_files],
            self.rename_map,
        )

        self.module_path.write_text(code)

        if not self.should_remove_package:
            return generated_files + [self.module_path.name]
        shutil.rmtree(self.package_path)
        return [self.module_path.name]


def merge_files(files: list[Path], rename_map: list[tuple[str, str, str]]) -> str:
    gql_args_splitter_transformer = GqlArgsSplitter()

    ordered_files = FlatPackageDependencyResolver(files).get_ordered_files()

    imports = []
    statements = []
    for file_ in ordered_files:
        parsed = ast.parse(file_.read_text(), file_.name)
        rename_to_perform = []

        for node in ast.iter_child_nodes(parsed):
            if isinstance(node, ast.ImportFrom):
                # Skip imports from generated package
                if node.level != 1:
                    rename_to_perform.extend(_rename_imports(node, rename_map))
                    imports.append(node)
            elif isinstance(node, ast.Import):
                imports.append(node)
            else:
                _rename_aliased_import_usage(node, rename_to_perform)

                node = gql_args_splitter_transformer.visit(node)
                ast.fix_missing_locations(node)

                statements.append(node)

    module = generate_module(body=cast(list[ast.stmt], imports + statements))
    return ast_to_str(module, multiline_strings=True)


class GqlArgsSplitter(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)

        if isinstance(node.func, ast.Name) and node.func.id == "gql":
            original_string = node.args[0].value
            if "\n" not in original_string:
                return node

            node.args = [
                [
                    generate_constant(line + "\n")
                    for line in original_string.strip().splitlines()
                ]
            ]

        return node


class FlatPackageDependencyResolver:
    def __init__(self, files: list[Path]):
        self.dependency_graph = {}
        self.module_to_file = {
            file_path.stem: file_path
            for file_path in files
            if file_path.name != "__init__.py"
        }

    def get_ordered_files(self) -> list[Path]:
        """Returns a list of file paths ordered linearly by dependency."""
        self._build_graph()

        sorter = TopologicalSorter(self.dependency_graph)
        ordered_modules = tuple(sorter.static_order())

        return [self.module_to_file[mod] for mod in ordered_modules]

    def _build_graph(self):
        """Builds the dependency graph for topological sorting."""
        for module_name, file_path in self.module_to_file.items():
            deps = self._extract_dependencies(file_path)

            valid_deps = {dep for dep in deps if dep in self.module_to_file}
            self.dependency_graph[module_name] = sorted(valid_deps)

    def _extract_dependencies(self, file_path: Path) -> set:
        """Parses a file and targets 'from .module import X' syntax."""
        source = file_path.read_text()
        tree = ast.parse(source, filename=str(file_path))
        deps = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level == 1:
                if node.module:
                    deps.add(node.module)
                else:
                    for alias in node.names:
                        deps.add(alias.name)

        return deps


def _rename_imports(
    node: ast.ImportFrom, rename_map: list[tuple[str, str, str]]
) -> list[tuple[str, str]]:
    rename_to_perform = []
    for rename_module, name_to_rename, new_asname in rename_map:
        if node.module and node.module == rename_module:
            for name in node.names:
                if name.name == name_to_rename:
                    rename_to_perform.append((name_to_rename, new_asname))
                    name.asname = new_asname
                    ast.fix_missing_locations(name)
    return rename_to_perform


def _rename_aliased_import_usage(
    node: ast.stmt, rename_to_perform: list[tuple[str, str]]
):
    for name_to_rename, new_name in rename_to_perform:
        transformer = ClassRenamer(name_to_rename, new_name)
        node = transformer.visit(node)
        ast.fix_missing_locations(node)


class ClassRenamer(ast.NodeTransformer):
    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name

    def visit_Name(self, node):
        self.generic_visit(node)

        if node.id == self.old_name:
            return ast.Name(id=self.new_name, ctx=node.ctx)

        return node
