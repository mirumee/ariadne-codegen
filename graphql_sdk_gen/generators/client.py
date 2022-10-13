import ast

from .codegen import (
    generate_async_method_definition,
    generate_class_def,
    generate_import_from,
    generate_name,
)
from .constants import OPTIONAL


class ClientGenerator:
    def __init__(self, name: str = "Client") -> None:
        self.name = name
        self.class_def = generate_class_def(name=name)
        self.imports: list = [generate_import_from([OPTIONAL], "typing")]

    def generate(self) -> ast.Module:
        """Generate module with class definistion of grahql client."""
        self.class_def.lineno = len(self.imports) + 1
        if not self.class_def.body:
            self.class_def.body.append(ast.Pass())
        return ast.Module(body=self.imports + [self.class_def], type_ignores=[])

    def add_import(self, names: list[str], from_: str, level: int = 0) -> None:
        """Add import to be included in init file."""
        self.imports.append(generate_import_from(names=names, from_=from_, level=level))

    def add_async_method(self, name: str, return_type: str, arguments: ast.arguments):
        """Add definition of async method."""
        self.class_def.body.append(
            generate_async_method_definition(
                name=name,
                arguments=arguments,
                return_type=generate_name(return_type),
                lineno=len(self.class_def.body) + 1,
            )
        )
