from dataclasses import dataclass
from pathlib import Path

from ariadne import (
    InputType,
    QueryType,
    ScalarType,
    load_schema_from_path,
    make_executable_schema,
)
from ariadne.asgi import GraphQL

type_defs = load_schema_from_path(Path(__file__).parent / "schema.graphql")

custom_scalar = ScalarType("CUSTOMSCALAR")


@dataclass
class CustomScalar:
    value: str


@custom_scalar.serializer
def serialize_custom_scalar(obj: CustomScalar) -> str:
    return obj.value


@custom_scalar.value_parser
def parse_custom_scalar(value: str) -> CustomScalar:
    return CustomScalar(value=value)


@dataclass
class CustomInput:
    value: CustomScalar


query = QueryType()


@query.field("queryA")
def resolve_query_a(*_):
    return CustomScalar(value="AAA")


@query.field("queryB")
def resolve_query_b(*_, value: CustomScalar):
    return CustomScalar(value=value.value + "BBB")


@query.field("queryC")
def resolve_query_c(*_, custom_input: CustomInput):
    return CustomScalar(value=custom_input.value.value + "CCC")


schema = make_executable_schema(
    type_defs,
    query,
    custom_scalar,
    InputType(
        "CustomInput",
        lambda data: CustomInput(**data),
    ),
    convert_names_case=True,
)

app = GraphQL(schema, debug=True)
