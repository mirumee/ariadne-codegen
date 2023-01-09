import os
from pathlib import Path

import pytest
from click.testing import CliRunner

from graphql_sdk_gen.exceptions import (
    InvalidConfiguration,
    MissingConfiguration,
    ParsingError,
)
from graphql_sdk_gen.main import main


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


def test_main_shows_version():
    result = CliRunner().invoke(main, "--version")

    assert result.exit_code == 0
    assert "0.1.0" in result.output


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
