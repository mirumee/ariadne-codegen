from graphql_sdk_gen.generators.dependencies.exceptions import (
    GraphQLClientGraphQLError,
    GraphQLClientGraphQLMultiError,
)


def test_from_dict_returns_graphql_error_with_parsed_data():
    error_dict = {
        "message": "Error message",
        "locations": [{"line": 6, "column": 7}],
        "path": ["field1", "field2", 1, "id"],
        "extensions": {
            "code": "EXAMPLE_CODE",
            "timestamp": "2023-01-01T12:0:0",
        },
    }

    result = GraphQLClientGraphQLError.from_dict(error_dict)

    assert isinstance(result, GraphQLClientGraphQLError)
    assert result.message == error_dict["message"]
    assert result.locations == error_dict["locations"]
    assert result.path == error_dict["path"]
    assert result.extensions == error_dict["extensions"]
    assert result.orginal == error_dict


def test_from_errors_dicts_returns_graphql_multi_error_with_parsed_data():
    errors_dicts = [
        {
            "message": "Error message",
            "locations": [{"line": 6, "column": 7}],
            "path": ["field1", "field2", 1, "id"],
            "extensions": {
                "code": "EXAMPLE_CODE",
                "timestamp": "2023-01-01T12:0:0",
            },
        },
        {
            "message": "Second error message",
            "locations": [{"line": 20, "column": 3}],
            "path": ["fieldA", "fieldB", 3, "name"],
            "extensions": {
                "code": "OTHER_CODE",
                "timestamp": "2023-01-01T12:0:0",
            },
        },
    ]

    result = GraphQLClientGraphQLMultiError.from_errors_dicts(errors_dicts, {})

    assert isinstance(result, GraphQLClientGraphQLMultiError)
    error0, error1 = result.errors

    assert isinstance(error0, GraphQLClientGraphQLError)
    assert error0.message == errors_dicts[0]["message"]
    assert error0.locations == errors_dicts[0]["locations"]
    assert error0.path == errors_dicts[0]["path"]
    assert error0.extensions == errors_dicts[0]["extensions"]
    assert error0.orginal == errors_dicts[0]

    assert isinstance(error1, GraphQLClientGraphQLError)
    assert error1.message == errors_dicts[1]["message"]
    assert error1.locations == errors_dicts[1]["locations"]
    assert error1.path == errors_dicts[1]["path"]
    assert error1.extensions == errors_dicts[1]["extensions"]
    assert error1.orginal == errors_dicts[1]
