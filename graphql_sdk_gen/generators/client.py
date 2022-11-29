import ast

from .codegen import (
    generate_ann_assign,
    generate_assign,
    generate_async_method_definition,
    generate_attribute,
    generate_await,
    generate_call,
    generate_class_def,
    generate_constant,
    generate_dict,
    generate_import_from,
    generate_keyword,
    generate_name,
    generate_return,
    generate_trivial_lambda,
)
from .constants import OPTIONAL


class ClientGenerator:
    def __init__(self, name: str, base_client: str) -> None:
        self.name = name
        self.class_def = generate_class_def(name=name, base_names=[base_client])
        self.imports: list = [generate_import_from([OPTIONAL], "typing")]
        self.gql_lambda_name = "gql"

    def generate(self) -> ast.Module:
        """Generate module with class definistion of grahql client."""
        gql_lambda = generate_trivial_lambda(self.gql_lambda_name, "q")
        gql_lambda.lineno = len(self.imports) + 1
        self.class_def.lineno = len(self.imports) + 2
        if not self.class_def.body:
            self.class_def.body.append(ast.Pass())
        return ast.Module(
            body=self.imports + [gql_lambda, self.class_def],
            type_ignores=[],
        )

    def add_import(self, names: list[str], from_: str, level: int = 0) -> None:
        """Add import to be included in init file."""
        self.imports.append(generate_import_from(names=names, from_=from_, level=level))

    def add_async_method(
        self,
        name: str,
        return_type: str,
        arguments: ast.arguments,
        arguments_dict: ast.Dict,
        query_str: str,
    ):
        """Add definition of async method."""
        self.class_def.body.append(
            generate_async_method_definition(
                name=name,
                arguments=arguments,
                return_type=generate_name(return_type),
                body=self._generate_query_method_body(
                    query_str, arguments_dict, return_type
                ),
                lineno=len(self.class_def.body) + 1,
            )
        )

    def _generate_query_method_body(
        self,
        query_str: str,
        arguments_dict: ast.Dict,
        return_type: str,
    ) -> list[ast.stmt]:
        return [
            generate_assign(
                ["query"],
                generate_call(
                    func=ast.Name(id=self.gql_lambda_name),
                    args=[
                        [generate_constant(l + "\n") for l in query_str.splitlines()]
                    ],
                ),
                lineno=1,
            ),
            generate_ann_assign(
                "variables",
                generate_name("dict"),
                arguments_dict,
                lineno=2,
            ),
            generate_assign(
                ["response"],
                generate_await(
                    generate_call(
                        func=generate_attribute(generate_name("self"), "execute"),
                        keywords=[
                            generate_keyword("query", generate_name("query")),
                            generate_keyword("variables", generate_name("variables")),
                        ],
                    )
                ),
                lineno=3,
            ),
            generate_return(
                generate_call(
                    func=generate_attribute(generate_name(return_type), "parse_obj"),
                    args=[
                        generate_call(
                            func=generate_attribute(
                                generate_call(
                                    generate_attribute(
                                        generate_name("response"), "json"
                                    )
                                ),
                                "get",
                            ),
                            args=[generate_constant("data"), generate_dict()],
                        )
                    ],
                )
            ),
        ]
