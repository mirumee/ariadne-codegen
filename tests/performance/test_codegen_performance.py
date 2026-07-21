"""Guard on how many times generation spawns ruff.

Formatting used to spawn ruff twice per generated file, a spawn count linear in
the size of the package. Ruff is now invoked once per rule-selection group for
the whole package. The test asserts that mechanism, that the spawn count stays
constant as the package grows, rather than wall-clock time, so it does not flake
on a loaded runner.

Marked `performance`, so it can be run on its own:

    hatch test -- -m performance
"""

import subprocess
from pathlib import Path
from unittest import mock

import pytest

import ariadne_codegen.utils as utils

from .helpers import generate_package, report

pytestmark = pytest.mark.performance

# `ariadne_codegen.utils.subprocess` is the stdlib module, so patching its `run`
# patches it everywhere. Hold on to the real one to wrap with.
_REAL_SUBPROCESS_RUN = subprocess.run

# Two package sizes far enough apart that a per-file spawn count could not
# coincide between them.
SMALL_OPERATION_COUNT = 5
LARGE_OPERATION_COUNT = 60

# Ruff runs once per rule-selection group (`I` and `I,F401`), for `check --fix`
# and again for `format`. Nothing here rewrites base_model.py, which would add a
# further pair. The bound matters less than the fact that it does not scale.
MAX_RUFF_SPAWNS = 6


def _build_project(project_dir: Path, operation_count: int) -> None:
    project_dir.mkdir(parents=True, exist_ok=True)
    types = "\n".join(f"type T{i} {{ a: String b: Int }}" for i in range(20))
    query_fields = " ".join(
        f"get{i}(id: ID!): T{i % 20}" for i in range(operation_count)
    )
    (project_dir / "schema.graphql").write_text(
        f"schema {{ query: Query }}\n{types}\ntype Query {{ {query_fields} }}\n"
    )
    (project_dir / "queries.graphql").write_text(
        "\n".join(
            f"query Op{i}($id: ID!) {{ get{i}(id: $id) {{ a b }} }}"
            for i in range(operation_count)
        )
    )


def _generate_recording_spawns(project_dir: Path) -> tuple[list, Path]:
    with mock.patch.object(utils.subprocess, "run", wraps=_REAL_SUBPROCESS_RUN) as spy:
        package_path = generate_package(project_dir, "codegen_client")
    return spy.call_args_list, package_path


def _ruff_spawns(calls: list) -> list:
    return [
        call
        for call in calls
        if len(call[0][0]) > 1 and call[0][0][1] in ("check", "format")
    ]


def test_ruff_spawn_count_does_not_grow_with_the_package(request, tmp_path):
    """The spawn count is what makes generation scale; wall-clock only reflects it."""
    _build_project(tmp_path / "small", SMALL_OPERATION_COUNT)
    small_calls, small_package = _generate_recording_spawns(tmp_path / "small")

    _build_project(tmp_path / "large", LARGE_OPERATION_COUNT)
    large_calls, large_package = _generate_recording_spawns(tmp_path / "large")

    small_spawns = len(_ruff_spawns(small_calls))
    large_spawns = len(_ruff_spawns(large_calls))
    small_files = len(list(small_package.glob("*.py")))
    large_files = len(list(large_package.glob("*.py")))

    report(
        request,
        "ruff subprocess spawns per generated package",
        [
            f"{small_files:3d} files -> {small_spawns} spawns",
            f"{large_files:3d} files -> {large_spawns} spawns"
            f"   (per-file would be {2 * large_files})",
        ],
    )

    assert large_files > small_files * 2, "the two packages must differ in size"
    assert large_spawns == small_spawns, (
        f"ruff spawn count scales with the package: "
        f"{small_files} files -> {small_spawns} spawns, "
        f"{large_files} files -> {large_spawns} spawns"
    )
    assert large_spawns <= MAX_RUFF_SPAWNS
