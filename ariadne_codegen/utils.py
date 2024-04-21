import ast
import re
from keyword import iskeyword
from textwrap import indent
from typing import List, Optional

import isort
from autoflake import fix_code  # type: ignore
from black import Mode, format_str
from graphql import Node
from pydantic import BaseModel

from .plugins.manager import PluginManager

PYDANTIC_RESERVED_FIELD_NAMES = [
    name for name in dir(BaseModel) if not name.startswith("_")
]


def ast_to_str(
    ast_obj: ast.AST,
    remove_unused_imports: bool = True,
    multiline_strings: bool = False,
    multiline_strings_offset: int = 4,
) -> str:
    """Convert ast object into string."""
    code = ast.unparse(ast_obj)
    code = remove_blank_line_between_class_and_content(code)
    if remove_unused_imports:
        code = fix_code(code, remove_all_unused_imports=True)
    if multiline_strings:
        code = format_multiline_strings(code, offset=multiline_strings_offset)
    return format_str(isort.code(code), mode=Mode())


def remove_blank_line_between_class_and_content(code: str) -> str:
    """Removes blank lines between class and first method.

    We are doing this for code style consistency and backwards compatibility.
    """
    code_lines: List[str] = []
    skip_blank_lines = False
    for line in code.splitlines():
        if skip_blank_lines and line:
            skip_blank_lines = False
        elif line.startswith("class "):
            skip_blank_lines = True
        if not skip_blank_lines or line:
            code_lines.append(line)
    return "\n".join(code_lines)


def str_to_snake_case(name: str) -> str:
    """Converts camelCase or PascalCase string into snake_case."""
    # lower-case letters that optionally start with a single upper-case letter
    lowercase_words = r"[A-Z]?[a-z]+"
    # upper-case letters, excluding last letter if it is followed by a lower-case letter
    uppercase_words = r"[A-Z]+(?=[A-Z][a-z]|\d|\W|_|$)"
    numbers = r"\d+"

    words = re.findall(rf"{lowercase_words}|{uppercase_words}|{numbers}", name)
    return "_".join(map(str.lower, words))


def str_to_pascal_case(name: str) -> str:
    """Converts snake_case string into PascalCase."""
    return "".join(n[:1].upper() + n[1:] for n in name.split("_"))


def convert_to_multiline_string(
    source: str, variable_indent_size: int = 8, offset: int = 4
) -> str:
    """
    Converts multiple strings into 1 multilne string.
    eg. 'abc\\n''def\\n''ghi\\n' is coverted into
    \"\"\"
        abc
        def
        ghi
        \"\"\"
    """
    joined_source = source.replace("\\n", "\n").replace("'", "")
    if joined_source.endswith("\n"):
        joined_source += '"""'
    else:
        joined_source += '\n"""'
    return '"""\n' + indent(joined_source, (variable_indent_size + offset) * " ")


def get_variable_indent_size(source: str) -> int:
    "Returns number of white characters at the beginning of source."
    match = re.match(r"\s*", source)
    if match:
        return len(match.group())
    return 0


def format_multiline_strings(source: str, offset: int = 4) -> str:
    """Fromats multiline string declarations."""
    formatted_source = source
    for match in re.finditer(r".*?=.*?('.*?'\s*){2,}", source):
        line = match.group()
        variable_indent_size = get_variable_indent_size(line)
        orginal_str_match = re.search("'.*'", line)
        if orginal_str_match:
            orginal_str = orginal_str_match.group()
            formatted = convert_to_multiline_string(
                orginal_str, variable_indent_size=variable_indent_size, offset=offset
            )
            formatted_source = formatted_source.replace(orginal_str, formatted)
    return formatted_source


def process_name(
    name: str,
    convert_to_snake_case: bool,
    plugin_manager: Optional[PluginManager] = None,
    node: Optional[Node] = None,
    trim_leading_underscore: bool = False,
    handle_pydantic_resrved_field_names: bool = False,
) -> str:
    """Processes the GraphQL name to remove keywords
    and optionally convert to snake_case."""
    processed_name = name
    if convert_to_snake_case:
        processed_name = str_to_snake_case(processed_name)
    if iskeyword(processed_name):
        processed_name += "_"
    if (
        handle_pydantic_resrved_field_names
        and processed_name in PYDANTIC_RESERVED_FIELD_NAMES
    ):
        processed_name += "_"
    if trim_leading_underscore:
        processed_name = processed_name.lstrip("_")
    if plugin_manager:
        processed_name = plugin_manager.process_name(processed_name, node=node)
    if set(name) == {"_"} and not processed_name:
        return "underscore_named_field_"
    return processed_name
