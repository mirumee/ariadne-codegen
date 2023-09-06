import ast
from typing import cast

from graphql import OperationDefinitionNode, build_ast_schema, parse

from ariadne_codegen.client_generators.result_types import ResultTypesGenerator
from ariadne_codegen.client_generators.scalars import ScalarData

from ...utils import compare_ast, filter_imports, sorted_imports
from .schema import SCHEMA_STR


def test_generate_returns_module_with_enum_imports():
    query_str = """
    query CustomQuery {
        query2 {
            field3
        }
    }
    """
    operation_definition = cast(
        OperationDefinitionNode, parse(query_str).definitions[0]
    )
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=operation_definition,
        enums_module_name="enums",
    )

    module = generator.generate()

    assert isinstance(module, ast.Module)
    import_ = filter_imports(module)[-1]
    assert compare_ast(
        import_,
        ast.ImportFrom(module="enums", names=[ast.alias("CustomEnum")], level=1),
    )


def test_generate_returns_module_with_used_custom_scalars_imports():
    query_str = """
    query CustomQuery {
        camelCaseQuery {
            scalarField
        }
    }
    """
    operation_definition = cast(
        OperationDefinitionNode, parse(query_str).definitions[0]
    )
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=operation_definition,
        enums_module_name="enums",
        custom_scalars={
            "SCALARA": ScalarData(
                type_=".custom_scalars.ScalarA",
                graphql_name="SCALARA",
                parse=".custom_scalars.parse_scalar_a",
            )
        },
    )
    expected_imports = [
        ast.ImportFrom(module=".custom_scalars", names=[ast.alias("ScalarA")], level=0),
        ast.ImportFrom(
            module=".custom_scalars", names=[ast.alias("parse_scalar_a")], level=0
        ),
    ]

    module = generator.generate()

    assert isinstance(module, ast.Module)
    imports = filter_imports(module)[-2:]
    assert compare_ast(sorted_imports(imports), sorted_imports(expected_imports))


def test_generate_returns_module_with_used_fragment_import():
    query_str = "query CustomQuery { query2 { ...TestFragment } }"
    operation_definition = cast(
        OperationDefinitionNode, parse(query_str).definitions[0]
    )
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=operation_definition,
        enums_module_name="enums",
        fragments_module_name="fragments",
        fragments_definitions={
            "TestFragment": parse(
                "fragment TestFragment on CustomType { id }"
            ).definitions[0]
        },
    )

    module = generator.generate()

    assert isinstance(module, ast.Module)
    import_ = filter_imports(module)[-1]
    assert compare_ast(
        import_,
        ast.ImportFrom(module="fragments", names=[ast.alias("TestFragment")], level=1),
    )
