import os
from importlib.metadata import version
from pathlib import Path
from typing import List

import httpx
import pytest
from click.testing import CliRunner

from ariadne_codegen.exceptions import (
    InvalidConfiguration,
    InvalidOperationForSchema,
    MissingConfiguration,
)
from ariadne_codegen.main import main

CLIENTS_PATH = Path(__file__).parent / "clients"
GRAPHQL_SCHEMAS_PATH = Path(__file__).parent / "graphql_schemas"


@pytest.fixture(scope="function")
def project_dir(request, tmp_path):
    pyproject_path, files_to_copy = request.param
    tmp_path.joinpath("pyproject.toml").write_text(pyproject_path.read_text())
    copy_files(files_to_copy, tmp_path)

    old_cwd = Path.cwd()
    os.chdir(tmp_path)

    yield tmp_path

    os.chdir(old_cwd)


def copy_files(files_to_copy: List[Path], target_dir: Path):
    for file_ in files_to_copy:
        target_dir.joinpath(file_.name).write_text(file_.read_text())


def assert_the_same_files_in_directories(dir1: Path, dir2: Path):
    files1 = {f for f in dir1.glob("*") if f.name != "__pycache__"}
    assert {f.name for f in files1} == {
        f.name for f in dir2.glob("*") if f.name != "__pycache__"
    }

    for file_ in files1:
        content1 = file_.read_text()
        content2 = dir2.joinpath(file_.name).read_text()
        assert content1 == content2, file_.name


def test_main_shows_version():
    result = CliRunner().invoke(main, "--version")

    assert result.exit_code == 0
    assert version("ariadne-codegen") in result.output


@pytest.mark.parametrize(
    "project_dir, package_name, expected_package_path",
    [
        (
            (
                CLIENTS_PATH / "example" / "pyproject.toml",
                (
                    CLIENTS_PATH / "example" / "queries.graphql",
                    CLIENTS_PATH / "example" / "schema.graphql",
                ),
            ),
            "example_client",
            CLIENTS_PATH / "example" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "extended_models" / "pyproject.toml",
                (
                    CLIENTS_PATH / "extended_models" / "queries.graphql",
                    CLIENTS_PATH / "extended_models" / "schema.graphql",
                    CLIENTS_PATH / "extended_models" / "common_mixins.py",
                    CLIENTS_PATH / "extended_models" / "mixins_a.py",
                    CLIENTS_PATH / "extended_models" / "mixins_b.py",
                ),
            ),
            "client_with_extended_models",
            CLIENTS_PATH / "extended_models" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "custom_files_names" / "pyproject.toml",
                (
                    CLIENTS_PATH / "custom_files_names" / "queries.graphql",
                    CLIENTS_PATH / "custom_files_names" / "schema.graphql",
                ),
            ),
            "custom_names_client",
            CLIENTS_PATH / "custom_files_names" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "custom_base_client" / "pyproject.toml",
                (
                    CLIENTS_PATH / "custom_base_client" / "queries.graphql",
                    CLIENTS_PATH / "custom_base_client" / "schema.graphql",
                    CLIENTS_PATH / "custom_base_client" / "custom_base_client.py",
                ),
            ),
            "custom_base_client",
            CLIENTS_PATH / "custom_base_client" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "custom_scalars" / "pyproject.toml",
                (
                    CLIENTS_PATH / "custom_scalars" / "queries.graphql",
                    CLIENTS_PATH / "custom_scalars" / "schema.graphql",
                    CLIENTS_PATH / "custom_scalars" / "custom_scalars.py",
                ),
            ),
            "custom_scalars_client",
            CLIENTS_PATH / "custom_scalars" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "inline_fragments" / "pyproject.toml",
                (
                    CLIENTS_PATH / "inline_fragments" / "queries.graphql",
                    CLIENTS_PATH / "inline_fragments" / "schema.graphql",
                ),
            ),
            "inline_fragments_client",
            CLIENTS_PATH / "inline_fragments" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "multiple_fragments" / "pyproject.toml",
                (
                    CLIENTS_PATH / "multiple_fragments" / "queries.graphql",
                    CLIENTS_PATH / "multiple_fragments" / "schema.graphql",
                ),
            ),
            "multiple_fragments_client",
            CLIENTS_PATH / "multiple_fragments" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "shorter_results" / "pyproject.toml",
                (
                    CLIENTS_PATH / "shorter_results" / "queries.graphql",
                    CLIENTS_PATH / "shorter_results" / "schema.graphql",
                    CLIENTS_PATH / "shorter_results" / "custom_scalars.py",
                ),
            ),
            "shorter_results",
            CLIENTS_PATH / "shorter_results" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "fragments_on_abstract_types" / "pyproject.toml",
                (
                    CLIENTS_PATH / "fragments_on_abstract_types" / "queries.graphql",
                    CLIENTS_PATH / "fragments_on_abstract_types" / "schema.graphql",
                ),
            ),
            "fragments_on_abstract_types_client",
            CLIENTS_PATH / "fragments_on_abstract_types" / "expected_client",
        ),
    ],
    indirect=["project_dir"],
)
def test_main_generates_correct_package(
    project_dir, package_name, expected_package_path
):
    result = CliRunner().invoke(main)

    assert result.exit_code == 0
    package_path = project_dir / package_name
    assert package_path.is_dir()
    assert_the_same_files_in_directories(package_path, expected_package_path)


