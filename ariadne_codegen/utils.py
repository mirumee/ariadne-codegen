import ast
import re
from keyword import iskeyword
from textwrap import indent
from typing import Optional

import isort
from autoflake import fix_code  # type: ignore
from black import Mode, format_str
from graphql import Node

from .plugins.manager import PluginManager


def ast_to_str(
    ast_obj: ast.AST,
    remove_unused_imports: bool = True,
    multiline_strings: bool = False,
) -> str:
    """Convert ast object into string."""
    code = ast.unparse(ast_obj)
    if remove_unused_imports:
        code = fix_code(code, remove_all_unused_imports=True)
    if multiline_strings:
        code = format_multiline_strings(code)
    return format_str(isort.code(code), mode=Mode())


def str_to_snake_case(name: str) -> str:
    """Converts camelCase or PascalCase string into snake_case."""
    result = "".join([f"_{c.lower()}" if c.isupper() else c for c in name])
    return result[1:] if result.startswith("_") else result


def str_to_pascal_case(name: str) -> str:
    """Converts snake_case string into PascalCase."""
    return "".join(n[:1].upper() + n[1:] for n in name.split("_"))


def convert_to_multiline_string(source: str, variable_indent_size=8) -> str:
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
    return '"""\n' + indent(joined_source, (variable_indent_size + 4) * " ")


def get_variable_indent_size(source: str) -> int:
    "Returns number of white characters at the beginning of source."
    match = re.match(r"\s*", source)
    if match:
        return len(match.group())
    return 0


def format_multiline_strings(source: str) -> str:
    """Fromats multiline string declarations."""
    formatted_source = source
    for match in re.finditer(r".*?=.*?('.*?'\s*){2,}", source):
        line = match.group()
        variable_indent_size = get_variable_indent_size(line)
        orginal_str_match = re.search("'.*'", line)
        if orginal_str_match:
            orginal_str = orginal_str_match.group()
            formatted = convert_to_multiline_string(orginal_str, variable_indent_size)
            formatted_source = formatted_source.replace(orginal_str, formatted)
    return formatted_source


def process_name(
    name: str,
    convert_to_snake_case: bool,
    plugin_manager: Optional[PluginManager] = None,
    node: Optional[Node] = None,
    trim_leading_underscore: bool = False,
) -> str:
    """Processes the GraphQL name to remove keywords
    and optionally convert to snake_case."""
    processed_name = name
    if convert_to_snake_case:
        processed_name = str_to_snake_case(processed_name)
    if iskeyword(processed_name):
        processed_name += "_"
    if trim_leading_underscore:
        processed_name = processed_name.lstrip("_")
    if plugin_manager:
        processed_name = plugin_manager.process_name(processed_name, node=node)
    return processed_name
