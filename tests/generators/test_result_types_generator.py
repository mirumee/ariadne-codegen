import ast
from typing import cast

import pytest
from graphql import (
    FragmentDefinitionNode,
    OperationDefinitionNode,
    build_ast_schema,
    parse,
)

from graphql_sdk_gen.generators.constants import (
    BASE_MODEL_CLASS_NAME,
    LIST,
    OPTIONAL,
    UPDATE_FORWARD_REFS_METHOD,
    ClassType,
)
from graphql_sdk_gen.generators.result_types import ResultTypesGenerator

from ..utils import compare_ast, filter_class_defs, format_graphql_str

SCHEMA_STR = """
schema {
  query: Query
  mutation: Mutation
}

type Query {
  query1(
    id: ID!
  ): CustomType

  query2: [CustomType!]

  query3: CustomType3!
}

type Mutation {
    mutation1(num: Int!): CustomType!
}

type CustomType {
    id: ID!
    field1: CustomType1!
    field2: CustomType2
    field3: CustomEnum!
}

type CustomType1 {
    fielda: Int!
}

type CustomType2 {
    fieldb: Int
}

type CustomType3 {
    field1: CustomType1!
    field2: CustomType1!
}

enum CustomEnum {
    VAL1
    VAL2
}
"""

CLASS_TYPES = {
    "CustomType": ClassType.OBJECT,
    "CustomType1": ClassType.OBJECT,
    "CustomType2": ClassType.OBJECT,
    "CustomType3": ClassType.OBJECT,
    "CustomEnum": ClassType.ENUM,
}

FIELDS_IMPLEMENTATIONS: dict[str, dict[str, ast.AnnAssign]] = {
    "CustomType": {
        "id": ast.AnnAssign(
            target=ast.Name(id="id"),
            annotation=ast.Name(id="str"),
            simple=1,
        ),
        "field1": ast.AnnAssign(
            target=ast.Name(id="field1"),
            annotation=ast.Name(id='"CustomType1"'),
            simple=1,
        ),
        "field2": ast.AnnAssign(
            target=ast.Name(id="field2"),
            annotation=ast.Subscript(
                value=ast.Name(id=OPTIONAL), slice=ast.Name(id='"CustomType2"')
            ),
            simple=1,
        ),
        "field3": ast.AnnAssign(
            target=ast.Name(id="field3"),
            annotation=ast.Name(id='"CustomEnum"'),
            simple=1,
        ),
    },
    "CustomType1": {
        "fielda": ast.AnnAssign(
            target=ast.Name(id="fielda"),
            annotation=ast.Name(id="int"),
            simple=1,
        )
    },
    "CustomType2": {
        "fieldb": ast.AnnAssign(
            target=ast.Name(id="fieldb"),
            annotation=ast.Subscript(
                value=ast.Name(id=OPTIONAL), slice=ast.Name(id="int")
            ),
            simple=1,
        )
    },
    "CustomType3": {
        "field1": ast.AnnAssign(
            target=ast.Name(id="field1"),
            annotation=ast.Name(id='"CustomType1"'),
            simple=1,
        ),
        "field2": ast.AnnAssign(
            target=ast.Name(id="field1"),
            annotation=ast.Name(id='"CustomType1"'),
            simple=1,
        ),
    },
}


