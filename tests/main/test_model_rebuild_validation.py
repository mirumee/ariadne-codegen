"""
To ensure all models with nested dependencies are fully rebuilt this test will
create an instance of the query from `multiple_fragments` containing a `FullA`
(extended from `ExampleQuery2ExampleQuery`) which in turn holds a `FullB`
(extended from `FullAFieldB`).

If this model is not rebuilt with `FullA.model_rebuild()` `ExampleQuery2` will
not be fully defined and we will get a `PydanticUserError`.

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


def test_model_rebuild_validate():
    # Perform some sanity checks on the schema for `ExampleQuery2` to test that
    # it confirms to the fields of `FullA` and that it references `FullB`.
    json_schema = ExampleQuery2.model_json_schema()
    assert all(
        x in json_schema["$defs"] for x in ["ExampleQuery2ExampleQuery", "FullAFieldB"]
    )

    query_props = json_schema["$defs"]["ExampleQuery2ExampleQuery"]["properties"]
    assert all(x in query_props for x in ["id", "value", "fieldB"])
    assert query_props["fieldB"]["$ref"] == "#/$defs/FullAFieldB"

    # Assert we cannot validate a faulty type.
    field_b = {"id": "321", "value": 13.37}
    field_a = {"id": "123", "value": "A", "field_b": field_b}

    with pytest.raises(ValidationError):
        ExampleQuery2.model_validate(field_a)

    # However it should work with the correct type and the type extending the
    # correct type.
    try:
        FullA.model_validate(field_a)
        ExampleQuery2ExampleQuery.model_validate(field_a)
    except ValidationError as e:
        assert False, f"model_valiadte failed: {e}"

    # And since the model is rebuilt we should be able to construct a full
    # `ExampleQuery2`.
    example_query_2 = {"example_query": field_a}

    try:
        ExampleQuery2.model_validate(example_query_2)
    except ValidationError as e:
        assert False, f"model validation failed: {e}"
