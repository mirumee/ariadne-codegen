import ast
from typing import cast

import pytest
from graphql import (
    FragmentDefinitionNode,
    OperationDefinitionNode,
    build_ast_schema,
    parse,
)

from graphql_sdk_gen.exceptions import ParsingError
from graphql_sdk_gen.generators.constants import (
    BASE_MODEL_CLASS_NAME,
    LIST,
    OPTIONAL,
    UPDATE_FORWARD_REFS_METHOD,
    WITH_MIXIN_NAME,
)
from graphql_sdk_gen.generators.result_types import ResultTypesGenerator

from ..utils import (
    compare_ast,
    filter_class_defs,
    filter_imports,
    format_graphql_str,
    get_class_def,
)

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
  query4: UnionType!
  camelCaseQuery: CustomType!
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

union UnionType = CustomType1 | CustomType2
"""


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
                                    slice=ast.Name(id='"CustomQueryQuery2"'),
                                ),
                            ),
                            simple=1,
                        )
                    ],
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
                                slice=ast.Name(id='"CustomQueryQuery1"'),
                            ),
                            simple=1,
                        )
                    ],
                    decorator_list=[],
                ),
                ast.ClassDef(
                    name="CustomQueryQuery1",
                    bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                    keywords=[],
                    body=[
                        ast.AnnAssign(
                            target=ast.Name(id="field1"),
                            annotation=ast.Name(id='"CustomQueryQuery1Field1"'),
                            simple=1,
                        ),
                        ast.AnnAssign(
                            target=ast.Name(id="field2"),
                            annotation=ast.Subscript(
                                value=ast.Name(id=OPTIONAL),
                                slice=ast.Name(id='"CustomQueryQuery1Field2"'),
                            ),
                            simple=1,
                        ),
                        ast.AnnAssign(
                            target=ast.Name(id="field3"),
                            annotation=ast.Name(id="CustomEnum"),
                            simple=1,
                        ),
                    ],
                    decorator_list=[],
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
                    annotation=ast.Name(id='"CustomMutationMutation1"'),
                    simple=1,
                )
            ],
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
        ),
    ]
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
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
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=operation_definition,
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
        "CustomQueryQuery1",
        "CustomQueryQuery1Field1",
        "CustomQueryQuery1Field2",
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
        name="CustomQueryQuery2",
        bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
        keywords=[],
        body=[
            ast.AnnAssign(
                target=ast.Name(id="id"), annotation=ast.Name(id="str"), simple=1
            ),
            ast.AnnAssign(
                target=ast.Name(id="field1"),
                annotation=ast.Name(id='"CustomQueryQuery2Field1"'),
                simple=1,
            ),
            ast.AnnAssign(
                target=ast.Name(id="field2"),
                annotation=ast.Subscript(
                    value=ast.Name(id="Optional"),
                    slice=ast.Name(id='"CustomQueryQuery2Field2"'),
                ),
                simple=1,
            ),
        ],
        decorator_list=[],
    )
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=operation_definition,
        enums_module_name="enums",
        fragments_definitions={"TestFragment": fragment_def},
    )

    module = generator.generate()

    class_defs = filter_class_defs(module)
    assert len(class_defs) == 4
    custom_type_class_def = class_defs[1]
    assert custom_type_class_def.name == "CustomQueryQuery2"
    assert compare_ast(custom_type_class_def, expected_class_def)


def test_generate_returns_module_with_handled_typename_field():
    query_str = """
    query CustomQuery {
        query2 {
            __typename
            id
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
    expected_fields_implementations = [
        ast.AnnAssign(
            target=ast.Name(id="__typename__"),
            annotation=ast.Name(id="str"),
            value=ast.Call(
                func=ast.Name(id="Field"),
                args=[],
                keywords=[
                    ast.keyword(arg="alias", value=ast.Constant(value="__typename"))
                ],
            ),
            simple=1,
        ),
        ast.AnnAssign(
            target=ast.Name(id="id"),
            annotation=ast.Name(id="str"),
            simple=1,
        ),
    ]

    module = generator.generate()

    class_defs = filter_class_defs(module)
    assert len(class_defs) == 2
    assert class_defs[0].name == "CustomQuery"
    assert class_defs[1].name == "CustomQueryQuery2"
    assert compare_ast(class_defs[1].body, expected_fields_implementations)


def test_generate_returns_module_with_classes_for_union_fields():
    query_str = format_graphql_str(
        """
        query CustomQuery {
            query4 {
                ... on CustomType1 {
                    fielda
                }
                ... on CustomType2 {
                    fieldb
                }
            }
        }
        """
    )
    expected_classes_defs = [
        ast.ClassDef(
            name="CustomQuery",
            bases=[ast.Name(id="BaseModel")],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="query4"),
                    annotation=ast.Subscript(
                        value=ast.Name(id="Union"),
                        slice=ast.Tuple(
                            elts=[
                                ast.Name(id='"CustomQueryQuery4CustomType1"'),
                                ast.Name(id='"CustomQueryQuery4CustomType2"'),
                            ],
                        ),
                    ),
                    simple=1,
                )
            ],
            decorator_list=[],
        ),
        ast.ClassDef(
            name="CustomQueryQuery4CustomType1",
            bases=[ast.Name(id="BaseModel")],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="__typename__"),
                    annotation=ast.Name(id="str"),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg="alias", value=ast.Constant(value="__typename")
                            )
                        ],
                    ),
                    simple=1,
                ),
                ast.AnnAssign(
                    target=ast.Name(id="fielda"),
                    annotation=ast.Name(id="int"),
                    simple=1,
                ),
            ],
            decorator_list=[],
        ),
        ast.ClassDef(
            name="CustomQueryQuery4CustomType2",
            bases=[ast.Name(id="BaseModel")],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="__typename__"),
                    annotation=ast.Name(id="str"),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg="alias", value=ast.Constant(value="__typename")
                            )
                        ],
                    ),
                    simple=1,
                ),
                ast.AnnAssign(
                    target=ast.Name(id="fieldb"),
                    annotation=ast.Subscript(
                        value=ast.Name(id="Optional"),
                        slice=ast.Name(id="int"),
                    ),
                    simple=1,
                ),
            ],
            decorator_list=[],
        ),
    ]

    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
    )

    module = generator.generate()

    class_defs = filter_class_defs(module)
    assert compare_ast(class_defs, expected_classes_defs)


