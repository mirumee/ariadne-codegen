import ast

from ariadne_codegen.client_generators.client import ClientGenerator

from ..utils import compare_ast, filter_imports, get_class_def


def test_generate_returns_module_with_correct_class_name():
    name = "ClientXyz"
    generator = ClientGenerator(name, "BaseClient")

    module = generator.generate()
    class_def = get_class_def(module)

    assert class_def
    assert class_def.name == name


def test_generate_returns_module_with_gql_lambda_definition():
    generator = ClientGenerator("ClientXyz", "BaseClient")
    expected_def = ast.FunctionDef(
        name="gql",
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg="q", annotation=ast.Name(id="str"))],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[ast.Return(value=ast.Name(id="q"))],
        returns=ast.Name(id="str"),
        decorator_list=[],
    )

    module = generator.generate()

    assign = next(
        filter(lambda expr: isinstance(expr, ast.FunctionDef), module.body), None
    )
    assert assign
    assert compare_ast(assign, expected_def)


def test_generate_triggers_generate_gql_function_hook(mocker):
    mocked_plugin_manager = mocker.MagicMock()
    generator = ClientGenerator(
        "ClientXyz", "BaseClient", plugin_manager=mocked_plugin_manager
    )

    generator.generate()

    assert mocked_plugin_manager.generate_gql_function.called


def test_generate_triggers_generate_client_class_hook(mocker):
    mocked_plugin_manager = mocker.MagicMock()
    generator = ClientGenerator(
        "ClientXyz", "BaseClient", plugin_manager=mocked_plugin_manager
    )

    generator.generate()

    assert mocked_plugin_manager.generate_client_class.called


def test_generate_triggers_generate_client_module_hook(mocker):
    mocked_plugin_manager = mocker.MagicMock()
    generator = ClientGenerator(
        "ClientXyz", "BaseClient", plugin_manager=mocked_plugin_manager
    )

    generator.generate()

    assert mocked_plugin_manager.generate_client_module.called


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


def test_add_import_with_empty_names_list_doesnt_add_invalid_import():
    generator = ClientGenerator("Client", "BaseClient")
    number_of_pre_existing_imports = len(generator.imports)

    generator.add_import([], from_="abc")
    module = generator.generate()

    imports = filter_imports(module)
    assert len(imports) == number_of_pre_existing_imports


def test_add_import_triggers_generate_client_import_hook(mocker):
    mocked_plugin_manager = mocker.MagicMock()
    generator = ClientGenerator(
        "ClientXyz", "BaseClient", plugin_manager=mocked_plugin_manager
    )

    generator.add_import(["TestType"], "test", level=1)

    assert mocked_plugin_manager.generate_client_import.called


def test_add_method_adds_async_method_definition():
    generator = ClientGenerator("Client", "AsyncBaseClient")
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

    generator.add_method(
        name=method_name,
        return_type=return_type,
        arguments=arguments,
        arguments_dict=arguments_dict,
        operation_str="",
        async_=True,
    )
    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def
    method_def = class_def.body[0]

    assert isinstance(method_def, ast.AsyncFunctionDef)
    assert method_def.name == method_name
    assert isinstance(method_def.returns, ast.Name)
    assert method_def.returns.id == return_type
    assert method_def.args == arguments


def test_add_method_generates_correct_async_method_body():
    generator = ClientGenerator("Client", "AsyncBaseClient")
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
            annotation=ast.Subscript(
                value=ast.Name(id="dict"),
                slice=ast.Tuple(elts=[ast.Name(id="str"), ast.Name(id="object")]),
            ),
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
        ast.Assign(
            targets=[ast.Name(id="data")],
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id="self"), attr="get_data"),
                args=[ast.Name(id="response")],
                keywords=[],
            ),
        ),
        ast.Return(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id="ListXyz"), attr="parse_obj"),
                args=[ast.Name(id="data")],
                keywords=[],
            )
        ),
    ]

    generator.add_method(
        name=method_name,
        return_type=return_type,
        arguments=arguments,
        arguments_dict=arguments_dict,
        operation_str=query_str,
        async_=True,
    )
    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def
    method_def = class_def.body[0]
    assert isinstance(method_def, ast.AsyncFunctionDef)
    assert compare_ast(method_def.body, expected_method_body)


def test_add_method_adds_method_definition():
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

    generator.add_method(
        name=method_name,
        return_type=return_type,
        arguments=arguments,
        arguments_dict=arguments_dict,
        operation_str="",
        async_=False,
    )
    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def
    method_def = class_def.body[0]

    assert isinstance(method_def, ast.FunctionDef)
    assert method_def.name == method_name
    assert isinstance(method_def.returns, ast.Name)
    assert method_def.returns.id == return_type
    assert method_def.args == arguments


def test_add_method_generates_correct_method_body():
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
            annotation=ast.Subscript(
                value=ast.Name(id="dict"),
                slice=ast.Tuple(elts=[ast.Name(id="str"), ast.Name(id="object")]),
            ),
            value=ast.Dict(
                keys=[ast.Constant(value="arg1")], values=[ast.Name(id="arg1")]
            ),
            simple=1,
        ),
        ast.Assign(
            targets=[ast.Name(id="response")],
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id="self"), attr="execute"),
                args=[],
                keywords=[
                    ast.keyword(arg="query", value=ast.Name(id="query")),
                    ast.keyword(arg="variables", value=ast.Name(id="variables")),
                ],
            ),
        ),
        ast.Assign(
            targets=[ast.Name(id="data")],
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id="self"), attr="get_data"),
                args=[ast.Name(id="response")],
                keywords=[],
            ),
        ),
        ast.Return(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id="ListXyz"), attr="parse_obj"),
                args=[ast.Name(id="data")],
                keywords=[],
            )
        ),
    ]

    generator.add_method(
        name=method_name,
        return_type=return_type,
        arguments=arguments,
        arguments_dict=arguments_dict,
        operation_str=query_str,
        async_=False,
    )
    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def
    method_def = class_def.body[0]
    assert isinstance(method_def, ast.FunctionDef)
    assert compare_ast(method_def.body, expected_method_body)


def test_add_method_triggers_generate_client_method_hook(mocker):
    mocked_plugin_manager = mocker.MagicMock()
    generator = ClientGenerator(
        "ClientXyz", "BaseClient", plugin_manager=mocked_plugin_manager
    )

    generator.add_method(
        name="list_xyz",
        return_type="ListXyz",
        arguments=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg="self")],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        arguments_dict=ast.Dict(keys=[], values=[]),
        operation_str="",
        async_=False,
    )
    generator.add_import(["TestType"], "test", level=1)

    assert mocked_plugin_manager.generate_client_method.called
