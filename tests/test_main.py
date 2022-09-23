from click.testing import CliRunner

from graphql_sdk_gen.main import main


def test_main_shows_version():
    runner = CliRunner()
    result = runner.invoke(main, "--version")
    assert result.exit_code == 0
    assert "0.1.0" in result.output
