import ast

from graphql import build_schema

from ariadne_codegen.contrib.client_forward_refs import ClientForwardRefsPlugin


def test_plugin_skips_self_calls_from_custom_operation_methods():
    """Methods that return self.something(...) must not trigger import of 'self'.

    With enable_custom_operations, the client has execute_custom_operation()
    returning self.get_data(response), and query()/mutation() returning
    await self.execute_custom_operation(...). The plugin must not treat
    'self' as a generated class name (KeyError('self')).
    """

    module = ast.parse(
        """
        from .async_base_client import AsyncBaseClient
        from .some_operation import SomeOperation

        class Client(AsyncBaseClient):
            def execute_custom_operation(self):
                return self.get_data("response")

            async def get_something(self):
                from .some_operation import SomeOperation
                return SomeOperation.model_validate({})
        """
    )

    schema = build_schema("type Query { x: Int }")
    config = {"target_package_name": "test"}
    plugin = ClientForwardRefsPlugin(schema, config)

    updated = plugin.generate_client_module(module)

    client_class = next(n for n in updated.body if isinstance(n, ast.ClassDef))
    methods = {n.name: n for n in client_class.body if isinstance(n, ast.FunctionDef)}
    exec_op = methods["execute_custom_operation"]
    first_stmt = exec_op.body[0]
    assert not (
        isinstance(first_stmt, ast.ImportFrom)
        and first_stmt.module
        and "self" in (a.name for a in first_stmt.names)
    ), "Plugin must not add import for 'self'"
