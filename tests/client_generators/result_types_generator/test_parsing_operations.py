import ast
from typing import Tuple, cast

import pytest
from graphql import FragmentDefinitionNode, OperationDefinitionNode, build_schema, parse

from ariadne_codegen.client_generators.constants import (
    ALIAS_KEYWORD,
    BASE_MODEL_CLASS_NAME,
    DISCRIMINATOR_KEYWORD,
    FIELD_CLASS,
    LIST,
    LITERAL,
    OPTIONAL,
    TYPENAME_ALIAS,
    TYPENAME_FIELD_NAME,
    UNION,
)
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

from ...utils import compare_ast, filter_class_defs
from .schema import SCHEMA_STR


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
                            target=ast.Name(id="query_2"),
                            annotation=ast.Subscript(
                                value=ast.Name(id=OPTIONAL),
                                slice=ast.Subscript(
                                    value=ast.Name(id=LIST),
                                    slice=ast.Name(id='"CustomQueryQuery2"'),
                                ),
                            ),
                            value=ast.Call(
                                func=ast.Name(id=FIELD_CLASS),
                                args=[],
                                keywords=[
                                    ast.keyword(
                                        arg=ALIAS_KEYWORD,
                                        value=ast.Constant(value="query2"),
                                    )
                                ],
                            ),
                            simple=1,
                        )
                    ],
                    type_params=[],
                ),
                ast.ClassDef(
                    name="CustomQueryQuery2",
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
                    type_params=[],
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
                            target=ast.Name(id="query_1"),
                            annotation=ast.Subscript(
                                value=ast.Name(id=OPTIONAL),
                                slice=ast.Name(id='"CustomQueryQuery1"'),
                            ),
                            value=ast.Call(
                                func=ast.Name(id=FIELD_CLASS),
                                args=[],
                                keywords=[
                                    ast.keyword(
                                        arg=ALIAS_KEYWORD,
                                        value=ast.Constant(value="query1"),
                                    )
                                ],
                            ),
                            simple=1,
                        )
                    ],
                    decorator_list=[],
                    type_params=[],
                ),
                ast.ClassDef(
                    name="CustomQueryQuery1",
                    bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                    keywords=[],
                    body=[
                        ast.AnnAssign(
                            target=ast.Name(id="field_1"),
                            annotation=ast.Name(id='"CustomQueryQuery1Field1"'),
                            value=ast.Call(
                                func=ast.Name(id=FIELD_CLASS),
                                args=[],
                                keywords=[
                                    ast.keyword(
                                        arg=ALIAS_KEYWORD,
                                        value=ast.Constant(value="field1"),
                                    )
                                ],
                            ),
                            simple=1,
                        ),
                        ast.AnnAssign(
                            target=ast.Name(id="field_2"),
                            annotation=ast.Subscript(
                                value=ast.Name(id=OPTIONAL),
                                slice=ast.Name(id='"CustomQueryQuery1Field2"'),
                            ),
                            value=ast.Call(
                                func=ast.Name(id=FIELD_CLASS),
                                args=[],
                                keywords=[
                                    ast.keyword(
                                        arg=ALIAS_KEYWORD,
                                        value=ast.Constant(value="field2"),
                                    )
                                ],
                            ),
                            simple=1,
                        ),
                        ast.AnnAssign(
                            target=ast.Name(id="field_3"),
                            annotation=ast.Name(id="CustomEnum"),
                            value=ast.Call(
                                func=ast.Name(id=FIELD_CLASS),
                                args=[],
                                keywords=[
                                    ast.keyword(
                                        arg=ALIAS_KEYWORD,
                                        value=ast.Constant(value="field3"),
                                    )
                                ],
                            ),
                            simple=1,
                        ),
                    ],
                    decorator_list=[],
                    type_params=[],
                ),
                ast.ClassDef(
                    name="CustomQueryQuery1Field1",
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
                    type_params=[],
                ),
                ast.ClassDef(
                    name="CustomQueryQuery1Field2",
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
                    type_params=[],
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
        schema=build_schema(SCHEMA_STR),
        operation_definition=operation_definition,
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
                    target=ast.Name(id="mutation_1"),
                    annotation=ast.Name(id='"CustomMutationMutation1"'),
                    value=ast.Call(
                        func=ast.Name(id=FIELD_CLASS),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg=ALIAS_KEYWORD,
                                value=ast.Constant(value="mutation1"),
                            )
                        ],
                    ),
                    simple=1,
                )
            ],
            type_params=[],
        ),
        ast.ClassDef(
            name="CustomMutationMutation1",
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
            type_params=[],
        ),
    ]
    generator = ResultTypesGenerator(
        schema=build_schema(SCHEMA_STR),
        operation_definition=operation_definition,
        enums_module_name="enums",
    )

    module = generator.generate()

    generated_class_defs = filter_class_defs(module)
    assert len(generated_class_defs) == len(expected_class_defs)
    assert compare_ast(generated_class_defs, expected_class_defs)
    assert set(generator.get_generated_public_names()) == {
        c.name for c in expected_class_defs
    }


