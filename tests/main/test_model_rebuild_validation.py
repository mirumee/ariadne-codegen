"""
To ensure all models with nested dependencies are fully rebuilt those tests
create an instance of the query from `multiple_fragments` containing the
`FullA` fragment (used by the `ExampleQuery2ExampleQuery`) which itself includes
a field of type `FullAFieldB` that extends the `FullB` fragment.

If this model is not rebuilt with `FullA.model_rebuild()` `ExampleQuery2` will
not be fully defined and we will raise a `PydanticUserError`.

Reference to Pydantic documentation about when and why we need to call
`model_rebuild` on our types:
https://errors.pydantic.dev/2.5/u/class-not-fully-defined
"""

import pytest
from pydantic_core import ValidationError

from .clients.multiple_fragments.expected_client.example_query_2 import (
    ExampleQuery2,
    ExampleQuery2ExampleQuery,
)
from .clients.multiple_fragments.expected_client.fragments import FullA


def test_json_schema_contains_all_properties():
    json_schema = ExampleQuery2.model_json_schema()
    assert "ExampleQuery2ExampleQuery" in json_schema["$defs"]
    assert "FullAFieldB" in json_schema["$defs"]

    query_props = json_schema["$defs"]["ExampleQuery2ExampleQuery"]["properties"]
    assert "id" in query_props
    assert "value" in query_props
    assert "fieldB" in query_props
    assert query_props["fieldB"]["$ref"] == "#/$defs/FullAFieldB"


@pytest.fixture
def field_a_data():
    field_b = {"id": "321", "value": 13.37}
    field_a = {"id": "123", "value": "A", "field_b": field_b}

    return field_a


def test_validate_field_a_on_faulty_model(field_a_data):
    with pytest.raises(ValidationError):
        ExampleQuery2.model_validate(field_a_data)


def test_validate_field_a_on_correct_model(field_a_data):
    try:
        FullA.model_validate(field_a_data)
        ExampleQuery2ExampleQuery.model_validate(field_a_data)
    except ValidationError as e:
        assert False, f"model_valiadte failed: {e}"


def test_validate_field_a_in_example_query(field_a_data):
    example_query_2 = {"example_query": field_a_data}

    try:
        ExampleQuery2.model_validate(example_query_2)
    except ValidationError as e:
        assert False, f"model validation failed: {e}"
