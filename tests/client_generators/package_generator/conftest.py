import pytest
from graphql import build_ast_schema, parse


@pytest.fixture
def schema_str():
    return """
        schema {
            query: Query
        }

        type Query {
            query1(id: ID!, param: SCALARABC): CustomType
            query2: [CustomType!]
            query3(val: CustomEnum!): [CustomType]
        }

        type CustomType {
            id: ID!
            field1: [String]
            field2: CustomType2
            field3: CustomEnum!
        }

        type CustomType2 {
            fieldb: Int
        }

        enum CustomEnum {
            VAL1
            VAL2
        }

        input CustomInput {
            value: Int!
        }

        scalar SCALARABC
    """


@pytest.fixture
def schema(schema_str):
    return build_ast_schema(parse(schema_str))