def test_generate_returns_module_with_types_generated_from_subscription():
    mutation_str = """
        subscription CustomSubscription($num: Int!) {
            subscription1(num: $num) {
                id
            }
        }
    """
    operation_definition = cast(
        OperationDefinitionNode, parse(mutation_str).definitions[0]
    )
    expected_class_defs = [
        ast.ClassDef(
            name="CustomSubscription",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            decorator_list=[],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="subscription_1"),
                    annotation=ast.Name(id='"CustomSubscriptionSubscription1"'),
                    value=ast.Call(
                        func=ast.Name(id=FIELD_CLASS),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg=ALIAS_KEYWORD,
                                value=ast.Constant(value="subscription1"),
                            )
                        ],
                    ),
                    simple=1,
                )
            ],
            type_params=[],
        ),
        ast.ClassDef(
            name="CustomSubscriptionSubscription1",
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
            type_params=[],
        ),
    ]
    generator = ResultTypesGenerator(
        schema=build_schema(SCHEMA_STR),
        operation_definition=operation_definition,
        enums_module_name="enums",
    )

    module = generator.generate()

    generated_class_defs = filter_class_defs(module)
    assert len(generated_class_defs) == len(expected_class_defs)
    assert compare_ast(generated_class_defs, expected_class_defs)
    assert set(generator.get_generated_public_names()) == {
        c.name for c in expected_class_defs
    }


def test_generate_returns_module_with_class_per_every_field():
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
        "CustomQueryQuery3",
        "CustomQueryQuery3Field1",
        "CustomQueryQuery3Field2",
    ]
    generator = ResultTypesGenerator(
        schema=build_schema(SCHEMA_STR),
        operation_definition=operation_definition,
        enums_module_name="enums",
    )

    module = generator.generate()

    generated_class_names = [class_def.name for class_def in filter_class_defs(module)]
    assert len(generated_class_names) == len(expected_class_names)
    assert sorted(generated_class_names) == sorted(expected_class_names)


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
        Tuple[OperationDefinitionNode, FragmentDefinitionNode],
        parse(query_str).definitions,
    )
    expected_class_def = ast.ClassDef(
        name="CustomQueryQuery2",
        bases=[ast.Name(id="TestFragment")],
        keywords=[],
        body=[
            ast.AnnAssign(
                target=ast.Name(id="field_2"),
                annotation=ast.Subscript(
                    value=ast.Name(id="Optional"),
                    slice=ast.Name(id='"CustomQueryQuery2Field2"'),
                ),
                value=ast.Call(
                    func=ast.Name(id=FIELD_CLASS),
                    args=[],
                    keywords=[
                        ast.keyword(
                            arg=ALIAS_KEYWORD,
                            value=ast.Constant(value="field2"),
                        )
                    ],
                ),
                simple=1,
            ),
        ],
        decorator_list=[],
        type_params=[],
    )
    generator = ResultTypesGenerator(
        schema=build_schema(SCHEMA_STR),
        operation_definition=operation_definition,
        enums_module_name="enums",
        fragments_definitions={"TestFragment": fragment_def},
    )

    module = generator.generate()

    class_defs = filter_class_defs(module)
    assert len(class_defs) == 3
    custom_type_class_def = class_defs[1]
    assert custom_type_class_def.name == "CustomQueryQuery2"
    assert compare_ast(custom_type_class_def, expected_class_def)


