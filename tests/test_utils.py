import ast
import subprocess
import sys
from textwrap import dedent

import pytest

from ariadne_codegen.utils import (
    _format_code,
    add_defer_build_to_base_model,
    add_extra_to_base_model,
    ast_to_str,
    convert_to_multiline_string,
    format_many,
    format_multiline_strings,
    get_variable_indent_size,
    needs_explicit_alias,
    process_name,
    rewrite_base_model,
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


def test_ast_to_str_non_ascii_unicode_round_trip_issue_422():
    """Regression for mirumee/ariadne-codegen#422 (Windows cp1252 / ruff stdin)."""
    description = "商店 line: émoji 🛍️ — characters outside cp1252"
    module = ast.parse(f'"""{description}"""')
    generated = ast_to_str(module, remove_unused_imports=False)
    assert description in generated


def _ruff_calls(spy, subcommand: str) -> list:
    """Calls to `ruff <subcommand>`, whatever prefix `_ruff_command` resolved to."""
    return [
        call
        for call in spy.call_args_list
        if subcommand in call[0][0] and call[0][0].index(subcommand) <= 3
    ]


def test_format_code_ruff_format_uses_utf8_encoding_issue_422(mocker):
    """Ensure ruff format stdin/stdout use UTF-8 (mirumee/ariadne-codegen#422)."""
    spy = mocker.patch("ariadne_codegen.utils.subprocess.run", wraps=subprocess.run)

    _format_code("x = 1\n")

    format_calls = _ruff_calls(spy, "format")
    assert format_calls, "expected a ruff format subprocess.run"
    assert format_calls[-1][1].get("encoding") == "utf-8"


def test_format_code_invokes_ruff_binary_directly(mocker):
    """Spawning `python -m ruff` per file dominates generation time."""
    spy = mocker.patch("ariadne_codegen.utils.subprocess.run", wraps=subprocess.run)

    _format_code("x = 1\n")

    for call in spy.call_args_list:
        assert call[0][0][:2] != [sys.executable, "-m"], (
            "ruff should be spawned as a binary, not through a Python interpreter"
        )


def test_format_code_keeps_empty_result_when_every_import_is_removed():
    """`ruff check --fix` legitimately returns '' here; it must not be discarded."""
    assert _format_code("from enum import Enum\n") == ""
    assert _format_code("from enum import Enum\n", remove_unused_imports=False) == (
        "from enum import Enum\n"
    )


@pytest.mark.parametrize("remove_unused_imports", [True, False])
def test_format_many_matches_format_code_per_module(remove_unused_imports):
    codes = [
        "import os\nx=1\n",
        "from enum import Enum\n",
        "from typing import Optional\nclass A:\n\n    x: Optional[int]=None\n",
        "",
    ]

    assert format_many(codes, remove_unused_imports=remove_unused_imports) == [
        _format_code(code, remove_unused_imports=remove_unused_imports)
        for code in codes
    ]


def test_format_many_without_modules_does_not_spawn_ruff(mocker):
    spy = mocker.patch("ariadne_codegen.utils.subprocess.run", wraps=subprocess.run)

    assert format_many([]) == []
    assert not spy.call_args_list


@pytest.mark.parametrize("formatter", [_format_code, lambda code: format_many([code])])
def test_formatting_raises_when_ruff_check_errors(mocker, formatter):
    """A failed check must not silently ship unsorted imports."""
    real_run = subprocess.run

    def fail_the_check(args, **kwargs):
        if "check" in args:
            return subprocess.CompletedProcess(args, 2, "", "ruff exploded")
        return real_run(args, **kwargs)

    mocker.patch("ariadne_codegen.utils.subprocess.run", side_effect=fail_the_check)

    with pytest.raises(RuntimeError, match="ruff check failed"):
        formatter("x = 1\n")


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


def test_adds_defer_build_to_base_model_if_missing():
    code = dedent("""
        class BaseModel:
            model_config = ConfigDict(populate_by_name=True)
    """)
    expected = dedent("""
        class BaseModel:
            model_config = ConfigDict(populate_by_name=True, defer_build=True)
    """)
    result = add_defer_build_to_base_model(code)
    assert dedent(result).strip() == expected.strip()


def test_adds_defer_build_to_base_model_does_not_overwrite_existing_value():
    code = dedent("""
        class BaseModel:
            model_config = ConfigDict(defer_build=False)
    """)
    expected = dedent("""
        class BaseModel:
            model_config = ConfigDict(defer_build=False)
    """)
    result = add_defer_build_to_base_model(code)
    assert dedent(result).strip() == expected.strip()


def test_adds_defer_build_to_base_model_leaves_other_classes_untouched():
    code = dedent("""
        class NotBaseModel:
            model_config = ConfigDict()
    """)
    expected = dedent("""
        class NotBaseModel:
            model_config = ConfigDict()
    """)
    result = add_defer_build_to_base_model(code)
    assert dedent(result).strip() == expected.strip()


@pytest.mark.parametrize(
    "rewrite", [add_extra_to_base_model, add_defer_build_to_base_model]
)
def test_rewriting_base_model_keeps_the_generated_file_header(rewrite):
    """The rewrites round-trip through `ast.unparse`, which drops comments."""
    code = dedent(
        """\
        # Generated by ariadne-codegen
        # Source: queries.graphql

        from pydantic import BaseModel as PydanticBaseModel
        from pydantic import ConfigDict


        class BaseModel(PydanticBaseModel):
            model_config = ConfigDict(populate_by_name=True)
        """
    )

    result = rewrite(code)

    assert result.startswith(
        "# Generated by ariadne-codegen\n# Source: queries.graphql"
    )


BASE_MODEL_SOURCE = dedent(
    """\
    from pydantic import BaseModel as PydanticBaseModel
    from pydantic import ConfigDict


    class BaseModel(PydanticBaseModel):
        model_config = ConfigDict(populate_by_name=True)
    """
)


def test_rewrite_base_model_without_settings_returns_the_source_untouched():
    assert rewrite_base_model(BASE_MODEL_SOURCE) is BASE_MODEL_SOURCE


def test_rewrite_base_model_applies_every_setting_in_one_pass():
    result = rewrite_base_model(
        BASE_MODEL_SOURCE, forbid_extra=True, defer_build=True, alias_generator=True
    )

    assert "from pydantic.alias_generators import to_camel" in result
    for kwarg in ('extra="forbid"', "defer_build=True", "alias_generator=to_camel"):
        assert kwarg in result, kwarg
    assert "populate_by_name=True" in result


def test_rewrite_base_model_only_imports_to_camel_when_it_is_used():
    result = rewrite_base_model(BASE_MODEL_SOURCE, defer_build=True)

    assert "to_camel" not in result


@pytest.mark.parametrize(
    "python_name, schema_name, expected",
    [
        # `to_camel` reproduces the schema name, so the alias can be left out.
        ("first_name", "firstName", False),
        ("product_id", "productId", False),
        ("id", "id", False),
        ("x2", "x2", False),
        # `to_camel` cannot reproduce these, so they must be spelled out.
        ("some_field", "some_field", True),
        ("product_id", "productID", True),
        ("url", "URL", True),
        ("list_", "list", True),
        ("typename__", "__typename", True),
    ],
)
def test_needs_explicit_alias_with_alias_generator(python_name, schema_name, expected):
    assert needs_explicit_alias(python_name, schema_name, True) is expected


@pytest.mark.parametrize("python_name", ["firstName", "productID", "URL", "lastName"])
def test_needs_explicit_alias_never_trusts_to_camel_on_a_non_snake_case_name(
    python_name,
):
    """`to_camel` mangled camelCase names before pydantic 2.9 (`firstName` ->
    `firstname`). We decide here with our pydantic, but the generated package
    derives the alias with the user's, so those names always get an alias."""
    assert needs_explicit_alias(python_name, python_name, True) is True


@pytest.mark.parametrize(
    "python_name, schema_name, expected",
    [("first_name", "firstName", True), ("some_field", "some_field", False)],
)
def test_needs_explicit_alias_without_alias_generator(
    python_name, schema_name, expected
):
    assert needs_explicit_alias(python_name, schema_name, False) is expected
