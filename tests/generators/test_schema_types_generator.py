import ast

import pytest
from graphql import GraphQLSchema, build_ast_schema, parse

from graphql_sdk_gen.generators.constants import ANY, OPTIONAL, UNION, ClassType
from graphql_sdk_gen.generators.schema_types import SchemaTypesGenerator

from ..utils import compare_ast, get_class_def


@pytest.mark.parametrize(
    "field_name, field_type, expected_annotation",
    [
        ("id", "ID!", ast.Name(id="str")),
        ("name", "String!", ast.Name(id="str")),
        ("count", "Int!", ast.Name(id="int")),
        ("ratio", "Float!", ast.Name(id="float")),
        ("flag", "Boolean!", ast.Name(id="bool")),
        (
            "id",
            "ID",
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
        (
            "name",
            "String",
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
        ),
        (
            "count",
            "Int",
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="int")),
        ),
        (
            "ratio",
            "Float",
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="float")),
        ),
        (
            "flag",
            "Boolean",
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="bool")),
        ),
    ],
)
def test_generator_parses_type_definition_with_scalar_field(
    field_name, field_type, expected_annotation
):
    type_name = "CustomType"
    schema_str = f"type {type_name} {{{field_name}: {field_type}}}"
    schema = build_ast_schema(parse(schema_str))
    expected_field_def = ast.AnnAssign(
        target=ast.Name(id=field_name),
        annotation=expected_annotation,
        simple=1,
    )
    expected_class_def = ast.ClassDef(
        name=type_name,
        bases=[ast.Name(id="BaseModel")],
        keywords=[],
        decorator_list=[],
        body=[expected_field_def],
    )

    generator = SchemaTypesGenerator(schema)

    assert generator.schema_types == [type_name]
    assert generator.class_types[type_name] == ClassType.OBJECT
    class_def = generator.schema_types_classes[0]
    assert isinstance(class_def, ast.ClassDef)
    assert compare_ast(class_def, expected_class_def)
    assert compare_ast(generator.fields[type_name][field_name], expected_field_def)


def test_generator_parses_type_with_custom_type_fields():
    schema_str = """
    type CustomType {
        field1: CustomType1!
        field2: CustomType2
    }

    type CustomType1 {
        field: Int!
    }

    type CustomType2 {
        field: Int!
    }
    """
    expected_class_def = ast.ClassDef(
        name="CustomType",
        bases=[ast.Name(id="BaseModel")],
        keywords=[],
        decorator_list=[],
        body=[
            ast.AnnAssign(
                target=ast.Name(id="field1"),
                annotation=ast.Name(id='"CustomType1"'),
                simple=1,
            ),
            ast.AnnAssign(
                target=ast.Name(id="field2"),
                annotation=ast.Subscript(
                    value=ast.Name(id=OPTIONAL), slice=ast.Name(id='"CustomType2"')
                ),
                simple=1,
            ),
        ],
    )
    schema = build_ast_schema(parse(schema_str))

    generator = SchemaTypesGenerator(schema)

    assert set(generator.schema_types) == {"CustomType", "CustomType1", "CustomType2"}
    assert generator.class_types["CustomType"] == ClassType.OBJECT
    class_def = generator.schema_types_classes[0]
    assert isinstance(class_def, ast.ClassDef)
    assert compare_ast(class_def, expected_class_def)


def test_generator_parses_enum_definition():
    val1, val2 = "VALUE1", "VALUE2"
    enum_name = "CustomEnum"
    schema_str = f"enum {enum_name} {{{val1} {val2}}}"
    schema = build_ast_schema(parse(schema_str))
    expected_class_def = ast.ClassDef(
        name=enum_name,
        bases=[ast.Name(id="str"), ast.Name(id="Enum")],
        keywords=[],
        decorator_list=[],
        body=[
            ast.Assign(targets=[ast.Name(id=val1)], value=ast.Constant(value=val1)),
            ast.Assign(targets=[ast.Name(id=val2)], value=ast.Constant(value=val2)),
        ],
    )

    generator = SchemaTypesGenerator(schema)

    assert generator.enums == [enum_name]
    assert generator.class_types[enum_name] == ClassType.ENUM
    class_def = generator.enums_classes[0]
    assert isinstance(class_def, ast.ClassDef)
    assert compare_ast(class_def, expected_class_def)


