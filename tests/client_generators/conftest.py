import ast
from pathlib import Path

import pytest

from ariadne_codegen.client_generators.constants import (
    BASE_MODEL_CLASS_NAME,
    UNSET_NAME,
    UNSET_TYPE_NAME,
    UPLOAD_CLASS_NAME,
)
from ariadne_codegen.client_generators.dependencies import (
    async_base_client,
    base_client,
    base_model,
)


@pytest.fixture
def base_model_import():
    return ast.ImportFrom(
        module=Path(base_model.__file__).stem,
        names=[ast.alias(BASE_MODEL_CLASS_NAME)],
        level=1,
    )


@pytest.fixture
def upload_import():
    return ast.ImportFrom(
        module=Path(base_model.__file__).stem,
        names=[ast.alias(UPLOAD_CLASS_NAME)],
        level=1,
    )


@pytest.fixture
def unset_import():
    return ast.ImportFrom(
        module=Path(base_model.__file__).stem,
        names=[
            ast.alias(UNSET_NAME),
            ast.alias(UNSET_TYPE_NAME),
        ],
        level=1,
    )


@pytest.fixture
def base_client_import():
    return ast.ImportFrom(
        module=Path(base_client.__file__).stem,
        names=[ast.alias("BaseClient")],
        level=1,
    )


@pytest.fixture
def async_base_client_import():
    return ast.ImportFrom(
        module=Path(async_base_client.__file__).stem,
        names=[ast.alias("AsyncBaseClient")],
        level=1,
    )
