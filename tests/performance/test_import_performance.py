"""Timing guards for how long a generated package takes to import.

Three settings make that cheaper, and they attack different costs:

`defer_model_build` stops pydantic building every model's core schema at import.
Because each model inlines the schemas of the types it references, that cost grows
super-linearly with the schema.

`use_alias_generator` removes the `Field(alias=...)` call from every field whose
GraphQL name `to_camel` can reconstruct. Each of those calls builds two `FieldInfo`
objects at import, so the cost is linear in the number of fields.

`lazy_imports` stops the package importing the modules at all until a name from one
is used. The other two make defining a model cheaper; this one skips the models an
application never touches. It is measured by reaching the client rather than by the
bare import, which is ~0 ms once nothing is imported eagerly.

Marked `performance`, so they can be run on their own:

    hatch test -- -m performance
"""

from pathlib import Path
from typing import NamedTuple

import pytest

from .helpers import generate_package, measure_import_seconds, report

pytestmark = pytest.mark.performance

# Schema size. Large enough that model definition clearly dominates the fixed cost
# of importing pydantic/httpx/graphql, small enough that generating it three times
# stays fast. The build cost is dominated by the number of fields per model, so we
# use many models each with a wide set of fields. Every model keeps a single self
# forward reference so the eager variant still emits `model_rebuild()` calls.
NUMBER_OF_MODELS = 300
FIELDS_PER_MODEL = 20
NUMBER_OF_HUBS = 6

# Ratios the changes really deliver on this schema, measured over 7 trials:
#   eager -> defer               1.91x .. 1.97x
#   defer -> defer+alias         1.48x .. 1.56x
#   eager -> defer+alias         ~3.0x
#   defer+alias -> +lazy         ~3.8x   (reaching the client, not the bare import)
# The thresholds sit well under the low end of each range.
MIN_DEFER_SPEEDUP = 1.5
MIN_ALIAS_GENERATOR_SPEEDUP = 1.2
MIN_COMBINED_SPEEDUP = 2.0
MIN_LAZY_IMPORTS_SPEEDUP = 2.0

# The operation takes an input argument, so `client.py` imports a type out of
# `input_types` to annotate it with. That is what `lazy_imports` has to get out of
# the module level, and an operation with no arguments would not exercise it.
QUERIES = "query Ping($filter: Model0) {\n    ping(filter: $filter)\n}\n"

VARIANTS = {
    "eager": "",
    "defer": "defer_model_build = true\n",
    "defer+alias": "defer_model_build = true\nuse_alias_generator = true\n",
    "defer+alias+lazy": (
        "defer_model_build = true\nuse_alias_generator = true\nlazy_imports = true\n"
    ),
}


class Variant(NamedTuple):
    seconds: float
    client_seconds: float
    package_path: Path


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


@pytest.fixture(scope="module")
def timings(tmp_path_factory) -> dict[str, Variant]:
    """Generate each variant once, and time importing it."""
    schema = _build_schema()
    results = {}
    for variant, settings in VARIANTS.items():
        package_name = variant.replace("+", "_") + "_client"
        project_dir = tmp_path_factory.mktemp(package_name)
        (project_dir / "schema.graphql").write_text(schema)
        (project_dir / "queries.graphql").write_text(QUERIES)
        package_path = generate_package(project_dir, package_name, settings)
        results[variant] = Variant(
            seconds=measure_import_seconds(project_dir, package_name),
            client_seconds=measure_import_seconds(
                project_dir, package_name, reach_client=True
            ),
            package_path=package_path,
        )
    return results


def test_import_timings_are_reported(request, timings):
    """Not an assertion so much as the numbers the other tests are asserting on."""
    slowest = timings["eager"].seconds
    rows = [
        f"{variant:17s} import {values.seconds * 1000:7.1f} ms"
        f" ({slowest / values.seconds:5.2f}x vs eager)"
        f"   + reach client {values.client_seconds * 1000:7.1f} ms"
        f" ({timings['eager'].client_seconds / values.client_seconds:5.2f}x)"
        for variant, values in timings.items()
    ]
    fields_per_model = FIELDS_PER_MODEL + FIELDS_PER_MODEL // 2 + NUMBER_OF_HUBS + 2
    report(
        request,
        f"import of a generated package "
        f"({NUMBER_OF_MODELS} models, {fields_per_model} fields each)",
        rows,
    )


