"""
Shorter results by returning single fields directly.

Given a GraphQL schema that looks like this:

    type Query{
        me: User
    }

    type User {
        id: ID!
        username: String!
    }

The codegen will generate a class that has a single attribute `me`.

    class GetAuthenticatedUser(BaseModel):
        me: Optional["GetAuthenticatedUserMe"]

When later using the client to call `get_authenticated_user` the return type
would most of the time immediately be expanded to get the inner
`GetAuthenticatedUserMe`:

    me = (await client.get_authenticated_user).me

By enabling this plugin the return type of the generated
`get_authenticated_user` would instead directly return a
`GetAuthenticatedUserMe` so the caller could use:

    me = await client.get_authenticated_user

This plugin can be enabled by either adding the plugin in the settings:

    plugins = ["ariadne_codegen.ShorterResultsPlugin"]

Or with the shorthand setting:

    [tool.ariadne-codegen]
    unwrap_single_fields = true
"""

import ast
from typing import Union

from ariadne_codegen.plugins.base import (
    Plugin,
    SelectionSetNode,
    OperationDefinitionNode,
)


class ShorterResultsPlugin(Plugin):
    """
    Make single field return types expanded.

    All client method that returns type with a single field will be expanded and
    instead return the type of the inner field.
    """

    def generate_result_class(
        self,
        class_def: ast.ClassDef,
        operation_definition: OperationDefinitionNode,
        selection_set: SelectionSetNode,
    ) -> ast.ClassDef:
        """Store a map of all classes and its ast"""
        self.class_dict[class_def.name] = class_def

        return super().generate_result_class(
            class_def, operation_definition, selection_set
        )

    def generate_client_module(self, module: ast.Module) -> ast.Module:
        """Add extra import needed after expanding the inner field"""
        if len(self.extended_imports) == 0:
            return super().generate_client_module(module)

        for stmt in module.body:
            # We know we've already imported the wrapping type so we're only
            # interested in `ImportFrom`.
            if not isinstance(stmt, ast.ImportFrom):
                continue

            # The module we import from is always the same as the method we
            # modified when changing the return type.
            if stmt.module not in self.extended_imports:
                continue

            # Add all additional imports discovered when generating the client
            # method.
            for additional_import in self.extended_imports[stmt.module]:
                stmt.names.append(ast.alias(name=additional_import))

        return super().generate_client_module(module)

    def generate_client_method(
        self, method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> Union[ast.FunctionDef, ast.AsyncFunctionDef]:
        """
        Change the method generated in the client to call the inner field and
        change the return type.
        """
        if len(method_def.body) < 1:
            return super().generate_client_method(method_def)

        # TODO: Can we assume that the return statement is always the last
        # statement?
        return_stmt = method_def.body[-1]
        if not isinstance(return_stmt, ast.Return):
            return super().generate_client_method(method_def)

        # Get the originally returned class so we can look at the class
        # definition to see how many fields it has.
        if not isinstance(method_def.returns, ast.Name):
            return super().generate_client_method(method_def)

        return_class = method_def.returns.id
        if return_class not in self.class_dict:
            return super().generate_client_method(method_def)

        return_class_ast = self.class_dict[return_class]

        # If we're not a single method data class move on!
        if len(return_class_ast.body) != 1:
            return super().generate_client_method(method_def)

        single_field = return_class_ast.body[0]

        # Get the field class name, which might be an optional and if so
        # represented as an `ast.Subscript`.
        # We need to update the proper return type to be optional as well so we
        # store that. The ast in the annotation isn't an evaluated node so we
        # can't return that as is.
        if isinstance(single_field.annotation, ast.Name):
            is_optional = False
            single_field_class = single_field.annotation.id
        elif isinstance(single_field.annotation, ast.Subscript):
            is_optional = True
            single_field_class = single_field.annotation.slice.id
        else:
            return super().generate_client_method(method_def)

        single_field_name = single_field.target.id

        # We only want to expand for classes we created. Some queries will
        # return a type that has a single field which is of `typing.Any` or
        # other things not generated this iteration so ignore those.
        # TODO: Can we ensure this in a better way?
        try:
            single_field_class = ast.literal_eval(single_field_class)
        except ValueError:
            # Not a literal
            pass

        if single_field_class not in self.class_dict:
            return super().generate_client_method(method_def)

        # Update the return type to be the inner field and ensure we reference
        # the single field before returning.
        if is_optional:
            method_def.returns = ast.Subscript(
                value=ast.Name(id="Optional"), slice=ast.Name(id=single_field_class)
            )
        else:
            method_def.returns = ast.Name(id=single_field_class)

        method_def.body[-1] = ast.Attribute(
            value=return_stmt,
            attr=single_field_name,
        )

        # After we change the type we also need to import it from the client so
        # add the extra import as needed.
        if method_def.name not in self.extended_imports:
            self.extended_imports[method_def.name] = set()

        self.extended_imports[method_def.name].add(single_field_class)

        return super().generate_client_method(method_def)
