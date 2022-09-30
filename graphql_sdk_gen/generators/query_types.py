from graphql import GraphQLSchema, OperationDefinitionNode
import ast


class QueryTypesGenerator:
    def __init__(
        self, schema: GraphQLSchema, base_type_definitions: dict[str, ast.ClassDef]
    ) -> None:
        self.schema = schema
        self.base_type_definitions = base_type_definitions

    
    def generate(self, query: OperationDefinitionNode) -> ast.Module:
        if not (query_name:= query.name):
            raise Exception
        
        class_def = ast.ClassDef(
            name=query_name.value,
            bases=[ast.Name("BaseModel")],
            keywords=[],
            body=[],
            decorator_list=[],
        )
        for lineno, field in enumerate(query.selection_set.selections, start=1):
            type_name = self.schema.query_type.fields[field.name.value].type.name

            class_def.body.append(
                ast.AnnAssign(
                    target=ast.Name(id=field.name.value),
                    annotation=ast.Name(id=query_name.value + type_name),
                    simple=1,
                    lineno=lineno,
                )
            )
        return ast.Module(body=[class_def], type_ignores=[])