def test_generate_returns_module_with_class_with_union_from_unpacked_fragment():
    query_str = """
    query CustomQuery {
        interfaceQuery {
            ...InterfaceIFragment
        }
    }

    fragment InterfaceIFragment on InterfaceI {
        id
        ... on TypeA {
            fieldA
        }
        ... on TypeB {
            fieldB
        }
    }
    """
    expected_class_defs = [
        ast.ClassDef(
            name="CustomQuery",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="interface_query"),
                    annotation=ast.Subscript(
                        value=ast.Name(id=UNION),
                        slice=ast.Tuple(
                            elts=[
                                ast.Name(id='"CustomQueryInterfaceQueryInterfaceI"'),
                                ast.Name(id='"CustomQueryInterfaceQueryTypeA"'),
                                ast.Name(id='"CustomQueryInterfaceQueryTypeB"'),
                            ]
                        ),
                    ),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg=ALIAS_KEYWORD,
                                value=ast.Constant(value="interfaceQuery"),
                            ),
                            ast.keyword(
                                arg=DISCRIMINATOR_KEYWORD,
                                value=ast.Constant(value=TYPENAME_ALIAS),
                            ),
                        ],
                    ),
                    simple=1,
                )
            ],
            decorator_list=[],
            type_params=[],
        ),
        ast.ClassDef(
            name="CustomQueryInterfaceQueryInterfaceI",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id=TYPENAME_ALIAS),
                    annotation=ast.Subscript(
                        value=ast.Name(LITERAL),
                        slice=ast.Tuple(
                            elts=[ast.Name('"InterfaceI"'), ast.Name('"TypeC"')]
                        ),
                    ),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg=ALIAS_KEYWORD,
                                value=ast.Constant(value=TYPENAME_FIELD_NAME),
                            )
                        ],
                    ),
                    simple=1,
                ),
                ast.AnnAssign(
                    target=ast.Name(id="id"),
                    annotation=ast.Name(id="str"),
                    simple=1,
                ),
            ],
            decorator_list=[],
            type_params=[],
        ),
        ast.ClassDef(
            name="CustomQueryInterfaceQueryTypeA",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id=TYPENAME_ALIAS),
                    annotation=ast.Subscript(
                        value=ast.Name(LITERAL), slice=ast.Name('"TypeA"')
                    ),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg=ALIAS_KEYWORD,
                                value=ast.Constant(value=TYPENAME_FIELD_NAME),
                            )
                        ],
                    ),
                    simple=1,
                ),
                ast.AnnAssign(
                    target=ast.Name(id="id"),
                    annotation=ast.Name(id="str"),
                    simple=1,
                ),
                ast.AnnAssign(
                    target=ast.Name(id="field_a"),
                    annotation=ast.Name(id="str"),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg=ALIAS_KEYWORD, value=ast.Constant(value="fieldA")
                            )
                        ],
                    ),
                    simple=1,
                ),
            ],
            decorator_list=[],
            type_params=[],
        ),
        ast.ClassDef(
            name="CustomQueryInterfaceQueryTypeB",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id=TYPENAME_ALIAS),
                    annotation=ast.Subscript(
                        value=ast.Name(LITERAL), slice=ast.Name('"TypeB"')
                    ),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg=ALIAS_KEYWORD,
                                value=ast.Constant(value=TYPENAME_FIELD_NAME),
                            )
                        ],
                    ),
                    simple=1,
                ),
                ast.AnnAssign(
                    target=ast.Name(id="id"),
                    annotation=ast.Name(id="str"),
                    simple=1,
                ),
                ast.AnnAssign(
                    target=ast.Name(id="field_b"),
                    annotation=ast.Name(id="float"),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg=ALIAS_KEYWORD, value=ast.Constant(value="fieldB")
                            )
                        ],
                    ),
                    simple=1,
                ),
            ],
            decorator_list=[],
            type_params=[],
        ),
    ]
    operation_definition, fragment_def = cast(
        Tuple[OperationDefinitionNode, FragmentDefinitionNode],
        parse(query_str).definitions,
    )
    generator = ResultTypesGenerator(
        schema=build_schema(SCHEMA_STR),
        operation_definition=operation_definition,
        enums_module_name="enums",
        fragments_definitions={"InterfaceIFragment": fragment_def},
    )

    module = generator.generate()

    class_defs = filter_class_defs(module)
    assert compare_ast(class_defs, expected_class_defs)
    assert generator.get_unpacked_fragments() == {"InterfaceIFragment"}


