from datetime import datetime
from typing import Callable, Optional

from ..settings import CommentsStrategy
from .constants import (
    COMMENT_DATETIME_FORMAT,
    SOURCE_COMMENT,
    STABLE_COMMENT,
    TIMESTAMP_COMMENT,
)


def get_comment(strategy: CommentsStrategy, source: Optional[str] = None) -> str:
    # pylint: disable=unused-argument
    def empty_comment_function(source: Optional[str] = None) -> str:
        return ""

    get_comment_function: Callable[[Optional[str]], str] = {
        CommentsStrategy.NONE: empty_comment_function,
        CommentsStrategy.TIMESTAMP: get_timestamp_comment,
        CommentsStrategy.STABLE: get_stable_comment,
    }.get(strategy, empty_comment_function)

    return get_comment_function(source)


def get_timestamp_comment(source: Optional[str] = None) -> str:
    comment = TIMESTAMP_COMMENT.format(datetime.now().strftime(COMMENT_DATETIME_FORMAT))
    if source:
        comment += "\n" + SOURCE_COMMENT.format(source)

    return comment


def get_stable_comment(source: Optional[str] = None) -> str:
    comment = STABLE_COMMENT
    if source:
        comment += "\n" + SOURCE_COMMENT.format(source)

    return comment