def test_generator_parses_type_that_implements_interface():
    schema_str = """
    type CustomType implements CustomInterface {
        id: ID!
    }
    interface CustomInterface {
        id: ID!
    }
    """
    schema = build_ast_schema(parse(schema_str))
    expected_field_def = ast.AnnAssign(
        target=ast.Name(id="id"),
        annotation=ast.Name(id="str"),
        simple=1,
    )
    expected_type_def = ast.ClassDef(
        name="CustomType",
        bases=[ast.Name(id="CustomInterface")],
        keywords=[],
        decorator_list=[],
        body=[expected_field_def],
    )
    expected_interface_def = ast.ClassDef(
        name="CustomInterface",
        bases=[ast.Name(id="BaseModel")],
        keywords=[],
        decorator_list=[],
        body=[expected_field_def],
    )

    generator = SchemaTypesGenerator(schema)

    assert set(generator.schema_types) == {"CustomType", "CustomInterface"}
    assert generator.class_types["CustomType"] == ClassType.OBJECT
    assert generator.class_types["CustomInterface"] == ClassType.INTERFACE
    interface_def = generator.schema_types_classes[0]
    type_def = generator.schema_types_classes[1]
    assert isinstance(interface_def, ast.ClassDef)
    assert isinstance(type_def, ast.ClassDef)
    assert compare_ast(type_def, expected_type_def)
    assert compare_ast(interface_def, expected_interface_def)


def test_generator_parses_input_type():
    schema_str = """
    input CustomInput {
        field1: CustomInput2!
        field2: Int!
    }

    input CustomInput2 {
        field: Int!
    }
    """
    expected_class_def = ast.ClassDef(
        name="CustomInput",
        bases=[ast.Name(id="BaseModel")],
        keywords=[],
        decorator_list=[],
        body=[
            ast.AnnAssign(
                target=ast.Name(id="field1"),
                annotation=ast.Name(id='"CustomInput2"'),
                simple=1,
            ),
            ast.AnnAssign(
                target=ast.Name(id="field2"),
                annotation=ast.Name(id="int"),
                simple=1,
            ),
        ],
    )
    schema = build_ast_schema(parse(schema_str))

    generator = SchemaTypesGenerator(schema)

    assert set(generator.input_types) == {"CustomInput", "CustomInput2"}
    assert generator.class_types["CustomInput"] == ClassType.INPUT
    class_def = generator.input_types_classes[0]
    assert isinstance(class_def, ast.ClassDef)
    assert compare_ast(class_def, expected_class_def)


def test_generate_returns_modules_with_correct_imports():
    generator = SchemaTypesGenerator(
        GraphQLSchema(),
        base_model_import=ast.ImportFrom(
            module="base_model", names=[ast.alias(name="BaseModel")], level=1
        ),
    )

    enums_module, input_types_module, schema_types_module = generator.generate()

    enums_imports = list(
        filter(lambda i: isinstance(i, ast.ImportFrom), enums_module.body)
    )
    expected_enums_imports = [
        ast.ImportFrom(module="enum", names=[ast.alias(name="Enum")], level=0)
    ]
    assert compare_ast(enums_imports, expected_enums_imports)

    input_types_imports = list(
        filter(lambda i: isinstance(i, ast.ImportFrom), input_types_module.body)
    )
    expected_input_types_imports = [
        ast.ImportFrom(
            module="typing",
            names=[
                ast.alias(name=OPTIONAL),
                ast.alias(name=ANY),
                ast.alias(name=UNION),
            ],
            level=0,
        ),
        ast.ImportFrom(
            module="pydantic",
            names=[ast.alias(name="Field")],
            level=0,
        ),
        ast.ImportFrom(
            module="base_model", names=[ast.alias(name="BaseModel")], level=1
        ),
    ]
    assert compare_ast(input_types_imports, expected_input_types_imports)

    schema_types_imports = list(
        filter(lambda i: isinstance(i, ast.ImportFrom), schema_types_module.body)
    )
    expected_schema_types_imports = [
        ast.ImportFrom(
            module="typing",
            names=[
                ast.alias(name=OPTIONAL),
                ast.alias(name=ANY),
                ast.alias(name=UNION),
            ],
            level=0,
        ),
        ast.ImportFrom(module="pydantic", names=[ast.alias(name="Field")], level=0),
        ast.ImportFrom(
            module="base_model", names=[ast.alias(name="BaseModel")], level=1
        ),
    ]
    assert compare_ast(schema_types_imports, expected_schema_types_imports)


