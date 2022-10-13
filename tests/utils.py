import ast
from itertools import zip_longest
from typing import Union


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
