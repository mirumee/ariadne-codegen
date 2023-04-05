from typing import List, Optional

import pytest

from ariadne_codegen.client_generators.dependencies.base_model import BaseModel


@pytest.mark.parametrize(
    "annotation, value, expected_args",
    [
        (str, "a", ["a"]),
        (Optional[str], "a", ["a"]),
        (Optional[str], None, [None]),
        (List[str], ["a", "b"], ["a", "b"]),
        (List[Optional[str]], ["a", None], ["a", None]),
        (Optional[List[str]], ["a", "b"], ["a", "b"]),
        (Optional[List[str]], None, []),
        (Optional[List[Optional[str]]], ["a", None], ["a", None]),
        (List[List[str]], [["a", "b"], ["c", "d"]], ["a", "b", "c", "d"]),
        (Optional[List[List[str]]], [["a", "b"], ["c", "d"]], ["a", "b", "c", "d"]),
        (Optional[List[List[str]]], None, []),
        (
            Optional[List[Optional[List[str]]]],
            [["a", "b"], ["c", "d"]],
            ["a", "b", "c", "d"],
        ),
        (Optional[List[Optional[List[str]]]], None, []),
        (Optional[List[Optional[List[str]]]], [["a", "b"], None], ["a", "b"]),
        (
            Optional[List[Optional[List[Optional[str]]]]],
            [["a", "b"], ["c", "d"]],
            ["a", "b", "c", "d"],
        ),
        (Optional[List[Optional[List[Optional[str]]]]], None, []),
        (Optional[List[Optional[List[Optional[str]]]]], [["a", "b"], None], ["a", "b"]),
        (
            Optional[List[Optional[List[Optional[str]]]]],
            [["a", None], ["b", None]],
            ["a", None, "b", None],
        ),
    ],
)
def test_parse_obj_applies_parse_on_every_element(
    annotation, value, expected_args, mocker
):
    mocked_parse = mocker.MagicMock(side_effect=lambda s: s)
    mocker.patch(
        "ariadne_codegen.client_generators.dependencies.base_model."
        "SCALARS_PARSE_FUNCTIONS",
        {str: mocked_parse},
    )

    class TestModel(BaseModel):
        field: annotation

    TestModel.parse_obj({"field": value})

    assert mocked_parse.call_count == len(expected_args)
    assert [c.args[0] for c in mocked_parse.call_args_list] == expected_args


def test_parse_obj_doesnt_apply_parse_on_not_matching_type(mocker):
    mocked_parse = mocker.MagicMock(side_effect=lambda s: s)
    mocker.patch(
        "ariadne_codegen.client_generators.dependencies.base_model."
        "SCALARS_PARSE_FUNCTIONS",
        {str: mocked_parse},
    )

    class TestModel(BaseModel):
        field_a: int
        field_b: Optional[int]
        field_c: Optional[int]
        field_d: List[int]
        field_e: Optional[List[int]]
        field_f: Optional[List[int]]
        field_g: Optional[List[Optional[int]]]
        field_h: Optional[List[Optional[int]]]
        field_i: Optional[List[Optional[int]]]

    TestModel.parse_obj(
        {
            "field_a": 1,
            "field_b": 2,
            "field_c": None,
            "field_d": [3, 4],
            "field_e": [5, 6],
            "field_f": None,
            "field_g": [7, 8],
            "field_h": [9, None],
            "field_i": None,
        }
    )

    assert not mocked_parse.called

@pytest.mark.parametrize(
    "annotation, value, expected_args",
    [
        (str, "a", {"a"}),
        (Optional[str], "a", {"a"}),
        (Optional[str], None, set()),
        (List[str], ["a", "b"], {"a", "b"}),
        (List[Optional[str]], ["a", None], {"a"}),
        (Optional[List[str]], ["a", "b"], {"a", "b"}),
        (Optional[List[str]], None, set()),
        (Optional[List[Optional[str]]], ["a", None], {"a"}),
        (Optional[List[Optional[str]]], None, set()),
        (List[List[str]], [["a", "b"], ["c", "d"]], {"a", "b", "c", "d"}),
        (Optional[List[List[str]]], [["a", "b"], ["c", "d"]], {"a", "b", "c", "d"}),
        (Optional[List[List[str]]], None, set()),
        (
            Optional[List[Optional[List[str]]]],
            [["a", "b"], ["c", "d"]],
            {"a", "b", "c", "d"},
        ),
        (Optional[List[Optional[List[str]]]], None, set()),
        (Optional[List[Optional[List[str]]]], [["a", "b"], None], {"a", "b"}),
        (
            Optional[List[Optional[List[Optional[str]]]]],
            [["a", "b"], ["c", "d"]],
            {"a", "b", "c", "d"},
        ),
        (Optional[List[Optional[List[Optional[str]]]]], None, set()),
        (Optional[List[Optional[List[Optional[str]]]]], [["a", "b"], None], {"a", "b"}),
        (
            Optional[List[Optional[List[Optional[str]]]]],
            [["a", None], ["b", None]],
            {"a", "b"},
        ),
    ],
)
def test_dict_applies_serialize_on_every_list_element(
    annotation, value, expected_args, mocker
):
    mocked_serialize = mocker.MagicMock(side_effect=lambda s: s)
    mocker.patch(
        "ariadne_codegen.client_generators.dependencies.base_model."
        "SCALARS_SERIALIZE_FUNCTIONS",
        {str: mocked_serialize},
    )

    class TestModel(BaseModel):
        field: annotation

    TestModel.parse_obj({"field": value}).dict()

    assert mocked_serialize.call_count == len(expected_args)
    assert {c.args[0] for c in mocked_serialize.call_args_list} == expected_args


def test_dict_doesnt_apply_serialize_on_not_matching_type(mocker):
    mocked_serialize = mocker.MagicMock(side_effect=lambda s: s)
    mocker.patch(
        "ariadne_codegen.client_generators.dependencies.base_model."
        "SCALARS_SERIALIZE_FUNCTIONS",
        {str: mocked_serialize},
    )

    class TestModel(BaseModel):
        field_a: int
        field_b: Optional[int]
        field_c: Optional[int]
        field_d: List[int]
        field_e: Optional[List[int]]
        field_f: Optional[List[int]]
        field_g: Optional[List[Optional[int]]]
        field_h: Optional[List[Optional[int]]]
        field_i: Optional[List[Optional[int]]]

    TestModel.parse_obj(
        {
            "field_a": 1,
            "field_b": 2,
            "field_c": None,
            "field_d": [3, 4],
            "field_e": [5, 6],
            "field_f": None,
            "field_g": [7, 8],
            "field_h": [9, None],
            "field_i": None,
        }
    ).dict()

    assert not mocked_serialize.called


def test_dict_applies_serialize_only_once_for_every_element(mocker):
    mocked_serialize = mocker.MagicMock(side_effect=lambda s: s)
    mocker.patch(
        "ariadne_codegen.client_generators.dependencies.base_model."
        "SCALARS_SERIALIZE_FUNCTIONS",
        {str: mocked_serialize},
    )

    class TestModelC(BaseModel):
        value: str

    class TestModelB(BaseModel):
        value: str
        field_c: TestModelC

    class TestModelA(BaseModel):
        value: str
        field_b: TestModelB

    TestModelA.parse_obj(
        {"value": "a", "field_b": {"value": "b", "field_c": {"value": "c"}}}
    ).dict()

    assert mocked_serialize.call_count == 3
    assert {c.args[0] for c in mocked_serialize.call_args_list} == {"a", "b", "c"}
