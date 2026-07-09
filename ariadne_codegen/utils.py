import ast
import builtins
import re
import shutil
import subprocess
import sys
import tempfile
from functools import lru_cache
from keyword import iskeyword
from pathlib import Path
from textwrap import indent
from typing import Optional

from graphql import Node
from pydantic import BaseModel

from .plugins.manager import PluginManager

_LINE_LENGTH = 88
_TARGET_VERSION = "py310"
_SUBPROCESS_TIMEOUT = 30

# `ruff check --fix` exits 1 when violations it cannot fix remain. That is not an
# error for us: the fixable ones were still applied.
_RUFF_CHECK_OK_RETURN_CODES = (0, 1)


@lru_cache(maxsize=1)
def _ruff_command() -> list[str]:
    """Command prefix used to invoke ruff.

    Running the binary directly skips a full Python interpreter startup on every
    call, which otherwise dominates generation time for packages with many
    modules. Falls back to `python -m ruff` if the binary cannot be located.
    """
    try:
        from ruff.__main__ import find_ruff_bin

        return [find_ruff_bin()]
    except (ImportError, FileNotFoundError):
        pass

    ruff_path = shutil.which("ruff")
    if ruff_path:
        return [ruff_path]

    return [sys.executable, "-m", "ruff"]


def _ruff_style_args() -> list[str]:
    """`--isolated` keeps output deterministic regardless of the user's config."""
    return [
        "--isolated",
        "--target-version",
        _TARGET_VERSION,
        "--line-length",
        str(_LINE_LENGTH),
    ]


def _ruff_select(remove_unused_imports: bool) -> str:
    return "I,F401" if remove_unused_imports else "I"


def _format_code(code: str, *, remove_unused_imports: bool = True) -> str:
    """Format a single module with ruff: sort imports, drop unused ones, format."""
    check = subprocess.run(
        _ruff_command()
        + ["check", "--fix"]
        + _ruff_style_args()
        + [
            "--select",
            _ruff_select(remove_unused_imports),
            "--stdin-filename",
            "generated.py",
            "-",
        ],
        input=code,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=_SUBPROCESS_TIMEOUT,
    )
    if check.returncode in _RUFF_CHECK_OK_RETURN_CODES:
        # An empty result is legitimate (e.g. a module of only unused imports),
        # so this must not fall back to `code` on a falsy stdout.
        code = check.stdout

    result = subprocess.run(
        _ruff_command() + ["format"] + _ruff_style_args() + ["-"],
        input=code,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        timeout=_SUBPROCESS_TIMEOUT,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"ruff format failed (exit code {result.returncode}): {result.stderr}"
        )
    return result.stdout


def format_many(codes: list[str], *, remove_unused_imports: bool = True) -> list[str]:
    """Format many modules with a single pair of ruff invocations.

    Equivalent to calling `_format_code` on each module, but ruff walks a scratch
    directory instead of being spawned twice per module.
    """
    if not codes:
        return []

    with tempfile.TemporaryDirectory() as tmp_dir:
        paths = []
        for index, code in enumerate(codes):
            path = Path(tmp_dir) / f"module_{index}.py"
            path.write_text(code, encoding="utf-8")
            paths.append(path)

        subprocess.run(
            _ruff_command()
            + ["check", "--fix", "--no-cache"]
            + _ruff_style_args()
            + ["--select", _ruff_select(remove_unused_imports), tmp_dir],
            capture_output=True,
            check=False,
            timeout=_SUBPROCESS_TIMEOUT,
        )

        result = subprocess.run(
            _ruff_command() + ["format", "--no-cache"] + _ruff_style_args() + [tmp_dir],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
            timeout=_SUBPROCESS_TIMEOUT,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"ruff format failed (exit code {result.returncode}): {result.stderr}"
            )

        return [path.read_text(encoding="utf-8") for path in paths]


PYDANTIC_RESERVED_FIELD_NAMES = [
    name for name in dir(BaseModel) if not name.startswith("_")
]


def _is_builtin_type_name(name: str) -> bool:
    try:
        value = getattr(builtins, name)
    except AttributeError:
        return False
    return isinstance(value, type)


def ast_to_raw_str(
    ast_obj: ast.AST,
    multiline_strings: bool = False,
    multiline_strings_offset: int = 4,
) -> str:
    """Convert ast object into string, without running ruff over it."""
    code = ast.unparse(ast_obj)
    code = remove_blank_line_between_class_and_content(code)
    if multiline_strings:
        code = format_multiline_strings(code, offset=multiline_strings_offset)
    return code


def ast_to_str(
    ast_obj: ast.AST,
    remove_unused_imports: bool = True,
    multiline_strings: bool = False,
    multiline_strings_offset: int = 4,
) -> str:
    """Convert ast object into string."""
    return _format_code(
        ast_to_raw_str(ast_obj, multiline_strings, multiline_strings_offset),
        remove_unused_imports=remove_unused_imports,
    )


def remove_blank_line_between_class_and_content(code: str) -> str:
    """Removes blank lines between class and first method.

    We are doing this for code style consistency and backwards compatibility.
    """
    code_lines: list[str] = []
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
    if iskeyword(processed_name) or _is_builtin_type_name(processed_name):
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


def _set_base_model_config_kwarg(code: str, arg: str, value: ast.expr) -> str:
    """Set a keyword argument on the ``ConfigDict`` call in ``BaseModel``.

    Does nothing if the keyword is already present, so explicit user values are
    never overwritten.
    """
    tree = ast.parse(code)
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        if node.name != "BaseModel":
            continue
        for statement in node.body:
            if not isinstance(statement, ast.Assign):
                continue
            call = statement.value
            if not isinstance(call, ast.Call):
                continue
            if not isinstance(call.func, ast.Name):
                continue
            if call.func.id != "ConfigDict":
                continue
            if not any(kw.arg == arg for kw in call.keywords):
                call.keywords.append(ast.keyword(arg=arg, value=value))
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


def add_extra_to_base_model(code: str) -> str:
    "Adds `extra='forbid'` to the ConfigDict in BaseModel if not already present."
    return _set_base_model_config_kwarg(code, "extra", ast.Constant("forbid"))


def add_defer_build_to_base_model(code: str) -> str:
    "Adds `defer_build=True` to the ConfigDict in BaseModel if not already present."
    return _set_base_model_config_kwarg(code, "defer_build", ast.Constant(True))
