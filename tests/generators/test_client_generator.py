import ast
from typing import Optional

from graphql_sdk_gen.generators.client import ClientGenerator


def _get_class_def(module: ast.Module) -> Optional[ast.ClassDef]:
    for expr in module.body:
        if isinstance(expr, ast.ClassDef):
            return expr
    return None


def test_generate_returns_module_with_correct_class_name():
    name = "ClientXyz"
    generator = ClientGenerator(name)

    module = generator.generate()
    class_def = _get_class_def(module)

    assert class_def
    assert class_def.name == name


def test_add_import_adds_import_to_generated_module():
    generator = ClientGenerator()
    name = "Xyz"
    from_ = "xyz"
    number_of_existing_imports = len(generator.imports)
    generator.add_import([name], from_=from_)

    module = generator.generate()
    generated_import = module.body[number_of_existing_imports]

    assert isinstance(generated_import, ast.ImportFrom)
    assert generated_import.module == from_
    assert [n.name for n in generated_import.names] == [name]


def test_add_async_method_adds_method_definition():
    generator = ClientGenerator()
    method_name = "list_xyz"
    return_type = "ListXyz"
    arguments = ast.arguments(
        posonlyargs=[],
        args=[ast.arg(name="self")],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[],
    )

    generator.add_async_method(method_name, return_type, arguments)
    module = generator.generate()

    class_def = _get_class_def(module)
    assert class_def
    method_def = class_def.body[0]

    assert isinstance(method_def, ast.AsyncFunctionDef)
    assert method_def.name == method_name
    assert isinstance(method_def.returns, ast.Name)
    assert method_def.returns.id == return_type
    assert method_def.args == arguments
