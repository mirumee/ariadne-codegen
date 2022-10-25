import ast

import pytest
from graphql import OperationDefinitionNode, build_ast_schema, parse

from graphql_sdk_gen.generators.constants import LIST, OPTIONAL, ClassType
from graphql_sdk_gen.generators.query_types import QueryTypesGenerator

from ..utils import compare_ast

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

FIELDS: dict[str, dict[str, ast.AnnAssign | ast.Assign]] = {
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
                    bases=[ast.Name(id="BaseModel")],
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
                    bases=[ast.Name(id="BaseModel")],
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
                    bases=[ast.Name(id="BaseModel")],
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
                    bases=[ast.Name(id="BaseModel")],
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
                    bases=[ast.Name(id="BaseModel")],
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
                    bases=[ast.Name(id="BaseModel")],
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
def test_generator_generates_types_from_query(query_str, expected_class_defs):
    operation_definition = parse(query_str).definitions[0]
    assert isinstance(operation_definition, OperationDefinitionNode)

    generator = QueryTypesGenerator(
        build_ast_schema(parse(SCHEMA_STR)),
        FIELDS,
        CLASS_TYPES,
        operation_definition,
        "schema_types",
    )

    assert len(generator.class_defs) == len(expected_class_defs)
    assert compare_ast(generator.class_defs, expected_class_defs)
    assert set(generator.public_names) == {c.name for c in expected_class_defs}


def test_generator_generates_types_from_mutation():
    mutation_str = """
        mutation CustomMutation($num: Int!) {
            mutation1(num: $num) {
                id
            }
        }
    """
    operation_definition = parse(mutation_str).definitions[0]
    assert isinstance(operation_definition, OperationDefinitionNode)

    generator = QueryTypesGenerator(
        build_ast_schema(parse(SCHEMA_STR)),
        FIELDS,
        CLASS_TYPES,
        operation_definition,
        "schema_types",
    )

    expected_class_defs = [
        ast.ClassDef(
            name="CustomMutation",
            bases=[ast.Name(id="BaseModel")],
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
            bases=[ast.Name(id="BaseModel")],
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

    assert len(generator.class_defs) == len(expected_class_defs)
    assert compare_ast(generator.class_defs, expected_class_defs)
    assert set(generator.public_names) == {c.name for c in expected_class_defs}


def test_generator_generates_only_not_duplicated_types_definitions():
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
    operation_definition = parse(query_str).definitions[0]
    assert isinstance(operation_definition, OperationDefinitionNode)

    generator = QueryTypesGenerator(
        build_ast_schema(parse(SCHEMA_STR)),
        FIELDS,
        CLASS_TYPES,
        operation_definition,
        "schema_types",
    )

    expected_class_names = [
        "CustomQuery",
        "CustomQueryCustomType3",
        "CustomQueryCustomType1",
    ]
    generated_class_names = [class_def.name for class_def in generator.class_defs]

    assert len(generated_class_names) == len(expected_class_names)
    assert sorted(generated_class_names) == sorted(expected_class_names)


def test_generate_adds_enum_imports_to_generated_module():
    query_str = """
    query CustomQuery {
        query2 {
            field3
        }
    }
    """
    operation_definition = parse(query_str).definitions[0]
    assert isinstance(operation_definition, OperationDefinitionNode)

    generator = QueryTypesGenerator(
        build_ast_schema(parse(SCHEMA_STR)),
        FIELDS,
        CLASS_TYPES,
        operation_definition,
        "schema_types",
    )
    module = generator.generate()

    assert isinstance(module, ast.Module)
    import_ = list(filter(lambda e: isinstance(e, ast.ImportFrom), module.body))[-1]
    assert compare_ast(
        import_,
        ast.ImportFrom(module="schema_types", names=[ast.alias("CustomEnum")], level=1),
    )


def test_generate_adds_update_forward_refs_calls():
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
    operation_definition = parse(query_str).definitions[0]
    assert isinstance(operation_definition, OperationDefinitionNode)
    expected_class_names = [
        "CustomQuery",
        "CustomQueryCustomType",
        "CustomQueryCustomType1",
        "CustomQueryCustomType2"
    ]
    expected_method_calls = [
        ast.Expr(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id=name), attr="update_forward_refs"),
                args=[],
                keywords=[],
            )
        )
        for name in expected_class_names
    ]
    generator = QueryTypesGenerator(
        build_ast_schema(parse(SCHEMA_STR)),
        FIELDS,
        CLASS_TYPES,
        operation_definition,
        "schema_types",
    )
    module = generator.generate()

    method_calls = list(filter(lambda x: isinstance(x, ast.Expr), module.body))
    assert compare_ast(method_calls, expected_method_calls)
