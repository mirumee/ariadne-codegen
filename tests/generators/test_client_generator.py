import ast

from graphql_sdk_gen.generators.client import ClientGenerator

from ..utils import compare_ast, get_class_def


def test_generate_returns_module_with_correct_class_name():
    name = "ClientXyz"
    generator = ClientGenerator(name, "BaseClient")

    module = generator.generate()
    class_def = get_class_def(module)

    assert class_def
    assert class_def.name == name


def test_add_import_adds_import_to_generated_module():
    generator = ClientGenerator("Client", "BaseClient")
    name = "Xyz"
    from_ = "xyz"
    number_of_existing_imports = len(generator.imports)
    generator.add_import([name], from_=from_)

    module = generator.generate()
    generated_import = module.body[number_of_existing_imports]

    assert isinstance(generated_import, ast.ImportFrom)
    assert generated_import.module == from_
    assert [n.name for n in generated_import.names] == [name]


def test_add_async_method_adds_method_definition():
    generator = ClientGenerator("Client", "BaseClient")
    method_name = "list_xyz"
    return_type = "ListXyz"
    arguments = ast.arguments(
        posonlyargs=[],
        args=[ast.arg(arg="self")],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[],
    )
    arguments_dict = ast.Dict(keys=[], values=[])

    generator.add_async_method(method_name, return_type, arguments, arguments_dict, "")
    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def
    method_def = class_def.body[0]

    assert isinstance(method_def, ast.AsyncFunctionDef)
    assert method_def.name == method_name
    assert isinstance(method_def.returns, ast.Name)
    assert method_def.returns.id == return_type
    assert method_def.args == arguments


def test_add_async_method_generates_correct_method_body():
    generator = ClientGenerator("Client", "BaseClient")
    method_name = "list_xyz"
    return_type = "ListXyz"
    arguments = ast.arguments(
        posonlyargs=[],
        args=[
            ast.arg(arg="self"),
            ast.arg(arg="arg1", annotation=ast.Name(id="int")),
        ],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[],
    )
    arguments_dict = ast.Dict(
        keys=[ast.Constant(value="arg1")], values=[ast.Name(id="arg1")]
    )
    query_str = """
    query ListXyz($arg1: Int!) {
        xyz(arg1: $arg1) {
            id
            name
        }
    }
    """
    expected_method_body = [
        ast.Assign(
            targets=[ast.Name(id="query")],
            value=ast.Call(
                func=ast.Name("gql"),
                keywords=[],
                args=[[ast.Constant(value=l + "\n") for l in query_str.splitlines()]],
            ),
        ),
        ast.AnnAssign(
            target=ast.Name(id="variables"),
            annotation=ast.Name(id="dict"),
            value=ast.Dict(
                keys=[ast.Constant(value="arg1")], values=[ast.Name(id="arg1")]
            ),
            simple=1,
        ),
        ast.Assign(
            targets=[ast.Name(id="response")],
            value=ast.Await(
                value=ast.Call(
                    func=ast.Attribute(value=ast.Name(id="self"), attr="execute"),
                    args=[],
                    keywords=[
                        ast.keyword(arg="query", value=ast.Name(id="query")),
                        ast.keyword(arg="variables", value=ast.Name(id="variables")),
                    ],
                )
            ),
        ),
        ast.Return(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id="ListXyz"), attr="parse_obj"),
                args=[
                    ast.Call(
                        func=ast.Attribute(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id="response"), attr="json"
                                ),
                                args=[],
                                keywords=[],
                            ),
                            attr="get",
                        ),
                        args=[ast.Constant(value="data"), ast.Dict(keys=[], values=[])],
                        keywords=[],
                    )
                ],
                keywords=[],
            )
        ),
    ]
    generator.add_async_method(
        method_name, return_type, arguments, arguments_dict, query_str
    )
    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def
    method_def = class_def.body[0]
    assert isinstance(method_def, ast.AsyncFunctionDef)
    assert compare_ast(method_def.body, expected_method_body)


def test_generate_returns_module_with_gql_lambda_definition():
    generator = ClientGenerator("ClientXyz", "BaseClient")
    expected_assign = ast.Assign(
        targets=[ast.Name(id="gql")],
        value=ast.Lambda(
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg="q")],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=ast.Name(id="q"),
        ),
    )

    module = generator.generate()

    assign = next(filter(lambda expr: isinstance(expr, ast.Assign), module.body), None)
    assert assign
    assert compare_ast(assign, expected_assign)
