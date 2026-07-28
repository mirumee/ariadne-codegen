"""
Plugin that merges the generated package into a single module.

Configuration:

[tool.ariadne-codegen.single-file-client]
output_file_name = "my_client.py"
should_remove_package = false

- output_file_name (defaults: `client.py`) - name of the generated file.
- should_remove_package (defaults to `true`) - if the generated package
    should be deleted from the disk
"""

import ast
import shutil
from graphlib import TopologicalSorter
from pathlib import Path
from typing import cast

from graphql import (
    GraphQLSchema,
)

from ariadne_codegen.codegen import generate_module
from ariadne_codegen.config import get_client_settings
from ariadne_codegen.utils import (
    format_code,
    format_multiline_strings,
    remove_blank_line_between_class_and_content,
)

from ..plugins.base import Plugin

DEFAULT_OUTPUT_FILE_NAME = "client.py"


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

    def generate_files(self, generated_files: list[str]) -> list[str]:
        code = merge_files(
            [Path(self.package_path) / file for file in generated_files],
        )

        self.module_path.write_text(code)

        if not self.should_remove_package:
            return generated_files + [self.module_path.name]
        shutil.rmtree(self.package_path)
        return [self.module_path.name]


def merge_files(files: list[Path]) -> str:
    ordered_files = FlatPackageDependencyResolver(files).get_ordered_files()

    imports = []
    statements = {}
    for file_ in ordered_files:
        raw_content = file_.read_text()
        parsed = ast.parse(raw_content, file_.name)

        file_statements = []
        for node in ast.iter_child_nodes(parsed):
            if isinstance(node, ast.ImportFrom):
                # Skip imports from generated package
                if node.level != 1:
                    imports.append(node)
            elif isinstance(node, ast.Import):
                imports.append(node)
            else:
                file_statements.append(node)

        last_statement = cast(ast.stmt, file_statements[0])
        statements[file_.name] = "\n".join(
            raw_content.splitlines()[last_statement.lineno - 1 :]
        )

    code = (
        ast.unparse(generate_module(body=cast(list[ast.stmt], imports)))
        + "\n"
        + "\n".join(content for content in statements.values())
    )
    code = remove_blank_line_between_class_and_content(code)
    code = format_multiline_strings(code, offset=4)

    return format_code(code, remove_unused_imports=True)


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