@pytest.mark.parametrize(
    "query_str, expected_class_defs",
    [
        (
            """
            query CustomQuery {
                query2 {
                    id
                }
            }
            """,
            [
                ast.ClassDef(
                    name="CustomQuery",
                    bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                    decorator_list=[],
                    keywords=[],
                    body=[
                        ast.AnnAssign(
                            target=ast.Name(id="query2"),
                            annotation=ast.Subscript(
                                value=ast.Name(id=OPTIONAL),
                                slice=ast.Subscript(
                                    value=ast.Name(id=LIST),
                                    slice=ast.Name(id='"CustomQueryCustomType"'),
                                ),
                            ),
                            simple=1,
                        )
                    ],
                ),
                ast.ClassDef(
                    name="CustomQueryCustomType",
                    bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                    decorator_list=[],
                    keywords=[],
                    body=[
                        ast.AnnAssign(
                            target=ast.Name(id="id"),
                            annotation=ast.Name(id="str"),
                            simple=1,
                        )
                    ],
                ),
            ],
        ),
        (
            """
            query CustomQuery($id: ID!) {
                query1(id: $id) {
                    field1 {
                        fielda
                    }
                    field2 {
                        fieldb
                    }
                    field3
                }
            }
            """,
            [
                ast.ClassDef(
                    name="CustomQuery",
                    bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                    keywords=[],
                    body=[
                        ast.AnnAssign(
                            target=ast.Name(id="query1"),
                            annotation=ast.Subscript(
                                value=ast.Name(id=OPTIONAL),
                                slice=ast.Name(id='"CustomQueryCustomType"'),
                            ),
                            simple=1,
                        )
                    ],
                    decorator_list=[],
                ),
                ast.ClassDef(
                    name="CustomQueryCustomType",
                    bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                    keywords=[],
                    body=[
                        ast.AnnAssign(
                            target=ast.Name(id="field1"),
                            annotation=ast.Name(id='"CustomQueryCustomType1"'),
                            simple=1,
                        ),
                        ast.AnnAssign(
                            target=ast.Name(id="field2"),
                            annotation=ast.Subscript(
                                value=ast.Name(id=OPTIONAL),
                                slice=ast.Name(id='"CustomQueryCustomType2"'),
                            ),
                            simple=1,
                        ),
                        ast.AnnAssign(
                            target=ast.Name(id="field3"),
                            annotation=ast.Name(id='"CustomEnum"'),
                            simple=1,
                        ),
                    ],
                    decorator_list=[],
                ),
                ast.ClassDef(
                    name="CustomQueryCustomType1",
                    bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                    keywords=[],
                    body=[
                        ast.AnnAssign(
                            target=ast.Name(id="fielda"),
                            annotation=ast.Name(id="int"),
                            simple=1,
                        )
                    ],
                    decorator_list=[],
                ),
                ast.ClassDef(
                    name="CustomQueryCustomType2",
                    bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                    keywords=[],
                    body=[
                        ast.AnnAssign(
                            target=ast.Name(id="fieldb"),
                            annotation=ast.Subscript(
                                value=ast.Name(id=OPTIONAL), slice=ast.Name(id="int")
                            ),
                            simple=1,
                        )
                    ],
                    decorator_list=[],
                ),
            ],
        ),
    ],
)
def test_generate_returns_module_with_generated_result_types_from_query(
    query_str, expected_class_defs
):
    operation_definition = cast(
        OperationDefinitionNode, parse(query_str).definitions[0]
    )
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=operation_definition,
        schema_fields_implementations=FIELDS_IMPLEMENTATIONS,
        class_types=CLASS_TYPES,
        enums_module_name="enums",
    )

    module = generator.generate()

    generated_class_defs = filter_class_defs(module)
    assert len(generated_class_defs) == len(expected_class_defs)
    assert compare_ast(generated_class_defs, expected_class_defs)
    assert set(generator.get_generated_public_names()) == {
        c.name for c in expected_class_defs
    }


def test_generate_returns_module_with_types_generated_from_mutation():
    mutation_str = """
        mutation CustomMutation($num: Int!) {
            mutation1(num: $num) {
                id
            }
        }
    """
    operation_definition = cast(
        OperationDefinitionNode, parse(mutation_str).definitions[0]
    )
    expected_class_defs = [
        ast.ClassDef(
            name="CustomMutation",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            decorator_list=[],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="mutation1"),
                    annotation=ast.Name(id='"CustomMutationCustomType"'),
                    simple=1,
                )
            ],
        ),
        ast.ClassDef(
            name="CustomMutationCustomType",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            decorator_list=[],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="id"),
                    annotation=ast.Name(id="str"),
                    simple=1,
                )
            ],
        ),
    ]
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=operation_definition,
        schema_fields_implementations=FIELDS_IMPLEMENTATIONS,
        class_types=CLASS_TYPES,
        enums_module_name="enums",
    )

    module = generator.generate()

    generated_class_defs = filter_class_defs(module)
    assert len(generated_class_defs) == len(expected_class_defs)
    assert compare_ast(generated_class_defs, expected_class_defs)
    assert set(generator.get_generated_public_names()) == {
        c.name for c in expected_class_defs
    }


def test_generate_returns_module_with_not_duplicated_types_definitions():
    query_str = """
    query CustomQuery {
        query3 {
            field1 {
                fielda
            }
            field2 {
                fielda
            }
        }
    }
    """
    operation_definition = cast(
        OperationDefinitionNode, parse(query_str).definitions[0]
    )
    expected_class_names = [
        "CustomQuery",
        "CustomQueryCustomType3",
        "CustomQueryCustomType1",
    ]
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=operation_definition,
        schema_fields_implementations=FIELDS_IMPLEMENTATIONS,
        class_types=CLASS_TYPES,
        enums_module_name="enums",
    )

    module = generator.generate()

    generated_class_names = [class_def.name for class_def in filter_class_defs(module)]
    assert len(generated_class_names) == len(expected_class_names)
    assert sorted(generated_class_names) == sorted(expected_class_names)


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
        schema_fields_implementations=FIELDS_IMPLEMENTATIONS,
        class_types=CLASS_TYPES,
        enums_module_name="enums",
    )

    module = generator.generate()

    assert isinstance(module, ast.Module)
    import_ = list(filter(lambda e: isinstance(e, ast.ImportFrom), module.body))[-1]
    assert compare_ast(
        import_,
        ast.ImportFrom(module="enums", names=[ast.alias("CustomEnum")], level=1),
    )