def test_generate_returns_modules_with_class_definitions():
    schema_str = """
    type CustomType implements CustomInterface {
        id: ID!
        field1: CustomType1!
        field2: CustomType2
        field3: CustomEnum!
    }

    interface CustomInterface {
        id: ID!
    }

    type CustomType1 {
        field: Int!
    }

    type CustomType2 {
        field: Int!
    }

    enum CustomEnum {
        VAL1
        VAL2
    }

    input CustomInput {
        field: Int!
    }
    """
    schema = build_ast_schema(parse(schema_str))
    generator = SchemaTypesGenerator(schema)

    enums_module, input_types_module, schema_types_module = generator.generate()

    assert {c.name for c in enums_module.body if isinstance(c, ast.ClassDef)} == {
        "CustomEnum"
    }
    assert {c.name for c in input_types_module.body if isinstance(c, ast.ClassDef)} == {
        "CustomInput"
    }
    assert {
        c.name for c in schema_types_module.body if isinstance(c, ast.ClassDef)
    } == {
        "CustomType",
        "CustomInterface",
        "CustomType1",
        "CustomType2",
    }


def test_generate_returns_modules_with_update_forward_refs_calls():
    schema_str = """
    type CustomType implements CustomInterface {
        id: ID!
        field1: CustomType1!
        field2: CustomType2
        field3: CustomEnum!
    }

    interface CustomInterface {
        id: ID!
    }

    type CustomType1 {
        field: Int!
    }

    type CustomType2 {
        field: Int!
    }

    enum CustomEnum {
        VAL1
        VAL2
    }

    input CustomInput {
        field: Int!
    }
    """
    schema = build_ast_schema(parse(schema_str))
    generator = SchemaTypesGenerator(schema)

    enums_module, input_types_module, schema_types_module = generator.generate()

    enums_module_methods_calls = list(
        filter(lambda x: isinstance(x, ast.Expr), enums_module.body)
    )
    assert not enums_module_methods_calls

    input_types_module_methods_calls = list(
        filter(lambda x: isinstance(x, ast.Expr), input_types_module.body)
    )
    expected_input_types_module_methods_calls = [
        ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="CustomInput"), attr="update_forward_refs"
                ),
                args=[],
                keywords=[],
            )
        )
    ]
    assert compare_ast(
        input_types_module_methods_calls, expected_input_types_module_methods_calls
    )

    schema_types_module_methods_calls = list(
        filter(lambda x: isinstance(x, ast.Expr), schema_types_module.body)
    )
    expected_schema_types_module_methods_calls = [
        ast.Expr(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id=name), attr="update_forward_refs"),
                args=[],
                keywords=[],
            )
        )
        for name in [
            "CustomInterface",
            "CustomType",
            "CustomType1",
            "CustomType2",
        ]
    ]
    assert compare_ast(
        schema_types_module_methods_calls, expected_schema_types_module_methods_calls
    )


@pytest.mark.parametrize(
    "field_str, expected_field_value",
    [
        ("field: Int! = 5", ast.Constant(value=5)),
        ("field: Float = 1.5", ast.Constant(value=1.5)),
        ('field: String = "abc"', ast.Constant(value="abc")),
        ("field: Boolean = false", ast.Constant(value=False)),
        ("field: String = null", ast.Constant(value=None)),
    ],
)
def test_generator_parses_inputs_scalar_field_default_value(
    field_str, expected_field_value
):
    schema_str = f"input testInput {{{field_str}}}"
    schema = build_ast_schema(parse(schema_str))

    generator = SchemaTypesGenerator(schema)
    _, input_module, _ = generator.generate()

    class_def = get_class_def(input_module)

    assert isinstance(class_def, ast.ClassDef)
    assert class_def.name == "testInput"
    assert len(class_def.body) == 1
    field_def = class_def.body[0]
    assert isinstance(field_def, ast.AnnAssign)
    assert field_def.value
    assert compare_ast(field_def.value, expected_field_value)


