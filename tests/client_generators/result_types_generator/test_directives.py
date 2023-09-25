import ast
from typing import cast

import pytest
from graphql import OperationDefinitionNode, build_ast_schema, parse

from ariadne_codegen.client_generators.constants import (
    BASE_MODEL_CLASS_NAME,
    INCLUDE_DIRECTIVE_NAME,
    MIXIN_FROM_NAME,
    MIXIN_IMPORT_NAME,
    MIXIN_NAME,
    OPTIONAL,
    SKIP_DIRECTIVE_NAME,
)
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator
from ariadne_codegen.exceptions import ParsingError

from ...utils import compare_ast, filter_imports, get_class_def
from .schema import SCHEMA_STR


def test_generate_adds_base_class_to_generated_type_provided_by_mixin_directive():
    query_str = f"""
    query CustomQuery {{
        camelCaseQuery
        @{MIXIN_NAME}({MIXIN_FROM_NAME}: ".abcd", {MIXIN_IMPORT_NAME}: "MixinClass") {{
            id
        }}
    }}
    """
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
    )

    module = generator.generate()

    class_def = get_class_def(module, 1)
    assert class_def.name == "CustomQueryCamelCaseQuery"
    assert [n.id for n in class_def.bases] == [BASE_MODEL_CLASS_NAME, "MixinClass"]
    import_def = filter_imports(module)[-1]
    assert compare_ast(
        import_def,
        ast.ImportFrom(module=".abcd", names=[ast.alias(name="MixinClass")], level=0),
    )


def test_generate_handles_multiple_mixin_directives():
    query_str = f"""
    query CustomQuery {{
        camelCaseQuery
        @{MIXIN_NAME}({MIXIN_FROM_NAME}: ".abcd", {MIXIN_IMPORT_NAME}: "MixinAbcd") {{
            id
        }}
        query2
        @{MIXIN_NAME}({MIXIN_FROM_NAME}: ".xyz", {MIXIN_IMPORT_NAME}: "MixinXyz") {{
            id
        }}
    }}
    """
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
    )

    module = generator.generate()

    class_def_camel_case = get_class_def(module, 1)
    assert class_def_camel_case.name == "CustomQueryCamelCaseQuery"
    assert [n.id for n in class_def_camel_case.bases] == [
        BASE_MODEL_CLASS_NAME,
        "MixinAbcd",
    ]
    import_def_abcd = filter_imports(module)[-2]
    assert compare_ast(
        import_def_abcd,
        ast.ImportFrom(module=".abcd", names=[ast.alias(name="MixinAbcd")], level=0),
    )
    class_def_query2 = get_class_def(module, 2)
    assert class_def_query2.name == "CustomQueryQuery2"
    assert [n.id for n in class_def_query2.bases] == [
        BASE_MODEL_CLASS_NAME,
        "MixinXyz",
    ]
    import_def_xyz = filter_imports(module)[-1]
    assert compare_ast(
        import_def_xyz,
        ast.ImportFrom(module=".xyz", names=[ast.alias(name="MixinXyz")], level=0),
    )


def test_generate_handles_multiple_mixin_directives_on_one_field():
    query_str = f"""
    query CustomQuery {{
        camelCaseQuery
            @{MIXIN_NAME}({MIXIN_FROM_NAME}: ".abcd", {MIXIN_IMPORT_NAME}: "MixinAbcd")
            @{MIXIN_NAME}({MIXIN_FROM_NAME}: ".xyz", {MIXIN_IMPORT_NAME}: "MixinXyz") {{
            id
        }}
    }}
    """
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
    )

    module = generator.generate()

    class_def = get_class_def(module, 1)
    assert class_def.name == "CustomQueryCamelCaseQuery"
    assert [n.id for n in class_def.bases] == [
        BASE_MODEL_CLASS_NAME,
        "MixinAbcd",
        "MixinXyz",
    ]
    import_def_abcd = filter_imports(module)[-2]
    assert compare_ast(
        import_def_abcd,
        ast.ImportFrom(module=".abcd", names=[ast.alias(name="MixinAbcd")], level=0),
    )
    import_def_xyz = filter_imports(module)[-1]
    assert compare_ast(
        import_def_xyz,
        ast.ImportFrom(module=".xyz", names=[ast.alias(name="MixinXyz")], level=0),
    )


@pytest.mark.parametrize(
    "arguments",
    [
        f'{MIXIN_FROM_NAME}: ".abcd", {MIXIN_IMPORT_NAME}: 1',
        f'{MIXIN_FROM_NAME}: 1, {MIXIN_IMPORT_NAME}: "ClassName"',
        f'{MIXIN_IMPORT_NAME}: "ClassName"',
        f'{MIXIN_FROM_NAME}: ".xyz"',
    ],
)
def test_generator_with_incorrect_data_passed_to_mixin_raises_parsing_error(
    arguments,
):
    query_str = f"""
    query CustomQuery {{
        camelCaseQuery @{MIXIN_NAME}({arguments}) {{
            id
        }}
    }}
    """

    with pytest.raises(ParsingError):
        ResultTypesGenerator(
            schema=build_ast_schema(parse(SCHEMA_STR)),
            operation_definition=cast(
                OperationDefinitionNode, parse(query_str).definitions[0]
            ),
            enums_module_name="enums",
        )


@pytest.mark.parametrize("directive", [INCLUDE_DIRECTIVE_NAME, SKIP_DIRECTIVE_NAME])
def test_generator_returns_module_with_handled_skip_and_include_directives(directive):
    query_str = f"""
    query CustomQuery {{
        query3 {{
            field1 @{directive}{{
                fielda
            }}
            field2 {{
                fielda
            }}
            field3 @{directive}{{
                fielda
            }}
        }}
    }}
    """
    expected_field_def_1 = ast.AnnAssign(
        target=ast.Name(id="field1"),
        annotation=ast.Subscript(
            value=ast.Name(id=OPTIONAL),
            slice=ast.Name(id='"CustomQueryQuery3Field1"'),
        ),
        value=ast.Constant(value=None),
        simple=1,
    )
    expected_field_def_2 = ast.AnnAssign(
        target=ast.Name(id="field3"),
        annotation=ast.Subscript(
            value=ast.Name(id=OPTIONAL),
            slice=ast.Name(id='"CustomQueryQuery3Field3"'),
        ),
        value=ast.Constant(value=None),
        simple=1,
    )
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        convert_to_snake_case=False,
    )

    module = generator.generate()

    class_def = get_class_def(module, 1)
    assert class_def.name == "CustomQueryQuery3"
    assert compare_ast(class_def.body[0], expected_field_def_1)
    assert compare_ast(class_def.body[2], expected_field_def_2)