def test_generate_returns_module_with_class_for_every_appearance_of_type():
    query_str = """
    query CustomQuery($id: ID!) {
        query1(id: $id){
            field3
        }
        camelCaseQuery {
            id
        }
    }
    """
    expected_class_defs = [
        ast.ClassDef(
            name="CustomQuery",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="query1"),
                    annotation=ast.Subscript(
                        value=ast.Name(id="Optional"),
                        slice=ast.Name(id='"CustomQueryQuery1"'),
                    ),
                    simple=1,
                ),
                ast.AnnAssign(
                    target=ast.Name(id="camelCaseQuery"),
                    annotation=ast.Name(id='"CustomQueryCamelCaseQuery"'),
                    simple=1,
                ),
            ],
            decorator_list=[],
            type_params=[],
        ),
        ast.ClassDef(
            name="CustomQueryQuery1",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="field3"),
                    annotation=ast.Name(id="CustomEnum"),
                    simple=1,
                )
            ],
            decorator_list=[],
            type_params=[],
        ),
        ast.ClassDef(
            name="CustomQueryCamelCaseQuery",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="id"), annotation=ast.Name(id="str"), simple=1
                )
            ],
            decorator_list=[],
            type_params=[],
        ),
    ]
    generator = ResultTypesGenerator(
        schema=build_schema(SCHEMA_STR),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        convert_to_snake_case=False,
    )

    module = generator.generate()

    class_defs = filter_class_defs(module)
    assert compare_ast(class_defs, expected_class_defs)


@pytest.mark.parametrize(
    "operation_str, expected_class_def",
    [
        (
            "query TestQuery { testQ }",
            ast.ClassDef(
                name="TestQuery",
                bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                decorator_list=[],
                keywords=[],
                body=[
                    ast.AnnAssign(
                        target=ast.Name(id="testQ"),
                        annotation=ast.Name(id="str"),
                        simple=1,
                    )
                ],
                type_params=[],
            ),
        ),
        (
            "mutation TestMutation { testM }",
            ast.ClassDef(
                name="TestMutation",
                bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                decorator_list=[],
                keywords=[],
                body=[
                    ast.AnnAssign(
                        target=ast.Name(id="testM"),
                        annotation=ast.Name(id="str"),
                        simple=1,
                    )
                ],
                type_params=[],
            ),
        ),
    ],
)
def test_generate_returns_module_for_schema_with_custom_operation_type_name(
    operation_str, expected_class_def
):
    schema_str = """
    schema {
        query: CustomQueryType
        mutation: CustomMutationType
    }
    type CustomQueryType { testQ: String! }
    type CustomMutationType { testM: String! }
    """
    generator = ResultTypesGenerator(
        schema=build_schema(schema_str),
        operation_definition=cast(
            OperationDefinitionNode, parse(operation_str).definitions[0]
        ),
        enums_module_name="enums",
        convert_to_snake_case=False,
    )

    module = generator.generate()

    assert isinstance(module, ast.Module)
    class_defs = filter_class_defs(module)
    assert len(class_defs) == 1
    assert compare_ast(class_defs[0], expected_class_def)
