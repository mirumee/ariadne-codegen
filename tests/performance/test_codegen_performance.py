"""Timing guards for how long generation itself takes.

Formatting used to spawn `python -m ruff` twice per generated file: a full Python
interpreter startup per spawn, and a spawn count linear in the size of the
package. Ruff is now invoked as a binary, once per rule-selection group for the
whole package.

Marked `performance`, so they can be run on their own:

    hatch test -- -m performance
"""

import subprocess
import time
from pathlib import Path
from unittest import mock

import pytest

import ariadne_codegen.client_generators.package as package_module
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

# Batching beats formatting each file separately by ~6x on the large package,
# with both using the ruff binary. The threshold leaves a wide margin.
MIN_BATCHING_SPEEDUP = 2.0

TIMING_REPEATS = 2


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


def test_ruff_is_not_spawned_through_a_python_interpreter(tmp_path):
    """`python -m ruff` costs a full interpreter startup on every call."""
    _build_project(tmp_path, SMALL_OPERATION_COUNT)

    calls, _ = _generate_recording_spawns(tmp_path)

    assert _ruff_spawns(calls), "expected generation to run ruff"
    for call in calls:
        argv = call[0][0]
        assert "-m" not in argv[:2], f"ruff spawned through an interpreter: {argv[:3]}"


def test_batched_formatting_beats_formatting_each_file(request, monkeypatch, tmp_path):
    _build_project(tmp_path, LARGE_OPERATION_COUNT)
    generate_package(tmp_path, "codegen_client")  # warm caches and the filesystem

    batched = min(_time_generation(tmp_path) for _ in range(TIMING_REPEATS))

    def _format_each_file(codes, *, remove_unused_imports=True):
        return [
            utils._format_code(code, remove_unused_imports=remove_unused_imports)
            for code in codes
        ]

    monkeypatch.setattr(package_module, "format_many", _format_each_file)
    per_file = min(_time_generation(tmp_path) for _ in range(TIMING_REPEATS))

    speedup = per_file / batched
    report(
        request,
        f"generation of a {LARGE_OPERATION_COUNT}-operation package",
        [
            f"one ruff pass per file  {per_file:5.2f}s",
            f"one ruff pass per group {batched:5.2f}s   ({speedup:.2f}x)",
        ],
    )
    assert speedup >= MIN_BATCHING_SPEEDUP, (
        f"batched formatting not fast enough: per_file={per_file:.3f}s "
        f"batched={batched:.3f}s speedup={speedup:.2f}x "
        f"(expected >= {MIN_BATCHING_SPEEDUP}x)"
    )


def _time_generation(project_dir: Path) -> float:
    start = time.perf_counter()
    generate_package(project_dir, "codegen_client")
    return time.perf_counter() - start