@pytest.mark.parametrize(
    "project_dir, expected_exception",
    [
        (
            (CLIENTS_PATH / "invalid_pyprojects" / "no_section.toml", ()),
            MissingConfiguration,
        ),
        (
            (CLIENTS_PATH / "invalid_pyprojects" / "no_files.toml", ()),
            InvalidConfiguration,
        ),
        (
            (
                CLIENTS_PATH
                / "invalid_pyprojects"
                / "operation_not_valid_for_schema.toml",
                (
                    CLIENTS_PATH / "invalid_pyprojects" / "schema.graphql",
                    CLIENTS_PATH / "invalid_pyprojects" / "not_valid_query.graphql",
                ),
            ),
            InvalidOperationForSchema,
        ),
    ],
    indirect=["project_dir"],
)
def test_main_raises_exception(
    project_dir, expected_exception
):  # pylint: disable=W0613
    with pytest.raises(expected_exception):
        CliRunner().invoke(main, catch_exceptions=False)


@pytest.mark.parametrize(
    "project_dir, package_name, expected_package_path",
    [
        (
            (
                CLIENTS_PATH / "remote_schema" / "pyproject.toml",
                (CLIENTS_PATH / "remote_schema" / "queries.graphql",),
            ),
            "remote_schema_client",
            CLIENTS_PATH / "remote_schema" / "expected_client",
        )
    ],
    indirect=["project_dir"],
)
def test_main_uses_remote_schema_url_and_remote_schema_headers(
    mocker, project_dir, package_name, expected_package_path
):  # pylint: disable=W0613
    introspection_response_contenct = CLIENTS_PATH.joinpath(
        "remote_schema", "response.json"
    ).read_bytes()
    mocked_post = mocker.patch(
        "httpx.post",
        return_value=httpx.Response(
            status_code=200, content=introspection_response_contenct
        ),
    )

    result = CliRunner().invoke(main, catch_exceptions=False)

    assert result.exit_code == 0
    package_path = project_dir / package_name
    assert package_path.is_dir()
    assert_the_same_files_in_directories(package_path, expected_package_path)
    assert mocked_post.called_with(
        url="http://test/graphql/", headers={"header1": "value1", "header2": "value2"}
    )


def test_main_can_read_config_from_provided_file(tmp_path):
    old_cwd = Path.cwd()
    files_to_copy = (
        CLIENTS_PATH / "custom_config_file" / "config.toml",
        CLIENTS_PATH / "custom_config_file" / "queries.graphql",
        CLIENTS_PATH / "custom_config_file" / "schema.graphql",
    )
    copy_files(files_to_copy, tmp_path)
    expected_client_path = CLIENTS_PATH / "custom_config_file" / "expected_client"
    package_name = "custom_config_client"

    os.chdir(tmp_path)
    result = CliRunner().invoke(
        main, args="--config config.toml", catch_exceptions=False
    )
    os.chdir(old_cwd)

    assert result.exit_code == 0
    package_path = tmp_path / package_name
    assert package_path.is_dir()
    assert_the_same_files_in_directories(package_path, expected_client_path)


@pytest.mark.parametrize(
    "project_dir, file_name, expected_file_path",
    [
        (
            (
                GRAPHQL_SCHEMAS_PATH / "example" / "pyproject.toml",
                (GRAPHQL_SCHEMAS_PATH / "example" / "schema.graphql",),
            ),
            "example_schema.py",
            GRAPHQL_SCHEMAS_PATH / "example" / "expected_schema.py",
        ),
        (
            (
                GRAPHQL_SCHEMAS_PATH / "all_types" / "pyproject.toml",
                (GRAPHQL_SCHEMAS_PATH / "all_types" / "schema.graphql",),
            ),
            "schema.py",
            GRAPHQL_SCHEMAS_PATH / "all_types" / "expected_schema.py",
        ),
    ],
    indirect=["project_dir"],
)
def test_main_generates_correct_schema_file(project_dir, file_name, expected_file_path):
    result = CliRunner().invoke(main, "graphqlschema")

    assert result.exit_code == 0
    schema_path = project_dir / file_name

    assert schema_path.read_text() == expected_file_path.read_text()
