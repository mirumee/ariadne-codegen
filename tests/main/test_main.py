import os
from importlib.metadata import version
from pathlib import Path

import httpx
import pytest
from click.testing import CliRunner

from ariadne_codegen.exceptions import (
    InvalidConfiguration,
    MissingConfiguration,
    ParsingError,
)
from ariadne_codegen.main import main


@pytest.fixture(scope="function")
def project_dir(request, tmp_path):
    pyproject_path, files_to_copy = request.param
    tmp_path.joinpath("pyproject.toml").write_text(pyproject_path.read_text())
    for file_ in files_to_copy:
        tmp_path.joinpath(file_.name).write_text(file_.read_text())

    old_cwd = Path.cwd()
    os.chdir(tmp_path)

    yield tmp_path

    os.chdir(old_cwd)


def assert_the_same_files_in_directories(dir1: Path, dir2: Path):
    files1 = [f for f in dir1.glob("*") if f.name != "__pycache__"]
    assert [f.name for f in files1] == [
        f.name for f in dir2.glob("*") if f.name != "__pycache__"
    ]

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
                Path(__file__).parent / "example" / "pyproject.toml",
                (
                    Path(__file__).parent / "example" / "queries.graphql",
                    Path(__file__).parent / "example" / "schema.graphql",
                ),
            ),
            "example_client",
            Path(__file__).parent / "example" / "expected_client",
        ),
        (
            (
                Path(__file__).parent / "extended_models" / "pyproject.toml",
                (
                    Path(__file__).parent / "extended_models" / "queries.graphql",
                    Path(__file__).parent / "extended_models" / "schema.graphql",
                    Path(__file__).parent / "extended_models" / "common_mixins.py",
                    Path(__file__).parent / "extended_models" / "mixins_a.py",
                    Path(__file__).parent / "extended_models" / "mixins_b.py",
                ),
            ),
            "client_with_extended_models",
            Path(__file__).parent / "extended_models" / "expected_client",
        ),
        (
            (
                Path(__file__).parent / "custom_files_names" / "pyproject.toml",
                (
                    Path(__file__).parent / "custom_files_names" / "queries.graphql",
                    Path(__file__).parent / "custom_files_names" / "schema.graphql",
                ),
            ),
            "custom_names_client",
            Path(__file__).parent / "custom_files_names" / "expected_client",
        ),
        (
            (
                Path(__file__).parent / "custom_base_client" / "pyproject.toml",
                (
                    Path(__file__).parent / "custom_base_client" / "queries.graphql",
                    Path(__file__).parent / "custom_base_client" / "schema.graphql",
                    Path(__file__).parent
                    / "custom_base_client"
                    / "custom_base_client.py",
                ),
            ),
            "custom_base_client",
            Path(__file__).parent / "custom_base_client" / "expected_client",
        ),
        (
            (
                Path(__file__).parent / "custom_scalars" / "pyproject.toml",
                (
                    Path(__file__).parent / "custom_scalars" / "queries.graphql",
                    Path(__file__).parent / "custom_scalars" / "schema.graphql",
                    Path(__file__).parent / "custom_scalars" / "custom_scalars.py",
                ),
            ),
            "custom_scalars_client",
            Path(__file__).parent / "custom_scalars" / "expected_client",
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
            (Path(__file__).parent / "invalid_pyprojects" / "no_section.toml", ()),
            MissingConfiguration,
        ),
        (
            (Path(__file__).parent / "invalid_pyprojects" / "no_files.toml", ()),
            InvalidConfiguration,
        ),
        (
            (
                Path(__file__).parent
                / "invalid_pyprojects"
                / "operation_not_valid_for_schema.toml",
                (
                    Path(__file__).parent / "invalid_pyprojects" / "schema.graphql",
                    Path(__file__).parent
                    / "invalid_pyprojects"
                    / "not_valid_query.graphql",
                ),
            ),
            ParsingError,
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
                Path(__file__).parent / "remote_schema" / "pyproject.toml",
                (Path(__file__).parent / "remote_schema" / "queries.graphql",),
            ),
            "remote_schema_client",
            Path(__file__).parent / "remote_schema" / "expected_client",
        )
    ],
    indirect=["project_dir"],
)
def test_main_uses_remote_schema_url_and_remote_schema_headers(
    mocker, project_dir, package_name, expected_package_path
):  # pylint: disable=W0613
    introspection_response_contenct = (
        Path(__file__).parent.joinpath("remote_schema", "response.json").read_bytes()
    )
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
