import ast

from graphql import Undefined, build_schema, print_schema

from ariadne_codegen.graphql_schema_generators.schema import (
    generate_graphql_schema_graphql_file,
    generate_graphql_schema_python_file,
    generate_schema,
    generate_schema_module,
    generate_type_map,
)

from ..utils import compare_ast, filter_ast_objects, filter_imports

SCHEMA_STR = """
    directive @testDirective on FIELD_DEFINITION
    schema {
        query: Query
        mutation: Mutation
        subscription: Subscription
    }
    type Query { _query: String! }
    type Mutation { _mutation: String! }
    type Subscription { _subscription: String! }
    type TypeA { fieldA: Int! }
    input InputB { fieldB: Float! }
    interface InterfaceC { fieldC: Boolean!}
    enum EnumD { D1 D2 }
"""


def test_generate_graphql_schema_graphql_file_creates_file_with_printed_schema(
    tmp_path,
):
    schema = build_schema(SCHEMA_STR)
    file_path = tmp_path / "test_schema.graphql"

    generate_graphql_schema_graphql_file(schema, file_path.as_posix())

    assert file_path.exists()
    assert file_path.is_file()
    with file_path.open() as file_:
        content = file_.read()
        assert content == print_schema(schema)


def test_generate_graphql_schema_python_file_creates_py_file_with_variables(
    tmp_path,
):
    schema = build_schema(SCHEMA_STR)
    file_path = tmp_path / "test_schema.py"

    generate_graphql_schema_python_file(
        schema, file_path.as_posix(), "type_map", "schema"
    )

    assert file_path.exists()
    assert file_path.is_file()
    with file_path.open() as file_:
        content = file_.read()
        assert "type_map: TypeMap = " in content
        assert "schema: GraphQLSchema = " in content


def test_generate_schema_module_returns_module_with_schema_and_type_map_variables():
    schema = build_schema(SCHEMA_STR)

    module = generate_schema_module(
        schema, type_map_name="type_map", schema_variable_name="schema"
    )

    assigns = filter_ast_objects(module, ast.AnnAssign)
    assert len(assigns) == 2
    type_map_assign, schema_assign = assigns
    assert compare_ast(type_map_assign.target, ast.Name("type_map"))
    assert compare_ast(type_map_assign.annotation, ast.Name("TypeMap"))
    assert compare_ast(schema_assign.target, ast.Name("schema"))
    assert compare_ast(schema_assign.annotation, ast.Name("GraphQLSchema"))


def test_generate_schema_module_returns_module_with_necessary_imports():
    schema = build_schema(SCHEMA_STR)

    module = generate_schema_module(
        schema, type_map_name="type_map", schema_variable_name="schema"
    )

    imports = filter_imports(module)
    assert len(imports) == 3
    graphql_import, type_map_import, typing_import = imports
    assert graphql_import.module == "graphql"
    assert {alias.name for alias in graphql_import.names} == {
        "DirectiveLocation",
        "GraphQLArgument",
        "GraphQLDirective",
        "GraphQLEnumType",
        "GraphQLEnumValue",
        "GraphQLField",
        "GraphQLInputField",
        "GraphQLInputObjectType",
        "GraphQLInterfaceType",
        "GraphQLList",
        "GraphQLNamedType",
        "GraphQLNonNull",
        "GraphQLObjectType",
        "GraphQLScalarType",
        "GraphQLSchema",
        "GraphQLUnionType",
        "GraphQLID",
        "GraphQLInt",
        "GraphQLFloat",
        "GraphQLString",
        "GraphQLBoolean",
        "Undefined",
    }
    assert type_map_import.module == "graphql.type.schema"
    assert len(type_map_import.names) == 1
    assert compare_ast(type_map_import.names[0], ast.alias("TypeMap"))
    assert typing_import.module == "typing"
    assert {alias.name for alias in typing_import.names} == {"cast", "List"}


