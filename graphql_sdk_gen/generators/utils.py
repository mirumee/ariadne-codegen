import ast

import isort
from black import Mode, format_str


def ast_to_str(ast_obj: ast.AST) -> str:
    """Convert ast object into string."""
    return format_str(isort.code(ast.unparse(ast_obj)), mode=Mode())


def str_to_snake_case(name: str) -> str:
    result = "".join([f"_{c.lower()}" if c.isupper() else c for c in name])
    return result[1:] if result.startswith("_") else result
