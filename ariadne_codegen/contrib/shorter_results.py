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
`get_authenticated_user` will instead directly return a
`GetAuthenticatedUserMe` so the caller can use:

    me = await client.get_authenticated_user

This plugin can be enabled in the settings:

    plugins = ["ariadne_codegen.contrib.shorter_results.ShorterResultsPlugin"]
"""

import ast
from copy import deepcopy
from typing import Dict, List, Optional, Union

from graphql import (
    ExecutableDefinitionNode,
    FragmentDefinitionNode,
    GraphQLSchema,
    SelectionSetNode,
)

from ..codegen import (
    generate_async_for,
    generate_attribute,
    generate_expr,
    generate_import_from,
    generate_name,
    generate_return,
    generate_subscript,
    generate_yield,
)
from ..plugins.base import Plugin


class ShorterResultsPlugin(Plugin):
    """
    Make single field return types expanded.

    All client methods that return a type with a single field will be expanded and
    instead return the inner field.
    """

    def __init__(self, schema: GraphQLSchema, config_dict: Dict) -> None:
        self.class_dict: Dict[str, ast.ClassDef] = {}
        self.extended_imports: Dict[str, set] = {}
        self.imported_types: Dict[str, str] = {}

        super().__init__(schema, config_dict)

    def generate_result_types_module(
        self, module: ast.Module, operation_definition: ExecutableDefinitionNode
    ) -> ast.Module:
        for stmt in module.body:
            if not isinstance(stmt, ast.ImportFrom):
                continue

            if stmt.module is None:
                continue

            for name in stmt.names:
                from_ = "." * stmt.level + stmt.module
                if name.asname is not None:
                    self.imported_types[name.asname] = from_
                else:
                    self.imported_types[name.name] = from_

        return super().generate_result_types_module(module, operation_definition)

    def generate_result_class(
        self,
        class_def: ast.ClassDef,
        operation_definition: ExecutableDefinitionNode,
        selection_set: SelectionSetNode,
    ) -> ast.ClassDef:
        """Store a map of all classes and their AST."""
        self.class_dict[class_def.name] = class_def

        return super().generate_result_class(
            class_def, operation_definition, selection_set
        )

    def generate_fragments_module(
        self,
        module: ast.Module,
        fragments_definitions: Dict[str, FragmentDefinitionNode],
    ) -> ast.Module:
        """Store a map of all fragment classes and their AST."""
        fragments_module_name = (
            self.config_dict.get("tool", {})
            .get("ariadne-codegen", {})
            .get("fragments_module_name", "fragments")
        )

        for fragment_class in [
            x.name for x in module.body if isinstance(x, ast.ClassDef)
        ]:
            self.imported_types[fragment_class] = f".{fragments_module_name}"

        return super().generate_fragments_module(module, fragments_definitions)

    def generate_client_module(self, module: ast.Module) -> ast.Module:
        """
        Update the generated client.

        At this point we've the full ast for all classes used for the client so
        instead of modifying class by class in `generate_client_method` we
        modify each method from here. By doing so we ensure that we have a map
        between all classes, including fragments, so we can traverse them to
        figure out how many fields we have in total for each request.

        If we only have a single field, including when expanding our fragments,
        we can expand the single field and update the return type.
        """
        client_def = next(
            filter(lambda o: isinstance(o, ast.ClassDef), module.body), None
        )
        if not client_def or not isinstance(client_def, ast.ClassDef):
            return super().generate_client_module(module)

        for method_def in [
            m
            for m in client_def.body
            if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]:
            self._modify_method_def(method_def)

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

            # We delete the key if it already had an import from statement so we
            # can create new imports for types not yet imported such as custom
            # scalars.
            self.extended_imports.pop(stmt.module, None)

        for import_from, alias in self.extended_imports.items():
            # We insert the import at the top, it will be sorted properly in a
            # post-process step that will order the imports.
            module.body.insert(
                0,
                generate_import_from(
                    names=list(alias),
                    from_=import_from,
                ),
            )

        return super().generate_client_module(module)

    def _modify_method_def(
        self, method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> None:
        """
        Change the method generated in the client to call the inner field and
        change the return type. We do this here instead of
        `generate_client_method` to ensure we have a map between all our classes
        when updating the method def.
        """
        if len(method_def.body) < 1:
            return None

        last_stmt = method_def.body[-1]

        if isinstance(last_stmt, ast.Return):
            self._generate_query_and_mutation_client_method(method_def, last_stmt)
        elif isinstance(last_stmt, ast.AsyncFor):
            self._generate_subscription_client_method(method_def, last_stmt)

        return None

    def _generate_subscription_client_method(
        self,
        method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef],
        async_for_stmt: ast.AsyncFor,
    ):
        """Generate method for subscriptions."""
        if not isinstance(method_def.returns, ast.Subscript):
            return None

        if not isinstance(method_def.returns.slice, ast.Name):
            return None

        node_and_class = _return_or_yield_node_and_class(
            method_def.returns.slice.id, self.class_dict
        )
        if node_and_class is None:
            return None

        yield_node, single_field_classes, single_field_return_class = node_and_class

        previous_yield_value = _get_yield_value_from_async_for(method_def.body[-1])
        if previous_yield_value is None:
            return None

        # Update the return type to be the inner field and ensure we reference
        # the single field before returning.
        method_def.returns = generate_subscript(
            value=generate_name("AsyncIterator"),
            slice_=yield_node,
        )

        method_def.body[-1] = generate_async_for(
            target=async_for_stmt.target,
            iter_=async_for_stmt.iter,
            body=generate_expr(
                value=generate_yield(
                    value=generate_attribute(
                        value=previous_yield_value,
                        attr=single_field_return_class,
                    )
                )
            ),
        )

        self._update_imports(method_def, single_field_classes)

        return None

    def _generate_query_and_mutation_client_method(
        self,
        method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef],
        return_stmt: ast.Return,
    ) -> None:
        """Generate method for query or mutations."""
        if return_stmt.value is None:
            return None

        if not isinstance(method_def.returns, ast.Name):
            return None

        node_and_class = _return_or_yield_node_and_class(
            method_def.returns.id, self.class_dict
        )
        if node_and_class is None:
            return None

        return_node, single_field_classes, single_field_return_class = node_and_class

        # Update the return type to be the inner field and ensure we reference
        # the single field before returning.
        method_def.returns = return_node
        method_def.body[-1] = generate_return(
            value=generate_attribute(
                value=return_stmt.value, attr=single_field_return_class
            )
        )

        self._update_imports(method_def, single_field_classes)

        return None

    def _update_imports(
        self,
        method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef],
        single_field_classes: List[str],
    ):
        """
        After expanding to the inner type we will end up with one or more
        classes that we're now returning. Ensure they're all imported in the
        file defining the method.
        """
        for single_field_class in single_field_classes:
            # The unwrapped field might be a custom scalar or fragment, if it is
            # ensure we add it to imports.
            if single_field_class in self.imported_types:
                import_from = self.imported_types[single_field_class]
            elif single_field_class in self.class_dict:
                import_from = method_def.name
            else:
                continue

            # After we change the type we also need to import it in the client if
            # it's one of our generated types so add the extra import as needed.
            if import_from not in self.extended_imports:
                self.extended_imports[import_from] = set()

            self.extended_imports[import_from].add(single_field_class)


def _get_yield_value_from_async_for(stmt: ast.stmt) -> Optional[ast.expr]:
    """
    Extract inner yield value from `ast.AsyncFor` and return `None` if the stmt
    isn't of expected type.
    """
    if not isinstance(stmt, ast.AsyncFor):
        return None

    if len(stmt.body) < 1:
        return None

    if not isinstance(stmt.body[0], ast.Expr):
        return None

    if not isinstance(stmt.body[0].value, ast.Yield):
        return None

    return stmt.body[0].value.value


def _return_or_yield_node_and_class(
    current_return_class: str, class_dict: Dict[str, ast.ClassDef]
) -> Optional[tuple[ast.expr, List[str], str]]:
    """
    Given there's only a single field in the return type, return the ast for
    that node, what class(es) that is and the name of the field.
    """
    if current_return_class not in class_dict:
        return None

    fields = _get_all_fields(class_dict[current_return_class], class_dict)
    if len(fields) != 1:
        return None

    single_field = fields[0]
    if not isinstance(single_field, ast.AnnAssign):
        return None

    if not isinstance(single_field.target, ast.Name):
        return None

    # Traverse the type annotation until we find the inner type. This can
    # require several iterations if the return type is something like
    # Optional[List[Any]]
    #
    # We make a deepcopy because we need to keep the quoted annotations for the
    # fields in the query classes but we want to have it unquoted in the client
    # method where we import the actual types.
    annotations = deepcopy(single_field.annotation)
    return_node, return_classes = _update_node(annotations)

    return return_node, return_classes, single_field.target.id


def _update_node(node: ast.expr) -> tuple[ast.expr, List[str]]:
    """
    Walk down a node to find the inner `ast.Name`. Once found, evaluate the
    potential literal so it gets unquoted and return the inner name.
    """
    if isinstance(node, ast.Name):
        try:
            node.id = ast.literal_eval(node.id)
        except ValueError:
            # Not a literal
            pass

        return node, [node.id]

    if isinstance(node, ast.Subscript):
        child_node, node_ids = _update_node(node.slice)

        # We don't want to keep annotations in the return type so if the node is
        # an annotated subscript (which may come from something like interface
        # discriminators), remove them.
        if (
            isinstance(node.value, ast.Name)
            and node.value.id == "Annotated"
            and isinstance(child_node, ast.Tuple)
            and len(child_node.elts) == 2
        ):
            return _update_node(child_node.elts[0])

        node.slice = child_node

        return node, node_ids

    if isinstance(node, ast.Tuple):
        all_node_ids = []
        for i, elt in enumerate(node.elts):
            node.elts[i], node_ids = _update_node(elt)
            all_node_ids.extend(node_ids)

        return node, all_node_ids

    if isinstance(node, ast.expr):
        return node, []

    return ast.expr(), []


def _get_all_fields(
    class_def: ast.ClassDef, class_dict: Dict[str, ast.ClassDef]
) -> List[ast.AnnAssign]:
    """
    Recursively get all fields from all inherited classes to figure out the
    total number of fields.
    """
    fields = []

    for base in class_def.bases:
        if not isinstance(base, ast.Name) or base.id not in class_dict:
            continue

        fields.extend(_get_all_fields(class_dict[base.id], class_dict))

    for field in class_def.body:
        if isinstance(field, ast.AnnAssign):
            fields.append(field)

    return fields
