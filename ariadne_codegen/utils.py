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
from pydantic.alias_generators import to_camel

from .plugins.manager import PluginManager

_LINE_LENGTH = 88
_TARGET_VERSION = "py310"
_SUBPROCESS_TIMEOUT = 30

# `ruff check --fix` exits 1 when violations it cannot fix remain. That is not an
# error for us: the fixable ones were still applied.
_RUFF_CHECK_OK_RETURN_CODES = (0, 1)

PYDANTIC_ALIAS_GENERATORS_MODULE = "pydantic.alias_generators"
TO_CAMEL_NAME = "to_camel"

# `to_camel` agrees across every pydantic 2.x only for names it was written to
# take: lowercase, digits and underscores. Given anything with an uppercase
# letter, pydantic < 2.8 runs it through `str.title()` (`firstName` ->
# `firstname`) while >= 2.8 returns it untouched. We decide here, with the
# generator's pydantic, which fields may omit an alias; the generated package
# rebuilds those aliases with the *user's* pydantic. So only names in this
# alphabet are safe to leave to the generator.
_VERSION_STABLE_UNDER_TO_CAMEL = re.compile(r"[a-z0-9_]*")


def needs_explicit_alias(
    python_name: str, schema_name: str, use_alias_generator: bool
) -> bool:
    """Whether a field must carry an explicit `Field(alias=...)`.

    With `alias_generator=to_camel` on the base model, pydantic derives the alias
    from the Python name, so only the names it cannot reconstruct need spelling
    out: `__typename`, keyword-escaped names like `list_`, acronyms (`productID`)
    and schemas that are already snake_case (`some_field` -> `someField`).
    """
    if not use_alias_generator:
        return python_name != schema_name
    if not _VERSION_STABLE_UNDER_TO_CAMEL.fullmatch(python_name):
        return True
    return to_camel(python_name) != schema_name


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
    if check.returncode not in _RUFF_CHECK_OK_RETURN_CODES:
        raise RuntimeError(
            f"ruff check failed (exit code {check.returncode}): {check.stderr}"
        )
    # An empty result is legitimate (e.g. a module of only unused imports), so
    # this must not fall back to `code` on a falsy stdout.
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

        check = subprocess.run(
            _ruff_command()
            + ["check", "--fix", "--no-cache"]
            + _ruff_style_args()
            + ["--select", _ruff_select(remove_unused_imports), tmp_dir],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
            timeout=_SUBPROCESS_TIMEOUT,
        )
        if check.returncode not in _RUFF_CHECK_OK_RETURN_CODES:
            raise RuntimeError(
                f"ruff check failed (exit code {check.returncode}): {check.stderr}"
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


def _split_leading_comments(code: str) -> tuple[str, str]:
    """Separate a module's leading comment block from its code.

    `ast.unparse` drops comments, which would otherwise discard the header that
    `_add_comments_to_code` puts on every generated file.
    """
    lines = code.splitlines(keepends=True)
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return "".join(lines[:index]), "".join(lines[index:])
    return "", code


def _set_base_model_config_kwargs(code: str, kwargs: dict[str, ast.expr]) -> str:
    """Set keyword arguments on the ``ConfigDict`` call in ``BaseModel``.

    Keywords already present are left alone, so explicit user values are never
    overwritten. Every keyword is applied in one parse/unparse round trip.
    """
    header, code = _split_leading_comments(code)
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
            present = {kw.arg for kw in call.keywords}
            call.keywords.extend(
                ast.keyword(arg=arg, value=value)
                for arg, value in kwargs.items()
                if arg not in present
            )
    ast.fix_missing_locations(tree)
    return header + ast.unparse(tree)


def _set_base_model_config_kwarg(code: str, arg: str, value: ast.expr) -> str:
    """Set a single keyword argument on the ``ConfigDict`` call in ``BaseModel``."""
    return _set_base_model_config_kwargs(code, {arg: value})


def _add_import_to_base_model(code: str, module: str, name: str) -> str:
    header, body = _split_leading_comments(code)
    if f"from {module} import {name}" in body:
        return code
    return f"{header}from {module} import {name}\n{body}"


def add_extra_to_base_model(code: str) -> str:
    "Adds `extra='forbid'` to the ConfigDict in BaseModel if not already present."
    return _set_base_model_config_kwarg(code, "extra", ast.Constant("forbid"))


def add_defer_build_to_base_model(code: str) -> str:
    "Adds `defer_build=True` to the ConfigDict in BaseModel if not already present."
    return _set_base_model_config_kwarg(code, "defer_build", ast.Constant(True))


def add_alias_generator_to_base_model(code: str) -> str:
    """Adds `alias_generator=to_camel` to the ConfigDict in BaseModel.

    Generators only emit an explicit `Field(alias=...)` for the fields whose
    GraphQL name `to_camel` cannot reconstruct, so the two must stay in sync.
    """
    code = _set_base_model_config_kwarg(
        code, "alias_generator", ast.Name(id=TO_CAMEL_NAME)
    )
    return _add_import_to_base_model(
        code, PYDANTIC_ALIAS_GENERATORS_MODULE, TO_CAMEL_NAME
    )


def rewrite_base_model(
    code: str,
    *,
    forbid_extra: bool = False,
    defer_build: bool = False,
    alias_generator: bool = False,
) -> str:
    """Apply the requested ConfigDict settings to the copied `base_model.py`.

    Returns `code` untouched when nothing was requested. Otherwise every keyword
    goes in with a single `ast.unparse`, which drops the blank lines and import
    order of the copied dependency, so the result is handed back to ruff.
    """
    kwargs: dict[str, ast.expr] = {}
    if forbid_extra:
        kwargs["extra"] = ast.Constant("forbid")
    if defer_build:
        kwargs["defer_build"] = ast.Constant(True)
    if alias_generator:
        kwargs["alias_generator"] = ast.Name(id=TO_CAMEL_NAME)
    if not kwargs:
        return code

    rewritten = _set_base_model_config_kwargs(code, kwargs)
    if alias_generator:
        rewritten = _add_import_to_base_model(
            rewritten, PYDANTIC_ALIAS_GENERATORS_MODULE, TO_CAMEL_NAME
        )
    return _format_code(rewritten, remove_unused_imports=False)