@pytest.mark.parametrize(
    "field_str, expected_list",
    [
        (
            "field: [Int!] = [1, 2]",
            ast.List(elts=[ast.Constant(value=1), ast.Constant(value=2)]),
        ),
        (
            'field: [String!] = ["a", "b", "c"]',
            ast.List(
                elts=[
                    ast.Constant(value="a"),
                    ast.Constant(value="b"),
                    ast.Constant(value="c"),
                ]
            ),
        ),
        (
            'field: [[String]!] = [["a", "a"], ["b", "b"], ["c", "c"]]',
            ast.List(
                elts=[
                    ast.List(
                        elts=[
                            ast.Constant(value="a"),
                            ast.Constant(value="a"),
                        ]
                    ),
                    ast.List(
                        elts=[
                            ast.Constant(value="b"),
                            ast.Constant(value="b"),
                        ]
                    ),
                    ast.List(
                        elts=[
                            ast.Constant(value="c"),
                            ast.Constant(value="c"),
                        ]
                    ),
                ]
            ),
        ),
    ],
)
def test_generator_parses_inputs_list_field_default_value(field_str, expected_list):
    schema_str = f"input testInput {{{field_str}}}"
    expected_pydantic_field = ast.Call(
        func=ast.Name(id="Field"),
        args=[],
        keywords=[
            ast.keyword(
                arg="default_factory",
                value=ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=expected_list,
                ),
            )
        ],
    )

    schema = build_ast_schema(parse(schema_str))

    generator = SchemaTypesGenerator(schema)
    _, input_module, _ = generator.generate()

    class_def = get_class_def(input_module)

    assert isinstance(class_def, ast.ClassDef)
    assert class_def.name == "testInput"
    assert len(class_def.body) == 1
    field_def = class_def.body[0]
    assert isinstance(field_def, ast.AnnAssign)
    assert field_def.value
    assert compare_ast(field_def.value, expected_pydantic_field)


def test_generator_parses_inputs_object_field_default_value():
    schema_str = """
    input testInput {
        field: secondInput = {val: 5}
    }

    input secondInput {
        val: Int!
    }
    """
    expected_field_value = ast.Call(
        func=ast.Attribute(value=ast.Name(id="secondInput"), attr="parse_obj"),
        args=[
            ast.Dict(keys=[ast.Constant(value="val")], values=[ast.Constant(value=5)])
        ],
        keywords=[],
    )
    schema = build_ast_schema(parse(schema_str))

    generator = SchemaTypesGenerator(schema)
    _, input_module, _ = generator.generate()

    class_def = get_class_def(input_module, 1)

    assert isinstance(class_def, ast.ClassDef)
    assert class_def.name == "testInput"
    assert len(class_def.body) == 1
    field_def = class_def.body[0]
    assert isinstance(field_def, ast.AnnAssign)
    assert field_def.value
    assert compare_ast(field_def.value, expected_field_value)


def test_generator_parses_inputs_field_with_nested_object_as_default_value():
    schema_str = """
    input testInput {
        field: secondInput = { nested: { val: 1.5 } }
    }

    input secondInput {
        nested: nestedInput! = { val: 2.5 }
    }

    input nestedInput {
        val: Float! 
    }
    """
    expected_field_value = ast.Call(
        func=ast.Attribute(value=ast.Name(id="secondInput"), attr="parse_obj"),
        args=[
            ast.Dict(
                keys=[ast.Constant(value="nested")],
                values=[
                    ast.Dict(
                        keys=[ast.Constant(value="val")],
                        values=[ast.Constant(value=1.5)],
                    )
                ],
            )
        ],
        keywords=[],
    )
    schema = build_ast_schema(parse(schema_str))

    generator = SchemaTypesGenerator(schema)
    _, input_module, _ = generator.generate()

    class_def = get_class_def(input_module, 2)

    assert isinstance(class_def, ast.ClassDef)
    assert class_def.name == "testInput"
    assert len(class_def.body) == 1
    field_def = class_def.body[0]
    assert isinstance(field_def, ast.AnnAssign)
    assert field_def.value
    assert compare_ast(field_def.value, expected_field_value)


def test_generator_generates_input_types_classes_in_correct_order():
    schema_str = """
    input beforeInput {
        field: Boolean!
    }

    input testInput {
        field: secondInput = { nested: { val: 1.5 } }
    }

    input secondInput {
        nested: nestedInput! = { val: 2.5 }
    }

    input nestedInput {
        val: Float! 
    }

    input afterInput {
        field: Boolean!
    }
    """

    schema = build_ast_schema(parse(schema_str))

    generator = SchemaTypesGenerator(schema)
    _, input_module, _ = generator.generate()

    generated_class_names = [
        c.name for c in input_module.body if isinstance(c, ast.ClassDef)
    ]

    assert generated_class_names == [
        "beforeInput",
        "nestedInput",
        "secondInput",
        "testInput",
        "afterInput",
    ]