def test_generate_returns_module_with_query_names_converted_to_snake_case():
    query_str = """
    query CustomQuery {
        camelCaseQuery {
            id
        }
    }
    """
    expected_field_implementation = ast.AnnAssign(
        target=ast.Name(id="camel_case_query"),
        annotation=ast.Name(id='"CustomQueryCamelCaseQuery"'),
        value=ast.Call(
            func=ast.Name(id="Field"),
            args=[],
            keywords=[
                ast.keyword(arg="alias", value=ast.Constant(value="camelCaseQuery"))
            ],
        ),
        simple=1,
    )

    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
    )

    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def.name == "CustomQuery"
    assert len(class_def.body) == 1
    field_implementation = class_def.body[0]
    assert compare_ast(field_implementation, expected_field_implementation)


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
            bases=[ast.Name(id="BaseModel")],
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
                    target=ast.Name(id="camel_case_query"),
                    annotation=ast.Name(id='"CustomQueryCamelCaseQuery"'),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg="alias", value=ast.Constant(value="camelCaseQuery")
                            )
                        ],
                    ),
                    simple=1,
                ),
            ],
            decorator_list=[],
        ),
        ast.ClassDef(
            name="CustomQueryQuery1",
            bases=[ast.Name(id="BaseModel")],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="field3"),
                    annotation=ast.Name(id="CustomEnum"),
                    simple=1,
                )
            ],
            decorator_list=[],
        ),
        ast.ClassDef(
            name="CustomQueryCamelCaseQuery",
            bases=[ast.Name(id="BaseModel")],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="id"), annotation=ast.Name(id="str"), simple=1
                )
            ],
            decorator_list=[],
        ),
    ]
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
    )

    module = generator.generate()

    class_defs = filter_class_defs(module)
    assert compare_ast(class_defs, expected_class_defs)


def test_generate_adds_base_class_to_generated_type_provided_by_with_mixin_directive():
    query_str = f"""
    query CustomQuery {{
        camelCaseQuery @{WITH_MIXIN_NAME} (from: ".abcd", class_name: "MixinClass") {{
            id
        }}
    }}
    """
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
    )

    module = generator.generate()

    class_def = get_class_def(module, 1)
    assert class_def.name == "CustomQueryCamelCaseQuery"
    assert [n.id for n in class_def.bases] == [BASE_MODEL_CLASS_NAME, "MixinClass"]
    import_def = filter_imports(module)[-1]
    assert compare_ast(
        import_def,
        ast.ImportFrom(module=".abcd", names=[ast.alias(name="MixinClass")], level=0),
    )


