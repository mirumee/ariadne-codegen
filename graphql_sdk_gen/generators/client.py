import ast


class ClientGenerator:
    def __init__(self, name: str = "Client") -> None:
        self.name = name
        self.class_def = ast.ClassDef(
            name=name, bases=[], keywords=[], body=[ast.Pass()], decorator_list=[]
        )
        self.imports: list = []

    def generate(self) -> ast.Module:
        """Generate module with class definistion of grahql client."""
        self.class_def.lineno = len(self.imports) + 1
        return ast.Module(body=self.imports + [self.class_def], type_ignores=[])
