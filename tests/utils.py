import ast
import re
from itertools import zip_longest
from textwrap import dedent
from typing import List, Optional, Set, Union, cast

# from requests_toolbelt.multipart import decoder


def compare_ast(
    node1: Union[ast.AST, List[ast.AST]], node2: Union[ast.AST, List[ast.AST]]
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


def get_class_def(
    module: ast.Module, class_index=0, name_filter=None
) -> Optional[ast.ClassDef]:
    found = 0
    for expr in module.body:
        if isinstance(expr, ast.ClassDef) and (
            not name_filter or expr.name == name_filter
        ):
            found += 1
            if found - 1 == class_index:
                return expr
    return None


def get_assignment_target_names(class_def: ast.ClassDef) -> Set[str]:
    return {
        x.target.id
        for x in class_def.body
        if isinstance(x, ast.AnnAssign) and isinstance(x.target, ast.Name)
    }


def filter_ast_objects(module: ast.Module, ast_class) -> List[ast.AST]:
    return [expr for expr in module.body if isinstance(expr, ast_class)]


def filter_class_defs(module: ast.Module) -> List[ast.ClassDef]:
    return cast(List[ast.ClassDef], filter_ast_objects(module, ast.ClassDef))


def filter_imports(module: ast.Module) -> List[ast.ImportFrom]:
    return cast(List[ast.ImportFrom], filter_ast_objects(module, ast.ImportFrom))


def format_graphql_str(source: str) -> str:
    return dedent(source).replace(4 * " ", 2 * " ").strip()


def sorted_imports(imports: List[ast.ImportFrom]) -> List[ast.ImportFrom]:
    return sorted(imports, key=lambda import_: import_.module or "")


# def decode_multipart_request(request):
#     return {
#         extract_name_from_part(part): part
#         for part in decoder.MultipartDecoder(
#             request.content, request.headers.get("content-type")
#         ).parts
#     }


def extract_name_from_part(part):
    content_disposition = part.headers[b"Content-Disposition"]
    match = re.search(r'name="(.*?)"', content_disposition.decode("utf-8"))
    if match:
        return match.group(1)

    return None
