import ast
from typing import List, Optional

from ..codegen import generate_import_from
from ..plugins.manager import PluginManager


class InitFileGenerator:
    def __init__(self, plugin_manager: Optional[PluginManager] = None) -> None:
        self.imports: list = []
        self.plugin_manager = plugin_manager

    def add_import(self, names: List[str], from_: str, level: int = 0) -> None:
        """Add import to be included in init file."""
        if not names:
            return
        import_ = generate_import_from(names=names, from_=from_, level=level)
        if self.plugin_manager:
            import_ = self.plugin_manager.generate_init_import(import_)
        self.imports.append(import_)

    def generate(self) -> ast.Module:
        """Generate init with imports and public api of package."""
        module = ast.Module(body=self.imports, type_ignores=[])
        if self.imports:
            constants_names: List[str] = []
            for import_ in self.imports:
                constants_names.extend([n.name for n in import_.names])
            constants_names.sort()

            module.body.append(
                ast.Assign(
                    targets=[
                        ast.Name(
                            id="__all__",
                        )
                    ],
                    value=ast.List(
                        elts=[ast.Constant(value=n) for n in constants_names]
                    ),
                    lineno=len(self.imports) + 1,
                )
            )
        if self.plugin_manager:
            module = self.plugin_manager.generate_init_module(module)
        return module