def test_generate_returns_module_with_update_forward_refs_calls():
    query_str = """
    query CustomQuery {
        query1 {
            field1 {
                fielda
            }
            field2 {
                fieldb
            }
        }
    }
    """
    operation_definition = cast(
        OperationDefinitionNode, parse(query_str).definitions[0]
    )
    expected_class_names = [
        "CustomQuery",
        "CustomQueryCustomType",
        "CustomQueryCustomType1",
        "CustomQueryCustomType2",
    ]
    expected_method_calls = [
        ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=name), attr=UPDATE_FORWARD_REFS_METHOD
                ),
                args=[],
                keywords=[],
            )
        )
        for name in expected_class_names
    ]
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=operation_definition,
        schema_fields_implementations=FIELDS_IMPLEMENTATIONS,
        class_types=CLASS_TYPES,
        enums_module_name="enums",
    )

    module = generator.generate()

    method_calls = list(filter(lambda x: isinstance(x, ast.Expr), module.body))
    assert compare_ast(method_calls, expected_method_calls)


def test_generate_returns_module_with_types_generated_from_query_that_uses_fragment():
    query_str = """
    query CustomQuery {
        query2 {
            ...TestFragment
            field2 {
                fieldb
            }
        }
    }

    fragment TestFragment on CustomType {
        id
        field1 {
            fielda
        }
    }
    """
    operation_definition, fragment_def = cast(
        tuple[OperationDefinitionNode, FragmentDefinitionNode],
        parse(query_str).definitions,
    )
    expected_class_def = ast.ClassDef(
        name="CustomQueryCustomType",
        bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
        keywords=[],
        body=[
            ast.AnnAssign(
                target=ast.Name(id="id"), annotation=ast.Name(id="str"), simple=1
            ),
            ast.AnnAssign(
                target=ast.Name(id="field1"),
                annotation=ast.Name(id='"CustomQueryCustomType1"'),
                simple=1,
            ),
            ast.AnnAssign(
                target=ast.Name(id="field2"),
                annotation=ast.Subscript(
                    value=ast.Name(id="Optional"),
                    slice=ast.Name(id='"CustomQueryCustomType2"'),
                ),
                simple=1,
            ),
        ],
        decorator_list=[],
    )
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=operation_definition,
        schema_fields_implementations=FIELDS_IMPLEMENTATIONS,
        class_types=CLASS_TYPES,
        enums_module_name="enums",
        fragments_definitions={"TestFragment": fragment_def},
    )

    module = generator.generate()

    class_defs = filter_class_defs(module)
    assert len(class_defs) == 4
    custom_type_class_def = class_defs[1]
    assert custom_type_class_def.name == "CustomQueryCustomType"
    assert compare_ast(custom_type_class_def, expected_class_def)


def test_get_operation_as_str_returns_str_with_used_fragments():
    query_str = format_graphql_str(
        """
        query CustomQuery {
            query2 {
                ...TestFragment1
                ...TestFragment2
                field2 {
                    fieldb
                }
            }
        }
        """
    )

    used_fragment1 = format_graphql_str(
        """
        fragment TestFragment1 on CustomType {
            id
        }
    """
    )

    used_fragment2 = format_graphql_str(
        """
        fragment TestFragment2 on CustomType {
            field1 {
                fielda
            }
        }
        """
    )

    not_used_fragment = format_graphql_str(
        """
        fragment TestFragment3 on CustomType {
            field2 {
                fieldb
            }
        }
        """
    )

    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        schema_fields_implementations=FIELDS_IMPLEMENTATIONS,
        class_types=CLASS_TYPES,
        enums_module_name="enums",
        fragments_definitions={
            "TestFragment1": cast(
                FragmentDefinitionNode, parse(used_fragment1).definitions[0]
            ),
            "TestFragment2": cast(
                FragmentDefinitionNode, parse(used_fragment2).definitions[0]
            ),
            "TestFragment3": cast(
                FragmentDefinitionNode, parse(not_used_fragment).definitions[0]
            ),
        },
    )

    result = generator.get_operation_as_str()

    assert query_str in result
    assert used_fragment1 in result
    assert used_fragment2 in result
    assert not_used_fragment not in result
