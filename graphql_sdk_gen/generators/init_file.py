from ast import Assign, Constant, List, Module, Name

from .utils import generate_import_from


class InitFileGenerator:
    def __init__(self) -> None:
        self._imports: list = []

    def add_import(self, modules: list[str], from_: str, level: int = 0) -> None:
        """Add import to be included in init file."""
        self._imports.append(
            generate_import_from(modules=modules, from_=from_, level=level)
        )

    def generate(self) -> Module:
        """Generate init with imports and public api of package."""
        module = Module(body=self._imports, type_ignores=[])
        if self._imports:
            constants_names: list[str] = []
            for import_ in self._imports:
                constants_names.extend([n.name for n in import_.names])
            constants_names.sort()

            module.body.append(
                Assign(
                    targets=[
                        Name(
                            id="__all__",
                        )
                    ],
                    value=List(elts=[Constant(value=n) for n in constants_names]),
                    lineno=len(self._imports) + 1,
                )
            )
        return module
