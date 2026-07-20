import ast
from typing import Optional

from ..codegen import generate_import_from
from ..plugins.manager import PluginManager
from .constants import (
    ALL_NAME,
    IMPORTLIB_MODULE,
    LAZY_IMPORTS_MAP_NAME,
    TYPE_CHECKING_FLAG,
    TYPING_MODULE,
)

# Module-level `__getattr__` (PEP 562): Python calls it only for names not already
# in globals, so each generated module is imported the first time one of its names
# is touched, then cached in `globals()` to stay out of the path afterwards. Kept
# as source rather than AST nodes: a fixed block with nothing to parameterize.
LAZY_IMPORTS_HELPERS = '''\
def __getattr__(name):
    """Import the module a generated name lives in, the first time it is used."""
    module_name = {lazy_imports_map}.get(name)
    if module_name is None:
        raise AttributeError(f"module {{__name__!r}} has no attribute {{name!r}}")
    value = getattr(importlib.import_module(module_name, __name__), name)
    globals()[name] = value
    return value


def __dir__():
    return sorted({all_name})
'''


class InitFileGenerator:
    def __init__(
        self,
        plugin_manager: Optional[PluginManager] = None,
        lazy_imports: bool = False,
    ) -> None:
        self.imports: list = []
        self.plugin_manager = plugin_manager
        self.lazy_imports = lazy_imports

    def add_import(self, names: list[str], from_: str, level: int = 0) -> None:
        """Add import to be included in init file."""
        if not names:
            return
        import_ = generate_import_from(names=sorted(names), from_=from_, level=level)
        if self.plugin_manager:
            import_ = self.plugin_manager.generate_init_import(import_)
        self.imports.append(import_)

    def generate(self) -> ast.Module:
        """Generate init with imports and public api of package."""
        if self.lazy_imports and self.imports:
            module = self._generate_lazy_module()
        else:
            module = self._generate_eager_module()
        if self.plugin_manager:
            module = self.plugin_manager.generate_init_module(module)
        return module

    def _get_exported_names(self) -> list[str]:
        names: list[str] = []
        for import_ in self.imports:
            names.extend([n.name for n in import_.names])
        return sorted(names)

    def _generate_all_assign(self, lineno: int) -> ast.Assign:
        return ast.Assign(
            targets=[ast.Name(id=ALL_NAME)],
            value=ast.List(
                elts=[ast.Constant(value=n) for n in self._get_exported_names()]
            ),
            lineno=lineno,
        )

    def _generate_eager_module(self) -> ast.Module:
        module = ast.Module(body=self.imports, type_ignores=[])
        if self.imports:
            module.body.append(self._generate_all_assign(lineno=len(self.imports) + 1))
        return module

    def _generate_lazy_module(self) -> ast.Module:
        """Generate an init that imports each module the first time it is needed.

        The eager init's module-level imports move under `TYPE_CHECKING` (so type
        checkers still resolve every name), and a `__getattr__` hook does the real
        import at runtime. This only pays off with the `ClientForwardRefsPlugin`,
        which `lazy_imports` turns on: otherwise importing `client.py` pulls in the
        input types it annotates with and the deferral buys nothing.
        """
        # An aliased import (`import X as Y`) would need both names carried through
        # here, but nothing generates one: `add_import` builds a plain
        # `ast.alias(name)`, and the eager `__all__` reads `.name` the same way.
        lazy_imports_map: dict[str, str] = {}
        for import_ in self.imports:
            module_name = "." * import_.level + (import_.module or "")
            for name in import_.names:
                lazy_imports_map[name.name] = module_name

        helpers = ast.parse(
            LAZY_IMPORTS_HELPERS.format(
                lazy_imports_map=LAZY_IMPORTS_MAP_NAME, all_name=ALL_NAME
            )
        ).body

        body: list[ast.stmt] = [
            ast.Import(names=[ast.alias(IMPORTLIB_MODULE)]),
            generate_import_from(names=[TYPE_CHECKING_FLAG], from_=TYPING_MODULE),
            ast.If(
                test=ast.Name(id=TYPE_CHECKING_FLAG),
                body=list(self.imports),
                orelse=[],
            ),
            ast.Assign(
                targets=[ast.Name(id=LAZY_IMPORTS_MAP_NAME)],
                value=ast.Dict(
                    keys=[ast.Constant(value=n) for n in sorted(lazy_imports_map)],
                    values=[
                        ast.Constant(value=lazy_imports_map[n])
                        for n in sorted(lazy_imports_map)
                    ],
                ),
                lineno=len(self.imports) + 1,
            ),
            *helpers,
            self._generate_all_assign(lineno=len(self.imports) + 2),
        ]
        module = ast.Module(body=body, type_ignores=[])
        # `helpers` carries linenos from its own parse and the nodes built here have
        # none; unparse only needs them to be present and consistent.
        ast.fix_missing_locations(module)
        return module
