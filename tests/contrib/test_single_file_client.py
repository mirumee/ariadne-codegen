from textwrap import dedent

import pytest
import toml
from graphql import GraphQLSchema

from ariadne_codegen.contrib.single_file_client import (
    SingleFileClientPlugin,
    merge_files,
)


@pytest.fixture
def config_dict(tmp_path):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    generated_client_path = tmp_path / "generated_client"
    generated_client_path.mkdir()
    return {
        "tool": {
            "ariadne-codegen": {
                "schema_path": schema_path.as_posix(),
                "queries_path": queries_path.as_posix(),
                "target_package_path": tmp_path.as_posix(),
                "target_package_name": "generated_client",
                "include_comments": "none",
            }
        }
    }


def test_config_parsing(config_dict):
    dict_ = config_dict.copy()

    config = """
    [tool.ariadne-codegen.single-file-client]
    output_file_name = "my_client.py"
    should_remove_package = false
    """
    config_update = toml.loads(config)

    dict_["tool"]["ariadne-codegen"].update(config_update["tool"]["ariadne-codegen"])

    plugin = SingleFileClientPlugin(GraphQLSchema(), config_dict)

    assert plugin.module_name == "my_client.py"
    assert plugin.should_remove_package is False


BASE_MODEL = """
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class UnsetType:
    def __bool__(self) -> bool:
        return False


UNSET = UnsetType()


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        protected_namespaces=(),
    )
"""

ASYNC_BASE_CLIENT = """
from pydantic import BaseModel as PydanticBaseModel
from .base_model import UNSET

class AsyncBaseClient:
    def foo():
        return PydanticBaseModel()

"""

GET_AUTHENTICATED_USER = """
from .base_model import BaseModel

class GetAuthenticatedUser(BaseModel):
    pass
"""


CLIENT = '''
from typing import Any

from .async_base_client import AsyncBaseClient
from .get_authenticated_user import GetAuthenticatedUser


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_authenticated_user(self, **kwargs: Any) -> GetAuthenticatedUser:
        query = gql("""
            query GetAuthenticatedUser {
              me {
                id
                username
              }
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetAuthenticatedUser",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetAuthenticatedUser.model_validate(data)

'''

FILES = {
    "base_model.py": BASE_MODEL,
    "async_base_client.py": ASYNC_BASE_CLIENT,
    "get_authenticated_user.py": GET_AUTHENTICATED_USER,
    "client.py": CLIENT,
}


def _generate_package_files(
    generated_client_path,
):
    files = []
    for file_name, file_content in FILES.items():
        file = generated_client_path / file_name
        file.write_text(dedent(file_content))
        files.append(file)
    return files


def test_single_file_client(tmp_path, config_dict):
    generated_client_path = tmp_path / "generated_client"
    _generate_package_files(generated_client_path)

    plugin = SingleFileClientPlugin(GraphQLSchema(), config_dict)

    result = plugin.generate_files(list(FILES.keys()))

    assert not generated_client_path.is_dir()

    assert len(result) == 1
    generated_module = tmp_path / result[0]
    assert generated_module == plugin.module_path
    assert generated_module.is_file()
    assert generated_module.read_text().startswith("from typing import Any")


def test_merge_files(tmp_path):
    generated_client_path = tmp_path / "generated_client"
    generated_client_path.mkdir()
    files = _generate_package_files(generated_client_path)

    code = merge_files(files)
    assert code == dedent(
        '''from typing import Any

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class UnsetType:
    def __bool__(self) -> bool:
        return False


UNSET = UnsetType()


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        protected_namespaces=(),
    )


class AsyncBaseClient:
    def foo():
        return PydanticBaseModel()


class GetAuthenticatedUser(BaseModel):
    pass


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_authenticated_user(self, **kwargs: Any) -> GetAuthenticatedUser:
        query = gql("""
            query GetAuthenticatedUser {
              me {
                id
                username
              }
            }
            """)
        variables: dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="GetAuthenticatedUser",
            variables=variables,
            **kwargs,
        )
        data = self.get_data(response)
        return GetAuthenticatedUser.model_validate(data)
'''
    )