def test_generate_type_map_returns_ast_dict():
    schema = build_schema(SCHEMA_STR)
    expected_ast = ast.Dict(
        keys=[
            ast.Constant(value="Query"),
            ast.Constant(value="Mutation"),
            ast.Constant(value="Subscription"),
            ast.Constant(value="TypeA"),
            ast.Constant(value="InputB"),
            ast.Constant(value="InterfaceC"),
            ast.Constant(value="EnumD"),
        ],
        values=[
            ast.Call(
                func=ast.Name(id="GraphQLObjectType"),
                args=[],
                keywords=[
                    ast.keyword(arg="name", value=ast.Constant(value="Query")),
                    ast.keyword(arg="description", value=ast.Constant(value=None)),
                    ast.keyword(arg="interfaces", value=ast.Constant(value=[])),
                    ast.keyword(
                        arg="fields",
                        value=ast.Lambda(
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[],
                            ),
                            body=ast.Dict(
                                keys=[ast.Constant(value="_query")],
                                values=[
                                    ast.Call(
                                        func=ast.Name(id="GraphQLField"),
                                        args=[
                                            ast.Call(
                                                func=ast.Name(id="GraphQLNonNull"),
                                                args=[ast.Name(id="GraphQLString")],
                                                keywords=[],
                                            )
                                        ],
                                        keywords=[
                                            ast.keyword(
                                                arg="args",
                                                value=ast.Dict(keys=[], values=[]),
                                            ),
                                            ast.keyword(
                                                arg="description",
                                                value=ast.Constant(value=None),
                                            ),
                                            ast.keyword(
                                                arg="deprecation_reason",
                                                value=ast.Constant(value=None),
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ),
                    ),
                ],
            ),
            ast.Call(
                func=ast.Name(id="GraphQLObjectType"),
                args=[],
                keywords=[
                    ast.keyword(arg="name", value=ast.Constant(value="Mutation")),
                    ast.keyword(arg="description", value=ast.Constant(value=None)),
                    ast.keyword(arg="interfaces", value=ast.Constant(value=[])),
                    ast.keyword(
                        arg="fields",
                        value=ast.Lambda(
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[],
                            ),
                            body=ast.Dict(
                                keys=[ast.Constant(value="_mutation")],
                                values=[
                                    ast.Call(
                                        func=ast.Name(id="GraphQLField"),
                                        args=[
                                            ast.Call(
                                                func=ast.Name(id="GraphQLNonNull"),
                                                args=[ast.Name(id="GraphQLString")],
                                                keywords=[],
                                            )
                                        ],
                                        keywords=[
                                            ast.keyword(
                                                arg="args",
                                                value=ast.Dict(keys=[], values=[]),
                                            ),
                                            ast.keyword(
                                                arg="description",
                                                value=ast.Constant(value=None),
                                            ),
                                            ast.keyword(
                                                arg="deprecation_reason",
                                                value=ast.Constant(value=None),
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ),
                    ),
                ],
            ),
            ast.Call(
                func=ast.Name(id="GraphQLObjectType"),
                args=[],
                keywords=[
                    ast.keyword(arg="name", value=ast.Constant(value="Subscription")),
                    ast.keyword(arg="description", value=ast.Constant(value=None)),
                    ast.keyword(arg="interfaces", value=ast.Constant(value=[])),
                    ast.keyword(
                        arg="fields",
                        value=ast.Lambda(
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[],
                            ),
                            body=ast.Dict(
                                keys=[ast.Constant(value="_subscription")],
                                values=[
                                    ast.Call(
                                        func=ast.Name(id="GraphQLField"),
                                        args=[
                                            ast.Call(
                                                func=ast.Name(id="GraphQLNonNull"),
                                                args=[ast.Name(id="GraphQLString")],
                                                keywords=[],
                                            )
                                        ],
                                        keywords=[
                                            ast.keyword(
                                                arg="args",
                                                value=ast.Dict(keys=[], values=[]),
                                            ),
                                            ast.keyword(
                                                arg="description",
                                                value=ast.Constant(value=None),
                                            ),
                                            ast.keyword(
                                                arg="deprecation_reason",
                                                value=ast.Constant(value=None),
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ),
                    ),
                ],
            ),
            ast.Call(
                func=ast.Name(id="GraphQLObjectType"),
                args=[],
                keywords=[
                    ast.keyword(arg="name", value=ast.Constant(value="TypeA")),
                    ast.keyword(arg="description", value=ast.Constant(value=None)),
                    ast.keyword(arg="interfaces", value=ast.Constant(value=[])),
                    ast.keyword(
                        arg="fields",
                        value=ast.Lambda(
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[],
                            ),
                            body=ast.Dict(
                                keys=[ast.Constant(value="fieldA")],
                                values=[
                                    ast.Call(
                                        func=ast.Name(id="GraphQLField"),
                                        args=[
                                            ast.Call(
                                                func=ast.Name(id="GraphQLNonNull"),
                                                args=[ast.Name(id="GraphQLInt")],
                                                keywords=[],
                                            )
                                        ],
                                        keywords=[
                                            ast.keyword(
                                                arg="args",
                                                value=ast.Dict(keys=[], values=[]),
                                            ),
                                            ast.keyword(
                                                arg="description",
                                                value=ast.Constant(value=None),
                                            ),
                                            ast.keyword(
                                                arg="deprecation_reason",
                                                value=ast.Constant(value=None),
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ),
                    ),
                ],
            ),
            ast.Call(
                func=ast.Name(id="GraphQLInputObjectType"),
                args=[],
                keywords=[
                    ast.keyword(arg="name", value=ast.Constant(value="InputB")),
                    ast.keyword(arg="description", value=ast.Constant(value=None)),
                    ast.keyword(
                        arg="fields",
                        value=ast.Lambda(
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[],
                            ),
                            body=ast.Dict(
                                keys=[ast.Constant(value="fieldB")],
                                values=[
                                    ast.Call(
                                        func=ast.Name(id="GraphQLInputField"),
                                        args=[
                                            ast.Call(
                                                func=ast.Name(id="GraphQLNonNull"),
                                                args=[ast.Name(id="GraphQLFloat")],
                                                keywords=[],
                                            )
                                        ],
                                        keywords=[
                                            ast.keyword(
                                                arg="default_value",
                                                value=ast.Constant(value=Undefined),
                                            ),
                                            ast.keyword(
                                                arg="description",
                                                value=ast.Constant(value=None),
                                            ),
                                            ast.keyword(
                                                arg="deprecation_reason",
                                                value=ast.Constant(value=None),
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ),
                    ),
                ],
            ),
            ast.Call(
                func=ast.Name(id="GraphQLInterfaceType"),
                args=[],
                keywords=[
                    ast.keyword(arg="name", value=ast.Constant(value="InterfaceC")),
                    ast.keyword(arg="description", value=ast.Constant(value=None)),
                    ast.keyword(arg="interfaces", value=ast.Constant(value=[])),
                    ast.keyword(
                        arg="fields",
                        value=ast.Lambda(
                            args=ast.arguments(
                                posonlyargs=[],
                                args=[],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[],
                            ),
                            body=ast.Dict(
                                keys=[ast.Constant(value="fieldC")],
                                values=[
                                    ast.Call(
                                        func=ast.Name(id="GraphQLField"),
                                        args=[
                                            ast.Call(
                                                func=ast.Name(id="GraphQLNonNull"),
                                                args=[ast.Name(id="GraphQLBoolean")],
                                                keywords=[],
                                            )
                                        ],
                                        keywords=[
                                            ast.keyword(
                                                arg="args",
                                                value=ast.Dict(keys=[], values=[]),
                                            ),
                                            ast.keyword(
                                                arg="description",
                                                value=ast.Constant(value=None),
                                            ),
                                            ast.keyword(
                                                arg="deprecation_reason",
                                                value=ast.Constant(value=None),
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ),
                    ),
                ],
            ),
            ast.Call(
                func=ast.Name(id="GraphQLEnumType"),
                args=[],
                keywords=[
                    ast.keyword(arg="name", value=ast.Constant(value="EnumD")),
                    ast.keyword(arg="description", value=ast.Constant(value=None)),
                    ast.keyword(
                        arg="values",
                        value=ast.Dict(
                            keys=[ast.Constant(value="D1"), ast.Constant(value="D2")],
                            values=[
                                ast.Call(
                                    func=ast.Name(id="GraphQLEnumValue"),
                                    args=[],
                                    keywords=[
                                        ast.keyword(
                                            arg="value", value=ast.Constant(value="D1")
                                        ),
                                        ast.keyword(
                                            arg="description",
                                            value=ast.Constant(value=None),
                                        ),
                                        ast.keyword(
                                            arg="deprecation_reason",
                                            value=ast.Constant(value=None),
                                        ),
                                    ],
                                ),
                                ast.Call(
                                    func=ast.Name(id="GraphQLEnumValue"),
                                    args=[],
                                    keywords=[
                                        ast.keyword(
                                            arg="value", value=ast.Constant(value="D2")
                                        ),
                                        ast.keyword(
                                            arg="description",
                                            value=ast.Constant(value=None),
                                        ),
                                        ast.keyword(
                                            arg="deprecation_reason",
                                            value=ast.Constant(value=None),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )

    assert compare_ast(generate_type_map(schema.type_map, "type_map"), expected_ast)


def test_generate_schema_returns_ast_call():
    schema = build_schema(SCHEMA_STR)
    schema.directives = schema.directives[:1]
    expected_ast = ast.Call(
        func=ast.Name(id="GraphQLSchema"),
        args=[],
        keywords=[
            ast.keyword(
                arg="query",
                value=ast.Call(
                    func=ast.Name(id="cast"),
                    args=[
                        ast.Name(id="GraphQLObjectType"),
                        ast.Subscript(
                            value=ast.Name(id="type_map"),
                            slice=ast.Constant(value="Query"),
                        ),
                    ],
                    keywords=[],
                ),
            ),
            ast.keyword(
                arg="mutation",
                value=ast.Call(
                    func=ast.Name(id="cast"),
                    args=[
                        ast.Name(id="GraphQLObjectType"),
                        ast.Subscript(
                            value=ast.Name(id="type_map"),
                            slice=ast.Constant(value="Mutation"),
                        ),
                    ],
                    keywords=[],
                ),
            ),
            ast.keyword(
                arg="subscription",
                value=ast.Call(
                    func=ast.Name(id="cast"),
                    args=[
                        ast.Name(id="GraphQLObjectType"),
                        ast.Subscript(
                            value=ast.Name(id="type_map"),
                            slice=ast.Constant(value="Subscription"),
                        ),
                    ],
                    keywords=[],
                ),
            ),
            ast.keyword(
                arg="types",
                value=ast.Call(
                    func=ast.Attribute(value=ast.Name(id="type_map"), attr="values"),
                    args=[],
                    keywords=[],
                ),
            ),
            ast.keyword(
                arg="directives",
                value=ast.List(
                    elts=[
                        ast.Call(
                            func=ast.Name(id="GraphQLDirective"),
                            args=[],
                            keywords=[
                                ast.keyword(
                                    arg="name",
                                    value=ast.Constant(value="testDirective"),
                                ),
                                ast.keyword(
                                    arg="description", value=ast.Constant(value=None)
                                ),
                                ast.keyword(
                                    arg="is_repeatable", value=ast.Constant(value=False)
                                ),
                                ast.keyword(
                                    arg="locations",
                                    value=ast.Tuple(
                                        elts=[
                                            ast.Attribute(
                                                value=ast.Name(id="DirectiveLocation"),
                                                attr="FIELD_DEFINITION",
                                            )
                                        ]
                                    ),
                                ),
                                ast.keyword(arg="args", value=ast.Constant(value=None)),
                            ],
                        )
                    ]
                ),
            ),
            ast.keyword(arg="description", value=ast.Constant(value=None)),
        ],
    )

    assert compare_ast(generate_schema(schema, "type_map"), expected_ast)
