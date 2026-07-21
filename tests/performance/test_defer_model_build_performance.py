"""Performance guards for the ``defer_model_build`` setting.

These tests generate a large, densely interconnected client both with and
without ``defer_model_build`` and compare how long the generated package takes
to *import*. With eager model building Pydantic constructs every model's
core-schema at import time, and because each model inlines the schemas of the
types it references that cost grows super-linearly with a big schema. Deferring
the build moves that work to first use, so importing the package becomes
dramatically cheaper.

The assertions are deliberately ratio-based (and use a generous margin) so they
guard against regressions - i.e. someone accidentally re-introducing eager
``model_rebuild()`` calls - without being flaky across machines.

Marked ``performance`` so they can be selected/deselected explicitly:

    hatch test -- -m performance
"""

import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
from click.testing import CliRunner

from ariadne_codegen.main import main

# Schema size. Large enough that eager building is clearly more expensive than
# deferred, small enough that generating it twice stays fast in CI. The build
# cost is dominated by the number of fields per model, so we use many models
# each with a wide set of fields. Every model keeps a single self forward
# reference so the eager variant still emits ``model_rebuild()`` calls.
NUMBER_OF_MODELS = 300
FIELDS_PER_MODEL = 20
NUMBER_OF_HUBS = 6

# Deferred import must be at least this many times faster than eager. On this
# schema the real ratio is ~2x; if eager ``model_rebuild()`` calls are ever
# re-introduced for the deferred variant the ratio collapses to ~1x, which this
# bound catches while staying stable on slow/noisy CI runners.
MIN_SPEEDUP = 1.5

# Number of fresh-subprocess import timings to take per package; the smallest is
# used to reduce the impact of scheduler noise.
TIMING_REPEATS = 3


def _build_schema() -> str:
    lines = [
        "schema { query: Query }",
        "type Query { ping(filter: Model0): String }",
    ]
    for hub in range(NUMBER_OF_HUBS):
        lines.append(
            f"input Hub{hub} {{ id: Int name: String value: Float flag: Boolean }}"
        )
    for i in range(NUMBER_OF_MODELS):
        fields = [f"f{k}: String" for k in range(FIELDS_PER_MODEL)]
        fields += [f"i{k}: Int" for k in range(FIELDS_PER_MODEL // 2)]
        fields += [f"rel{hub}: Hub{hub}" for hub in range(NUMBER_OF_HUBS)]
        fields.append(f"selfRef: Model{i}")
        fields.append(f"children: [Model{i}!]")
        lines.append("input Model{} {{ {} }}".format(i, " ".join(fields)))
    return "\n".join(lines)


QUERIES = "query Ping {\n    ping\n}\n"


def _pyproject(package_name: str, defer: bool) -> str:
    return textwrap.dedent(
        f"""\
        [tool.ariadne-codegen]
        schema_path = "schema.graphql"
        queries_path = "queries.graphql"
        include_comments = "none"
        target_package_name = "{package_name}"
        defer_model_build = {"true" if defer else "false"}
        """
    )


def _generate_package(project_dir: Path, package_name: str, defer: bool) -> Path:
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "schema.graphql").write_text(_build_schema())
    (project_dir / "queries.graphql").write_text(QUERIES)
    (project_dir / "pyproject.toml").write_text(_pyproject(package_name, defer))

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


def _measure_import_seconds(project_dir: Path, package_name: str) -> float:
    """Import the generated package in a fresh interpreter and return the best
    (smallest) wall-clock time across a few repeats."""
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


@pytest.mark.performance
def test_defer_model_build_speeds_up_import(tmp_path):
    eager_dir = tmp_path / "eager"
    deferred_dir = tmp_path / "deferred"

    eager_package = _generate_package(eager_dir, "eager_client", defer=False)
    deferred_package = _generate_package(deferred_dir, "deferred_client", defer=True)

    # Sanity: the eager package builds models at import time (model_rebuild),
    # the deferred one must not.
    assert any(
        "model_rebuild()" in p.read_text() for p in eager_package.glob("*.py")
    ), "expected eager package to contain model_rebuild() calls"
    assert all(
        "model_rebuild()" not in p.read_text() for p in deferred_package.glob("*.py")
    ), "deferred package must not contain model_rebuild() calls"

    eager_seconds = _measure_import_seconds(eager_dir, "eager_client")
    deferred_seconds = _measure_import_seconds(deferred_dir, "deferred_client")

    speedup = eager_seconds / deferred_seconds
    assert speedup >= MIN_SPEEDUP, (
        f"defer_model_build import not fast enough: "
        f"eager={eager_seconds:.3f}s deferred={deferred_seconds:.3f}s "
        f"speedup={speedup:.2f}x (expected >= {MIN_SPEEDUP}x)"
    )
