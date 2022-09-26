from ast import ClassDef, Module, Pass


class ClientGenerator:
    def __init__(self, name: str = "Client") -> None:
        self.name = name
        self.class_def = ClassDef(
            name=name, bases=[], keywords=[], body=[Pass()], decorator_list=[]
        )
        self.imports: list = []

    def generate(self) -> Module:
        """Generate module with class definistion of grahql client."""
        self.class_def.lineno = len(self.imports) + 1
        return Module(body=self.imports + [self.class_def], type_ignores=[])
