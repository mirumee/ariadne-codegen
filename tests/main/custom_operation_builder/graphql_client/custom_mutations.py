from typing import Optional

from .custom_fields import PostFields, UserFields
from .input_types import AddUserInput, UpdateUserInput


class Mutation:
    @classmethod
    def add_user(cls, user_input: AddUserInput) -> UserFields:
        arguments = {"user_input": {"type": "AddUserInput!", "value": user_input}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UserFields(field_name="addUser", arguments=cleared_arguments)

    @classmethod
    def update_user(cls, user_id: str, user_input: UpdateUserInput) -> UserFields:
        arguments = {
            "user_id": {"type": "ID!", "value": user_id},
            "user_input": {"type": "UpdateUserInput!", "value": user_input},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UserFields(field_name="updateUser", arguments=cleared_arguments)

    @classmethod
    def delete_user(cls, user_id: str) -> UserFields:
        arguments = {"user_id": {"type": "ID!", "value": user_id}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UserFields(field_name="deleteUser", arguments=cleared_arguments)

    @classmethod
    def add_post(
        cls, title: str, content: str, author_id: str, published_at: str
    ) -> PostFields:
        arguments = {
            "title": {"type": "String!", "value": title},
            "content": {"type": "String!", "value": content},
            "authorId": {"type": "ID!", "value": author_id},
            "publishedAt": {"type": "String!", "value": published_at},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PostFields(field_name="addPost", arguments=cleared_arguments)

    @classmethod
    def update_post(
        cls,
        post_id: str,
        *,
        title: Optional[str] = None,
        content: Optional[str] = None,
        published_at: Optional[str] = None
    ) -> PostFields:
        arguments = {
            "post_id": {"type": "ID!", "value": post_id},
            "title": {"type": "String", "value": title},
            "content": {"type": "String", "value": content},
            "publishedAt": {"type": "String", "value": published_at},
        }
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PostFields(field_name="updatePost", arguments=cleared_arguments)

    @classmethod
    def delete_post(cls, post_id: str) -> PostFields:
        arguments = {"post_id": {"type": "ID!", "value": post_id}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return PostFields(field_name="deletePost", arguments=cleared_arguments)
