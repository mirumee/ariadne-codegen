import ast

import isort
from autoflake import fix_code
from black import Mode, format_str


def ast_to_str(ast_obj: ast.AST, remove_unused_imports: bool = True) -> str:
    """Convert ast object into string."""
    code = ast.unparse(ast_obj)
    if remove_unused_imports:
        code = fix_code(
            code, remove_all_unused_imports=True, additional_imports=["typing"]
        )
    return format_str(isort.code(code), mode=Mode())


def str_to_snake_case(name: str) -> str:
    result = "".join([f"_{c.lower()}" if c.isupper() else c for c in name])
    return result[1:] if result.startswith("_") else result
