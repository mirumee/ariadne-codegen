from typing import Dict, List, Set

from graphql import (
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLUnionType,
)


class TypeCollector:
    def __init__(self, schema: GraphQLSchema):
        self.schema = schema
        self.collected_types: Set[str] = set()
        self.visited_types: Set[str] = set()

    def collect(self) -> List[str]:
        if self.schema.query_type:
            self._collect_types(self.schema.query_type.fields)
        if self.schema.mutation_type:
            self._collect_types(self.schema.mutation_type.fields)
        return sorted(self.collected_types)

    def _collect_types(self, fields: Dict[str, GraphQLObjectType]) -> None:
        for field in fields.values():
            graphql_type = get_final_type(field)
            self._collect_dependent_types(graphql_type)

    def _collect_dependent_types(self, graphql_type: GraphQLObjectType) -> None:
        stack = [graphql_type]

        while stack:
            current_type = stack.pop()
            if current_type.name in self.visited_types:
                continue

            self.visited_types.add(current_type.name)
            self.collected_types.add(current_type.name)

            if isinstance(current_type, (GraphQLObjectType, GraphQLInterfaceType)):
                for subfield in current_type.fields.values():
                    subfield_type = get_final_type(subfield)
                    if isinstance(subfield_type, GraphQLObjectType):
                        stack.append(subfield_type)
                    elif isinstance(subfield_type, GraphQLUnionType):
                        stack.extend(subfield_type.types)
                for interface in current_type.interfaces:
                    stack.append(interface)


def get_final_type(type_):
    while hasattr(type_, "of_type"):
        type_ = type_.of_type
    if hasattr(type_, "type"):
        return get_final_type(type_.type)
    return type_
