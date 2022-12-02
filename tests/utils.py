import ast
from itertools import zip_longest
from textwrap import dedent
from typing import Optional, Union


def compare_ast(
    node1: Union[ast.AST, list[ast.AST]], node2: Union[ast.AST, list[ast.AST]]
) -> bool:
    if type(node1) is not type(node2):
        return False

    if isinstance(node1, ast.AST):
        for k, var in vars(node1).items():
            if k in {"lineno", "end_lineno", "col_offset", "end_col_offset", "ctx"}:
                continue
            if not compare_ast(var, getattr(node2, k)):
                return False
        return True

    if isinstance(node1, list) and isinstance(node2, list):
        return all(compare_ast(n1, n2) for n1, n2 in zip_longest(node1, node2))

    return node1 == node2


def get_class_def(module: ast.Module, class_index=0) -> Optional[ast.ClassDef]:
    found = 0
    for expr in module.body:
        if isinstance(expr, ast.ClassDef):
            found += 1
            if found - 1 == class_index:
                return expr
    return None


def filter_class_defs(module: ast.Module) -> list[ast.ClassDef]:
    return [expr for expr in module.body if isinstance(expr, ast.ClassDef)]


def format_graphql_str(source: str) -> str:
    return dedent(source).replace(4 * " ", 2 * " ").strip()
