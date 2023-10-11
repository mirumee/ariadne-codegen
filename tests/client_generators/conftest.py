import ast
from pathlib import Path

import pytest

from ariadne_codegen.client_generators.dependencies import (
    async_base_client,
    base_client,
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
