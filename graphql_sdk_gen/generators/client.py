import ast
from .utils import generate_import_from

class ClientGenerator:
    def __init__(self, name: str = "Client") -> None:
        self.name = name
        self.class_def = ast.ClassDef(
            name=name, bases=[], keywords=[], body=[], decorator_list=[]
        )
        self.imports: list = []

    def generate(self) -> ast.Module:
        """Generate module with class definistion of grahql client."""
        self.class_def.lineno = len(self.imports) + 1
        if not self.class_def.body:
            self.class_def.body.append(ast.Pass())
        return ast.Module(body=self.imports + [self.class_def], type_ignores=[])

    def add_import(self, names: list[str], from_: str, level: int = 0) -> None:
        """Add import to be included in init file."""
        self.imports.append(generate_import_from(names=names, from_=from_, level=level))

    def add_async_method(
        self, name: str, return_type: str, arguments: ast.arguments
    ):
        self.class_def.body.append(
            ast.AsyncFunctionDef(
                name=name,
                args=arguments,
                body=[ast.Pass()],
                decorator_list=[],
                returns=ast.Name(id=return_type),
                lineno=len(self.class_def.body) + 1,
            )
        )
