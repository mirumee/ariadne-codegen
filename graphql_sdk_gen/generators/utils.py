import ast

import isort
from black import Mode, format_str


def ast_to_str(ast_obj: ast.AST) -> str:
    """Convert ast object into string."""
    return format_str(isort.code(ast.unparse(ast_obj)), mode=Mode())


def generate_import_from(
    names: list[str], from_: str, level: int = 0
) -> ast.ImportFrom:
    """Generate import from statement."""
    return ast.ImportFrom(
        module=from_, names=[ast.alias(n) for n in names], level=level
    )


def to_snake_case(name: str) -> str:
    result =  "".join([f"_{c.lower()}" if c.isupper() else c for c in name])
    return result [1:] if result.startswith("_") else result
