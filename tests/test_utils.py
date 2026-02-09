import ast
from textwrap import dedent

import pytest

from ariadne_codegen.utils import (
    add_extra_to_base_model,
    ast_to_str,
    convert_to_multiline_string,
    format_multiline_strings,
    get_variable_indent_size,
    process_name,
    str_to_snake_case,
)


@pytest.mark.parametrize(
    ["ast_object", "expected_result"],
    [
        (
            ast.ImportFrom(module="xyz", names=[ast.alias(name="Xyz")], level=1),
            "from .xyz import Xyz\n",
        ),
        (ast.Import(names=[ast.alias(name="xyz")]), "import xyz\n"),
        (
            ast.ClassDef(
                name="Xyz", bases=[], keywords=[], body=[ast.Pass()], decorator_list=[]
            ),
            "class Xyz:\n    pass\n",
        ),
        (
            ast.Assign(
                targets=[ast.Name(id="__all__")],
                value=ast.List(elts=[ast.Constant(value="Xyz")]),
                lineno=1,
            ),
            '__all__ = ["Xyz"]\n',
        ),
    ],
)
def test_ast_to_str_returns_correct_string_without_removing_imports(
    ast_object, expected_result
):
    assert ast_to_str(ast_object, False) == expected_result


def test_ast_to_str_removes_unused_imports():
    not_used_imported_class = "Xyz"
    module = ast.Module(
        body=[
            ast.ImportFrom(
                module="xyz", names=[ast.alias(name=not_used_imported_class)], level=0
            ),
            ast.ImportFrom(module="efg", names=[ast.alias(name="Efg")], level=0),
            ast.ClassDef(
                name="TestClass",
                bases=[ast.Name(id="Efg")],
                keywords=[],
                body=[ast.Pass()],
                decorator_list=[],
            ),
        ],
        type_ignores=[],
    )
    expected_generated_code = dedent(
        """
        from efg import Efg


        class TestClass(Efg):
            pass
        """
    ).lstrip()

    generated_code = ast_to_str(module, True)

    assert generated_code == expected_generated_code
    assert not_used_imported_class not in generated_code


@pytest.mark.parametrize(
    "name, expected_result",
    [
        ("test", "test"),
        ("Test", "test"),
        ("TEST", "test"),
        ("test_word", "test_word"),
        ("TEST_word", "test_word"),
        ("testTEST__Word3", "test_test_word_3"),
        ("TestWord", "test_word"),
        ("testWord", "test_word"),
        ("TESTWord", "test_word"),
        ("TEST%Word", "test_word"),
        ("testWORD", "test_word"),
        ("testW", "test_w"),
        ("TestW", "test_w"),
        ("test_long_word", "test_long_word"),
        ("TestLongWord", "test_long_word"),
        ("testLongWord", "test_long_word"),
        ("test_LongWord", "test_long_word"),
        ("testLongWORD", "test_long_word"),
        ("test123", "test_123"),
        ("123test", "123_test"),
        ("Test123", "test_123"),
        ("123Test", "123_test"),
        ("TEST123", "test_123"),
        ("123TEST", "123_test"),
        ("testWord123", "test_word_123"),
        ("TestWord123", "test_word_123"),
        ("testWORD123", "test_word_123"),
        ("TESTWord123", "test_word_123"),
        ("test123Word", "test_123_word"),
        ("Test123Word", "test_123_word"),
        ("test123WORD", "test_123_word"),
        ("Test123WORD", "test_123_word"),
        ("TEST123Word", "test_123_word"),
        ("testWord123", "test_word_123"),
        ("TestWord123", "test_word_123"),
        ("testWORD123", "test_word_123"),
        ("TestWORD123", "test_word_123"),
        ("TESTWord123", "test_word_123"),
    ],
)
def test_str_to_snake_case_returns_correct_string(name, expected_result):
    assert str_to_snake_case(name) == expected_result


@pytest.mark.parametrize(
    ["source", "expected_indent"],
    [
        ("        query = gql('xyz''xyz')", 8),
        ("    return True", 4),
        ("def abcd():", 0),
    ],
)
def test_get_variable_indent_size_returns_number_of_spaces_at_the_beginning_of_source(
    source, expected_indent
):
    assert get_variable_indent_size(source) == expected_indent


def test_convert_to_multiline_string_removes_string_with_triple_quotes():
    source = "'abc\\n'def\\n''ghi\\n'"
    expected = '"""\n    abc\n    def\n    ghi\n    """'

    assert convert_to_multiline_string(source, variable_indent_size=0) == expected


def test_format_multiline_strings_returns_code_with_formatted_multiline_strings():
    source = """
    async def abcd(self) -> Abcd:
        query = gql('query abcd {\\n''  query1 {\\n''    field1\\n''  }\\n''}\\n')
    """
    expected = '''
    async def abcd(self) -> Abcd:
        query = gql("""
            query abcd {
              query1 {
                field1
              }
            }
            """)
    '''

    assert format_multiline_strings(source) == expected


def test_process_name_triggers_plugin_manager_process_name(mocked_plugin_manager):
    process_name("", convert_to_snake_case=False, plugin_manager=mocked_plugin_manager)

    assert mocked_plugin_manager.process_name.called


@pytest.mark.parametrize("trim_leading_underscore", (True, False))
def test_process_name_returns_default_value_for_name_with_only_underscore(
    trim_leading_underscore,
):
    assert (
        process_name(
            "_",
            convert_to_snake_case=True,
            trim_leading_underscore=trim_leading_underscore,
        )
        == "underscore_named_field_"
    )


@pytest.mark.parametrize("trim_leading_underscore", (True, False))
def test_process_name_returns_name_returned_from_plugin_for_name_with_only_underscore(
    trim_leading_underscore, mocked_plugin_manager, mocker
):
    mocked_plugin_manager.process_name = mocker.MagicMock(
        return_value="name_from_plugin"
    )

    assert (
        process_name(
            "_",
            convert_to_snake_case=True,
            trim_leading_underscore=trim_leading_underscore,
            plugin_manager=mocked_plugin_manager,
        )
        == "name_from_plugin"
    )


def test_adds_extra_to_base_model_if_missing():
    code = dedent("""
        class BaseModel:
            Config = ConfigDict()
    """)
    expected = dedent("""
        class BaseModel:
            Config = ConfigDict(extra='forbid')
    """)
    result = add_extra_to_base_model(code)
    assert dedent(result).strip() == expected.strip()


def test_adds_extra_to_base_model_does_not_overwrite_existing_extra():
    code = dedent("""
        class BaseModel:
            Config = ConfigDict(extra='ignore')
    """)
    expected = dedent("""
        class BaseModel:
            Config = ConfigDict(extra='ignore')
    """)
    result = add_extra_to_base_model(code)
    assert dedent(result).strip() == expected.strip()


def test_adds_extra_to_base_model_leaves_other_classes_untouched():
    code = dedent("""
        class NotBaseModel:
            Config = ConfigDict()
    """)
    expected = dedent("""
        class NotBaseModel:
            Config = ConfigDict()
    """)
    result = add_extra_to_base_model(code)
    assert dedent(result).strip() == expected.strip()
