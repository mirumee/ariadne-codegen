from typing import Optional

from .custom_fields import PostFields, UserFields
from .input_types import AddUserInput, UpdateUserInput


class Mutation:
    @classmethod
    def add_user(cls, user_input: AddUserInput) -> UserFields:
        return UserFields(
            field_name="addUser",
            arguments={"user_input": {"type": "AddUserInput!", "value": user_input}},
        )

    @classmethod
    def update_user(cls, user_id: str, user_input: UpdateUserInput) -> UserFields:
        return UserFields(
            field_name="updateUser",
            arguments={
                "user_id": {"type": "ID!", "value": user_id},
                "user_input": {"type": "UpdateUserInput!", "value": user_input},
            },
        )

    @classmethod
    def delete_user(cls, user_id: str) -> UserFields:
        return UserFields(
            field_name="deleteUser",
            arguments={"user_id": {"type": "ID!", "value": user_id}},
        )

    @classmethod
    def add_post(
        cls, title: str, content: str, author_id: str, published_at: str
    ) -> PostFields:
        return PostFields(
            field_name="addPost",
            arguments={
                "title": {"type": "String!", "value": title},
                "content": {"type": "String!", "value": content},
                "authorId": {"type": "ID!", "value": author_id},
                "publishedAt": {"type": "String!", "value": published_at},
            },
        )

    @classmethod
    def update_post(
        cls,
        post_id: str,
        *,
        title: Optional[str] = None,
        content: Optional[str] = None,
        published_at: Optional[str] = None
    ) -> PostFields:
        return PostFields(
            field_name="updatePost",
            arguments={
                "post_id": {"type": "ID!", "value": post_id},
                "title": {"type": "String", "value": title},
                "content": {"type": "String", "value": content},
                "publishedAt": {"type": "String", "value": published_at},
            },
        )

    @classmethod
    def delete_post(cls, post_id: str) -> PostFields:
        return PostFields(
            field_name="deletePost",
            arguments={"post_id": {"type": "ID!", "value": post_id}},
        )
