import ast

from graphql import build_ast_schema, parse

from ariadne_codegen.generators.constants import ENUM_CLASS, ENUM_MODULE
from ariadne_codegen.generators.enums import EnumsGenerator

from ..utils import compare_ast, filter_class_defs, get_class_def


def test_generate_returns_module_with_correct_imports():
    schema_str = """
    enum CustomEnum {
        VALUE1
        VALUE2
    }
    """
    expected_import = ast.ImportFrom(
        module=ENUM_MODULE, names=[ast.alias(name=ENUM_CLASS)], level=0
    )
    generator = EnumsGenerator(schema=build_ast_schema(parse(schema_str)))

    module = generator.generate()

    import_ = module.body[0]
    assert compare_ast(import_, expected_import)


def test_generate_returns_module_with_enum_class_definition():
    schema_str = """
    enum CustomEnum {
        VALUE1
        VALUE2
    }
    """
    expected_class_def = ast.ClassDef(
        name="CustomEnum",
        bases=[ast.Name(id="str"), ast.Name(id=ENUM_CLASS)],
        keywords=[],
        decorator_list=[],
        body=[
            ast.Assign(
                targets=[ast.Name(id="VALUE1")], value=ast.Constant(value="VALUE1")
            ),
            ast.Assign(
                targets=[ast.Name(id="VALUE2")], value=ast.Constant(value="VALUE2")
            ),
        ],
    )
    generator = EnumsGenerator(schema=build_ast_schema(parse(schema_str)))

    module = generator.generate()

    assert generator.get_generated_public_names() == ["CustomEnum"]
    class_def = get_class_def(module)
    assert class_def.name == "CustomEnum"
    assert compare_ast(class_def, expected_class_def)


def test_generate_returns_module_with_enum_class_definition_for_every_enum():
    schema_str = """
    enum TestEnumA {
        VALUE1
        VALUE2
    }

    enum TestEnumB {
        A
        B
        C
    }

    enum TestEnumC {
        A1
        B2
        C3
        D4
        E5
    }
    """
    expected_class_defs = [
        ast.ClassDef(
            name="TestEnumA",
            bases=[ast.Name(id="str"), ast.Name(id=ENUM_CLASS)],
            keywords=[],
            decorator_list=[],
            body=[
                ast.Assign(
                    targets=[ast.Name(id="VALUE1")], value=ast.Constant(value="VALUE1")
                ),
                ast.Assign(
                    targets=[ast.Name(id="VALUE2")], value=ast.Constant(value="VALUE2")
                ),
            ],
        ),
        ast.ClassDef(
            name="TestEnumB",
            bases=[ast.Name(id="str"), ast.Name(id=ENUM_CLASS)],
            keywords=[],
            decorator_list=[],
            body=[
                ast.Assign(targets=[ast.Name(id="A")], value=ast.Constant(value="A")),
                ast.Assign(targets=[ast.Name(id="B")], value=ast.Constant(value="B")),
                ast.Assign(targets=[ast.Name(id="C")], value=ast.Constant(value="C")),
            ],
        ),
        ast.ClassDef(
            name="TestEnumC",
            bases=[ast.Name(id="str"), ast.Name(id=ENUM_CLASS)],
            keywords=[],
            decorator_list=[],
            body=[
                ast.Assign(targets=[ast.Name(id="A1")], value=ast.Constant(value="A1")),
                ast.Assign(targets=[ast.Name(id="B2")], value=ast.Constant(value="B2")),
                ast.Assign(targets=[ast.Name(id="C3")], value=ast.Constant(value="C3")),
                ast.Assign(targets=[ast.Name(id="D4")], value=ast.Constant(value="D4")),
                ast.Assign(targets=[ast.Name(id="E5")], value=ast.Constant(value="E5")),
            ],
        ),
    ]
    generator = EnumsGenerator(schema=build_ast_schema(parse(schema_str)))

    module = generator.generate()

    assert generator.get_generated_public_names() == [
        "TestEnumA",
        "TestEnumB",
        "TestEnumC",
    ]
    class_defs = filter_class_defs(module)
    assert compare_ast(class_defs, expected_class_defs)
