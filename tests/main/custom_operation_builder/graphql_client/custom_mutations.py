from typing import Any, Optional

from .custom_fields import PostFields, UserFields
from .input_types import AddUserInput, UpdateUserInput


class Mutation:
    @classmethod
    def add_user(cls, *, user_input: Optional[AddUserInput] = None) -> UserFields:
        return UserFields(field_name="addUser", user_input=user_input)

    @classmethod
    def update_user(
        cls,
        *,
        user_id: Optional[str] = None,
        user_input: Optional[UpdateUserInput] = None
    ) -> UserFields:
        return UserFields(
            field_name="updateUser", user_id=user_id, user_input=user_input
        )

    @classmethod
    def delete_user(cls, *, user_id: Optional[str] = None) -> UserFields:
        return UserFields(field_name="deleteUser", user_id=user_id)

    @classmethod
    def add_post(
        cls,
        *,
        title: Optional[str] = None,
        content: Optional[str] = None,
        authorId: Optional[str] = None,
        publishedAt: Optional[Any] = None
    ) -> PostFields:
        return PostFields(
            field_name="addPost",
            title=title,
            content=content,
            authorId=authorId,
            publishedAt=publishedAt,
        )

    @classmethod
    def update_post(
        cls,
        *,
        post_id: Optional[str] = None,
        title: Optional[str] = None,
        content: Optional[str] = None,
        publishedAt: Optional[Any] = None
    ) -> PostFields:
        return PostFields(
            field_name="updatePost",
            post_id=post_id,
            title=title,
            content=content,
            publishedAt=publishedAt,
        )

    @classmethod
    def delete_post(cls, *, post_id: Optional[str] = None) -> PostFields:
        return PostFields(field_name="deletePost", post_id=post_id)