def test_generate_handles_multiple_with_mixin_directives():
    query_str = f"""
    query CustomQuery {{
        camelCaseQuery @{WITH_MIXIN_NAME}(from: ".abcd", class_name: "MixinAbcd") {{
            id
        }}
        query2 @{WITH_MIXIN_NAME}(from: ".xyz", class_name: "MixinXyz") {{
            id
        }}
    }}
    """
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
    )

    module = generator.generate()

    class_def_camel_case = get_class_def(module, 1)
    assert class_def_camel_case.name == "CustomQueryCamelCaseQuery"
    assert [n.id for n in class_def_camel_case.bases] == [
        BASE_MODEL_CLASS_NAME,
        "MixinAbcd",
    ]
    import_def_abcd = filter_imports(module)[-2]
    assert compare_ast(
        import_def_abcd,
        ast.ImportFrom(module=".abcd", names=[ast.alias(name="MixinAbcd")], level=0),
    )
    class_def_query2 = get_class_def(module, 2)
    assert class_def_query2.name == "CustomQueryQuery2"
    assert [n.id for n in class_def_query2.bases] == [
        BASE_MODEL_CLASS_NAME,
        "MixinXyz",
    ]
    import_def_xyz = filter_imports(module)[-1]
    assert compare_ast(
        import_def_xyz,
        ast.ImportFrom(module=".xyz", names=[ast.alias(name="MixinXyz")], level=0),
    )


def test_generate_handles_multiple_with_mixin_directives_on_one_field():
    query_str = f"""
    query CustomQuery {{
        camelCaseQuery
            @{WITH_MIXIN_NAME}(from: ".abcd", class_name: "MixinAbcd")
            @{WITH_MIXIN_NAME}(from: ".xyz", class_name: "MixinXyz") {{
            id
        }}
    }}
    """
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
    )

    module = generator.generate()

    class_def = get_class_def(module, 1)
    assert class_def.name == "CustomQueryCamelCaseQuery"
    assert [n.id for n in class_def.bases] == [
        BASE_MODEL_CLASS_NAME,
        "MixinAbcd",
        "MixinXyz",
    ]
    import_def_abcd = filter_imports(module)[-2]
    assert compare_ast(
        import_def_abcd,
        ast.ImportFrom(module=".abcd", names=[ast.alias(name="MixinAbcd")], level=0),
    )
    import_def_xyz = filter_imports(module)[-1]
    assert compare_ast(
        import_def_xyz,
        ast.ImportFrom(module=".xyz", names=[ast.alias(name="MixinXyz")], level=0),
    )


@pytest.mark.parametrize(
    "arguments",
    [
        'from: ".abcd", class_name: 1',
        'from: 1, class_name: "ClassName"',
        'class_name: "ClassName"',
        'from: ".xyz"',
    ],
)
def test_generator_with_incorrect_data_passed_to_with_mixin_raises_parsing_error(
    arguments,
):
    query_str = f"""
    query CustomQuery {{
        camelCaseQuery @{WITH_MIXIN_NAME}({arguments}) {{
            id
        }}
    }}
    """

    with pytest.raises(ParsingError):
        ResultTypesGenerator(
            schema=build_ast_schema(parse(SCHEMA_STR)),
            operation_definition=cast(
                OperationDefinitionNode, parse(query_str).definitions[0]
            ),
            enums_module_name="enums",
        )


def test_get_operation_as_str_returns_str_with_added_typename():
    query_str = format_graphql_str(
        """
        query CustomQuery {
            query4 {
                ... on CustomType1 {
                    fielda
                }
                ... on CustomType2 {
                    fieldb
                }
            }
        }
        """
    )
    expected_result = format_graphql_str(
        """
        query CustomQuery {
            query4 {
                __typename
                ... on CustomType1 {
                    fielda
                }
                ... on CustomType2 {
                    fieldb
                }
            }
        }
        """
    )
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
    )

    result = generator.get_operation_as_str()

    assert result == expected_result


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
