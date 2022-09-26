from ast import ClassDef

from graphql_sdk_gen.generators.client import ClientGenerator


def test_generate_returns_module_with_correct_class_name():
    name = "ClientXyz"
    generator = ClientGenerator(name)

    module = generator.generate()
    class_def = next(filter(lambda expr: isinstance(expr, ClassDef), module.body))

    assert class_def.name == name