def test_defer_model_build_speeds_up_import(timings):
    eager = timings["eager"]
    deferred = timings["defer"]

    # Tie the timing to the mechanism: without this, a no-op change to the setting
    # would still "pass" whenever the machine happened to be fast.
    assert any(
        "model_rebuild()" in path.read_text()
        for path in eager.package_path.glob("*.py")
    ), "expected the eager package to contain model_rebuild() calls"
    assert all(
        "model_rebuild()" not in path.read_text()
        for path in deferred.package_path.glob("*.py")
    ), "deferred package must not contain model_rebuild() calls"

    speedup = eager.seconds / deferred.seconds
    assert speedup >= MIN_DEFER_SPEEDUP, (
        f"defer_model_build import not fast enough: "
        f"eager={eager.seconds:.3f}s deferred={deferred.seconds:.3f}s "
        f"speedup={speedup:.2f}x (expected >= {MIN_DEFER_SPEEDUP}x)"
    )


def test_alias_generator_speeds_up_import_on_top_of_defer(timings):
    deferred = timings["defer"]
    with_alias = timings["defer+alias"]

    # Every field name in this schema round-trips through `to_camel`, so the
    # setting should have removed all of them.
    assert (deferred.package_path / "input_types.py").read_text().count("alias=")
    assert (
        not (with_alias.package_path / "input_types.py").read_text().count("alias=")
    ), "expected use_alias_generator to remove every explicit Field(alias=...)"

    speedup = deferred.seconds / with_alias.seconds
    assert speedup >= MIN_ALIAS_GENERATOR_SPEEDUP, (
        f"use_alias_generator import not fast enough: "
        f"deferred={deferred.seconds:.3f}s with_alias={with_alias.seconds:.3f}s "
        f"speedup={speedup:.2f}x (expected >= {MIN_ALIAS_GENERATOR_SPEEDUP}x)"
    )


def test_defer_model_build_and_alias_generator_compose(timings):
    eager = timings["eager"].seconds
    both = timings["defer+alias"].seconds

    speedup = eager / both
    assert speedup >= MIN_COMBINED_SPEEDUP, (
        f"the two settings together are not fast enough: "
        f"eager={eager:.3f}s both={both:.3f}s "
        f"speedup={speedup:.2f}x (expected >= {MIN_COMBINED_SPEEDUP}x)"
    )


def test_lazy_imports_speeds_up_reaching_the_client_on_top_of_defer_and_alias(timings):
    """`lazy_imports` is measured by reaching the client, not by the bare import.

    The bare import is ~0 ms once nothing is imported eagerly, which would make any
    ratio look spectacular without proving an application got faster. Reaching the
    client is the smallest thing that has to pay for what the import deferred.
    """
    baseline = timings["defer+alias"]
    lazy = timings["defer+alias+lazy"]

    # Tie the timing to the mechanism, and to *both* halves of it: the lazy init
    # stops the package importing every module, and the plugin the setting turns on
    # stops `client.py` importing the input types it only names in annotations.
    # Either one alone leaves the other pulling the models in.
    lazy_init = (lazy.package_path / "__init__.py").read_text()
    assert "_LAZY_IMPORTS" in lazy_init, "expected a lazy __init__"
    assert "def __getattr__(name):" in lazy_init

    baseline_client = (baseline.package_path / "client.py").read_text()
    lazy_client = (lazy.package_path / "client.py").read_text()
    assert "from .input_types import" in baseline_client
    assert "if TYPE_CHECKING:" in lazy_client, (
        "expected lazy_imports to enable the ClientForwardRefsPlugin"
    )
    input_types_import = "from .input_types import"
    assert input_types_import not in lazy_client.split("if TYPE_CHECKING:")[0], (
        "client.py must not import input types at module level"
    )

    speedup = baseline.client_seconds / lazy.client_seconds
    assert speedup >= MIN_LAZY_IMPORTS_SPEEDUP, (
        f"lazy_imports not fast enough: "
        f"baseline={baseline.client_seconds:.3f}s lazy={lazy.client_seconds:.3f}s "
        f"speedup={speedup:.2f}x (expected >= {MIN_LAZY_IMPORTS_SPEEDUP}x)"
    )
