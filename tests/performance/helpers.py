"""Shared helpers for the performance guards.

These tests compare two ways of doing the same thing and assert a ratio, rather
than asserting an absolute duration, so that they stay meaningful on machines of
wildly different speed. Every threshold is set well below the ratio the change
actually delivers, so what they catch is a change of *mechanism* (somebody
re-introducing eager `model_rebuild()` calls, or per-file ruff spawns), not a
slow CI runner.
"""

import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
from click.testing import CliRunner

from ariadne_codegen.main import main

# Number of fresh-subprocess timings to take per measurement; the smallest is
# used, which is far more stable than a mean when the noise is all one-sided.
TIMING_REPEATS = 3


def report(request: pytest.FixtureRequest, title: str, rows: list[str]) -> None:
    """Print a comparison table through the terminal reporter.

    Written straight to the reporter rather than with `print`, so the numbers
    show up on a normal run instead of only under `-s`.
    """
    reporter = request.config.pluginmanager.get_plugin("terminalreporter")
    if reporter is None:
        return
    reporter.ensure_newline()
    reporter.write_line(f"  {title}")
    for row in rows:
        reporter.write_line(f"    {row}")


def generate_package(project_dir: Path, package_name: str, settings: str = "") -> Path:
    """Run codegen in `project_dir` and return the generated package path."""
    (project_dir / "pyproject.toml").write_text(
        textwrap.dedent(
            f"""\
            [tool.ariadne-codegen]
            schema_path = "schema.graphql"
            queries_path = "queries.graphql"
            include_comments = "none"
            target_package_name = "{package_name}"
            """
        )
        + settings
    )

    old_cwd = Path.cwd()
    os.chdir(project_dir)
    try:
        result = CliRunner().invoke(main)
        assert result.exit_code == 0, result.output
    finally:
        os.chdir(old_cwd)

    package_path = project_dir / package_name
    assert package_path.is_dir()
    return package_path


def measure_import_seconds(project_dir: Path, package_name: str) -> float:
    """Import the package in a fresh interpreter; return the best wall-clock time."""
    script = textwrap.dedent(
        f"""
        import time
        start = time.perf_counter()
        import {package_name}  # noqa: F401
        print(time.perf_counter() - start)
        """
    )
    best = float("inf")
    for _ in range(TIMING_REPEATS):
        completed = subprocess.run(
            [sys.executable, "-c", script],
            cwd=project_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        best = min(best, float(completed.stdout.strip().splitlines()[-1]))
    return best
