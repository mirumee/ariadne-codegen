from datetime import datetime

import pytest
from freezegun import freeze_time

from ariadne_codegen.client_generators.comments import (
    get_comment,
    get_stable_comment,
    get_timestamp_comment,
)
from ariadne_codegen.client_generators.constants import (
    COMMENT_DATETIME_FORMAT,
    SOURCE_COMMENT,
    STABLE_COMMENT,
    TIMESTAMP_COMMENT,
)
from ariadne_codegen.settings import CommentsStrategy


@pytest.mark.parametrize("source", [None, "source.graphql"])
def test_get_comment_calls_correct_method_for_stable_strategy(source):
    assert get_comment(
        strategy=CommentsStrategy.STABLE, source=source
    ) == get_stable_comment(source=source)


@pytest.mark.parametrize("source", [None, "source.graphql"])
@freeze_time("24.12.2023 18:00")
def test_get_comment_calls_correct_method_for_timestamp_strategy(source):
    assert get_comment(
        strategy=CommentsStrategy.TIMESTAMP, source=source
    ) == get_timestamp_comment(source=source)


@pytest.mark.parametrize("source", [None, "source.graphql"])
def test_get_comment_returns_empty_string_for_none_strategy(source):
    assert get_comment(strategy=CommentsStrategy.NONE, source=source) == ""


@freeze_time("24.12.2023 18:00")
def test_get_timestamp_comment_returns_string_without_source():
    assert get_timestamp_comment() == TIMESTAMP_COMMENT.format(
        datetime.now().strftime(COMMENT_DATETIME_FORMAT)
    )


@freeze_time("24.12.2023 18:00")
def test_get_timestamp_comment_returns_string_witho_source():
    result = get_timestamp_comment("source.graphql")

    assert (
        TIMESTAMP_COMMENT.format(datetime.now().strftime(COMMENT_DATETIME_FORMAT))
        in result
    )
    assert SOURCE_COMMENT.format("source.graphql") in result


def test_get_stable_comment_returns_string_without_source():
    assert get_stable_comment() == STABLE_COMMENT


def test_get_stable_cooment_returns_string_with_source():
    result = get_stable_comment(source="source.graphql")

    assert STABLE_COMMENT in result
    assert SOURCE_COMMENT.format("source.graphql") in result
