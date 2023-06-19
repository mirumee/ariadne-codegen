import ast
from pathlib import Path

import pytest

import ariadne_codegen.client_generators.dependencies.base_model as base_model_module
from ariadne_codegen.client_generators.constants import (
    BASE_MODEL_CLASS_NAME,
    UPLOAD_CLASS_NAME,
)


@pytest.fixture
def base_model_import():
    return ast.ImportFrom(
        module=Path(base_model_module.__file__).stem,
        names=[ast.alias(BASE_MODEL_CLASS_NAME)],
        level=1,
    )


@pytest.fixture
def upload_import():
    return ast.ImportFrom(
        module=Path(base_model_module.__file__).stem,
        names=[ast.alias(UPLOAD_CLASS_NAME)],
        level=1,
    )
