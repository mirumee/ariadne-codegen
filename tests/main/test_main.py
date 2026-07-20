import ast
import importlib
import json
import os
import subprocess
import sys
import textwrap
from importlib.metadata import version
from pathlib import Path

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


def copy_files(files_to_copy: list[Path], target_dir: Path):
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
        (
            (
                CLIENTS_PATH / "operations" / "pyproject.toml",
                (
                    CLIENTS_PATH / "operations" / "queries.graphql",
                    CLIENTS_PATH / "operations" / "schema.graphql",
                ),
            ),
            "client_with_operations",
            CLIENTS_PATH / "operations" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "only_used_inputs_and_enums" / "pyproject.toml",
                (
                    CLIENTS_PATH / "only_used_inputs_and_enums" / "queries.graphql",
                    CLIENTS_PATH / "only_used_inputs_and_enums" / "schema.graphql",
                ),
            ),
            "client_only_used_inputs_and_enums",
            CLIENTS_PATH / "only_used_inputs_and_enums" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "interface_as_fragment" / "pyproject.toml",
                (
                    CLIENTS_PATH / "interface_as_fragment" / "queries.graphql",
                    CLIENTS_PATH / "interface_as_fragment" / "schema.graphql",
                ),
            ),
            "interface_as_fragment",
            CLIENTS_PATH / "interface_as_fragment" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "custom_query_builder" / "pyproject.toml",
                (CLIENTS_PATH / "custom_query_builder" / "schema.graphql",),
            ),
            "example_client",
            CLIENTS_PATH / "custom_query_builder" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "custom_sync_query_builder" / "pyproject.toml",
                (CLIENTS_PATH / "custom_sync_query_builder" / "schema.graphql",),
            ),
            "example_client",
            CLIENTS_PATH / "custom_sync_query_builder" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "client_forward_refs" / "pyproject.toml",
                (
                    CLIENTS_PATH / "client_forward_refs" / "queries.graphql",
                    CLIENTS_PATH / "client_forward_refs" / "schema.graphql",
                    CLIENTS_PATH / "client_forward_refs" / "custom_scalars.py",
                ),
            ),
            "client_forward_refs",
            CLIENTS_PATH / "client_forward_refs" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "client_forward_refs_shorter_results" / "pyproject.toml",
                (
                    CLIENTS_PATH
                    / "client_forward_refs_shorter_results"
                    / "queries.graphql",
                    CLIENTS_PATH
                    / "client_forward_refs_shorter_results"
                    / "schema.graphql",
                    CLIENTS_PATH
                    / "client_forward_refs_shorter_results"
                    / "custom_scalars.py",
                ),
            ),
            "client_forward_refs_shorter_results",
            CLIENTS_PATH / "client_forward_refs_shorter_results" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "no_multipart_upload" / "pyproject.toml",
                (
                    CLIENTS_PATH / "no_multipart_upload" / "queries.graphql",
                    CLIENTS_PATH / "no_multipart_upload" / "schema.graphql",
                ),
            ),
            "expected_client",
            CLIENTS_PATH / "no_multipart_upload" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "defer_model_build" / "pyproject.toml",
                (
                    CLIENTS_PATH / "defer_model_build" / "queries.graphql",
                    CLIENTS_PATH / "defer_model_build" / "schema.graphql",
                ),
            ),
            "defer_model_build_client",
            CLIENTS_PATH / "defer_model_build" / "expected_client",
        ),
        (
            (
                CLIENTS_PATH / "alias_generator" / "pyproject.toml",
                (
                    CLIENTS_PATH / "alias_generator" / "queries.graphql",
                    CLIENTS_PATH / "alias_generator" / "schema.graphql",
                ),
            ),
            "alias_generator_client",
            CLIENTS_PATH / "alias_generator" / "expected_client",
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
    "project_dir, package_name",
    [
        (
            (
                CLIENTS_PATH / "defer_model_build" / "pyproject.toml",
                (
                    CLIENTS_PATH / "defer_model_build" / "queries.graphql",
                    CLIENTS_PATH / "defer_model_build" / "schema.graphql",
                ),
            ),
            "defer_model_build_client",
        ),
    ],
    indirect=["project_dir"],
)
def test_main_with_defer_model_build_omits_model_rebuild_calls(
    project_dir, package_name
):
    """With ``defer_model_build = true`` the generated package must not contain
    any eager ``model_rebuild()`` calls, and ``BaseModel`` must enable
    ``defer_build`` so Pydantic builds each model schema lazily on first use.
    """
    result = CliRunner().invoke(main)

    assert result.exit_code == 0
    package_path = project_dir / package_name
    assert package_path.is_dir()

    for module_path in package_path.glob("*.py"):
        assert "model_rebuild()" not in module_path.read_text(), (
            f"unexpected model_rebuild() in {module_path.name}"
        )

    base_model_code = (package_path / "base_model.py").read_text()
    assert "defer_build=True" in base_model_code

    # Forward references must still be generated (otherwise there would be
    # nothing to defer). This guards against accidentally dropping them.
    assert (
        'Optional["UserFilterInput"]' in (package_path / "input_types.py").read_text()
    )


@pytest.mark.parametrize(
    "project_dir, package_name",
    [
        (
            (
                CLIENTS_PATH / "base_model_options_no_upload" / "pyproject.toml",
                (
                    CLIENTS_PATH / "base_model_options_no_upload" / "queries.graphql",
                    CLIENTS_PATH / "base_model_options_no_upload" / "schema.graphql",
                ),
            ),
            "base_model_options_no_upload_client",
        ),
    ],
    indirect=["project_dir"],
)
def test_main_applies_base_model_config_with_multipart_uploads_disabled(
    project_dir, package_name
):
    """The base-model rewrites must apply even when ``multipart_uploads = false``.

    With uploads disabled the base model is copied from ``base_model_no_upload.py``
    rather than ``base_model.py``, so keying the rewrite off the source file name
    silently skipped it, shipping a ``BaseModel`` without the requested
    ``defer_build``/``alias_generator``/``extra`` config while still reporting the
    options as enabled. The rewrite is keyed off the base-model source path, so it
    must fire in both upload modes.
    """
    result = CliRunner().invoke(main)

    assert result.exit_code == 0
    base_model_code = (project_dir / package_name / "base_model.py").read_text()
    assert "defer_build=True" in base_model_code
    assert "alias_generator=to_camel" in base_model_code
    assert 'extra="forbid"' in base_model_code


@pytest.mark.parametrize(
    "project_dir, package_name",
    [
        (
            (
                CLIENTS_PATH / "defer_model_build" / "pyproject.toml",
                (
                    CLIENTS_PATH / "defer_model_build" / "queries.graphql",
                    CLIENTS_PATH / "defer_model_build" / "schema.graphql",
                ),
            ),
            "defer_model_build_client",
        ),
    ],
    indirect=["project_dir"],
)
def test_main_defer_model_build_package_validates_fragment_mixin_payload(
    project_dir, package_name
):
    """A deferred operation whose result subclasses a fragment must still build
    and validate a real payload.

    ``query ListUsers { users { ...UserFields } }`` generates
    ``class ListUsersUsers(UserFields)`` in ``list_users.py`` while
    ``UserFields.friends`` is a forward reference to ``UserFieldsFriends`` defined
    in ``fragments.py``. With ``defer_model_build`` the subclass is built lazily
    on first validation and resolves that inherited forward reference against its
    *own* module, so ``list_users.py`` must keep ``UserFieldsFriends`` importable.
    Diffing the generated source never exercised this. The package is imported
    and a payload validated here, across every supported Python version.
    """
    result = CliRunner().invoke(main)

    assert result.exit_code == 0, result.output
    package_path = project_dir / package_name
    assert package_path.is_dir()

    sys.path.insert(0, str(project_dir))
    for name in [n for n in list(sys.modules) if n.split(".")[0] == package_name]:
        del sys.modules[name]
    try:
        package = importlib.import_module(package_name)
        parsed = package.ListUsers.model_validate(
            {
                "users": [
                    {"id": "1", "name": "Ann", "friends": [{"id": "2", "name": "Bob"}]}
                ]
            }
        )
        assert parsed.users[0].friends[0].name == "Bob"
    finally:
        for name in [n for n in list(sys.modules) if n.split(".")[0] == package_name]:
            del sys.modules[name]
        sys.path.remove(str(project_dir))


@pytest.mark.parametrize(
    "project_dir, package_name",
    [
        (
            (
                CLIENTS_PATH / "fragment_mixin_forward_refs" / "pyproject.toml",
                (
                    CLIENTS_PATH / "defer_model_build" / "queries.graphql",
                    CLIENTS_PATH / "defer_model_build" / "schema.graphql",
                ),
            ),
            "fragment_mixin_forward_refs_client",
        ),
    ],
    indirect=["project_dir"],
)
def test_main_default_package_validates_fragment_mixin_payload(
    project_dir, package_name
):
    """A default (non-defer) operation whose result subclasses a fragment must
    still build and validate a real payload.

    ``query ListUsers { users { ...UserFields } }`` generates
    ``class ListUsersUsers(UserFields)`` in ``list_users.py`` while
    ``UserFields.friends`` is a forward reference to ``UserFieldsFriends`` defined
    in ``fragments.py``. Without ``defer_model_build`` the eager
    ``ListUsers.model_rebuild()`` re-evaluates that inherited forward reference
    against the subclass's *own* module, so ``list_users.py`` must keep
    ``UserFieldsFriends`` importable. On Python 3.10 this fails otherwise with
    ``PydanticUndefinedAnnotation``; on 3.11+ the inherited reference is reused
    rather than re-evaluated so it happens to pass. Diffing the generated source
    never exercised this. The package is imported and a payload validated here.
    """
    result = CliRunner().invoke(main)

    assert result.exit_code == 0, result.output
    package_path = project_dir / package_name
    assert package_path.is_dir()

    # Guard the generated shape the test depends on: a lazily-built subclass of a
    # fragment must not be present (that is the defer path, covered elsewhere).
    base_model_code = (package_path / "base_model.py").read_text()
    assert "defer_build=True" not in base_model_code

    sys.path.insert(0, str(project_dir))
    for name in [n for n in list(sys.modules) if n.split(".")[0] == package_name]:
        del sys.modules[name]
    try:
        package = importlib.import_module(package_name)
        parsed = package.ListUsers.model_validate(
            {
                "users": [
                    {"id": "1", "name": "Ann", "friends": [{"id": "2", "name": "Bob"}]}
                ]
            }
        )
        assert parsed.users[0].friends[0].name == "Bob"
    finally:
        for name in [n for n in list(sys.modules) if n.split(".")[0] == package_name]:
            del sys.modules[name]
        sys.path.remove(str(project_dir))


@pytest.mark.parametrize(
    "project_dir, package_name",
    [
        (
            (
                CLIENTS_PATH
                / "client_forward_refs_custom_operations"
                / "pyproject.toml",
                (
                    CLIENTS_PATH
                    / "client_forward_refs_custom_operations"
                    / "schema.graphql",
                ),
            ),
            "example_client",
        ),
    ],
    indirect=["project_dir"],
)
def test_main_client_forward_refs_with_custom_operations(project_dir, package_name):
    """ClientForwardRefsPlugin + enable_custom_operations should produce valid client.

    Custom operation methods (execute_custom_operation, query, mutation) return
    self.* or await self.* - the plugin must not treat 'self' as a generated class.
    """
    result = CliRunner().invoke(main)

    assert result.exit_code == 0, result.output
    package_path = project_dir / package_name
    assert package_path.is_dir()
    client_py = package_path / "client.py"
    assert client_py.exists(), f"Expected {client_py}"
    ast.parse(client_py.read_text())


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
def test_main_raises_exception(project_dir, expected_exception):
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
):
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
    assert "http://test/graphql/" in mocked_post.call_args.args
    assert mocked_post.call_args.kwargs["headers"] == {
        "header1": "value1",
        "header2": "value2",
    }


def test_main_can_read_config_from_provided_file(tmp_path):
    old_cwd = Path.cwd()
    files_to_copy = (
        CLIENTS_PATH / "custom_config_file" / "config.toml",
        CLIENTS_PATH / "custom_config_file" / "queries.graphql",
        CLIENTS_PATH / "custom_config_file" / "schema.graphql",
    )
    copy_files(list(files_to_copy), tmp_path)
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
        (
            (
                GRAPHQL_SCHEMAS_PATH / "example" / "pyproject-schema-graphql.toml",
                (GRAPHQL_SCHEMAS_PATH / "example" / "schema.graphql",),
            ),
            "expected_schema.graphql",
            GRAPHQL_SCHEMAS_PATH / "example" / "expected_schema.graphql",
        ),
        (
            (
                GRAPHQL_SCHEMAS_PATH / "example" / "pyproject-schema-gql.toml",
                (GRAPHQL_SCHEMAS_PATH / "example" / "schema.graphql",),
            ),
            "expected_schema.gql",
            GRAPHQL_SCHEMAS_PATH / "example" / "expected_schema.gql",
        ),
    ],
    indirect=["project_dir"],
)
def test_main_generates_correct_schema_file(project_dir, file_name, expected_file_path):
    result = CliRunner().invoke(main, "graphqlschema")

    assert result.exit_code == 0
    schema_path = project_dir / file_name

    # normalise texts to account for a spelling change in graphql-core 3.2.5
    def normalise(schema: str) -> str:
        return schema.replace(" behaviour ", " behavior ")

    actual = normalise(schema_path.read_text())
    expected = normalise(expected_file_path.read_text())

    assert actual == expected


@pytest.mark.parametrize(
    "project_dir",
    [
        (
            CLIENTS_PATH / "alias_generator" / "pyproject.toml",
            (
                CLIENTS_PATH / "alias_generator" / "queries.graphql",
                CLIENTS_PATH / "alias_generator" / "schema.graphql",
            ),
        )
    ],
    indirect=True,
)
def test_main_alias_generator_keeps_every_effective_alias(project_dir):
    """`alias_generator=to_camel` must not change what any field is named on the wire.

    Fields whose GraphQL name `to_camel` can reconstruct lose their explicit
    `Field(alias=...)`; the rest keep it. Asking pydantic for the alias it will
    really use (rather than reading the generated source) is what guards that
    split. A schema whose names are already snake_case (`some_field` ->
    `someField`) would otherwise be silently mis-aliased.
    """
    pyproject = (project_dir / "pyproject.toml").read_text()

    assert CliRunner().invoke(main).exit_code == 0
    with_generator = _resolved_aliases(project_dir, "alias_generator_client")

    (project_dir / "pyproject.toml").write_text(
        pyproject.replace("use_alias_generator = true", "use_alias_generator = false")
    )
    assert CliRunner().invoke(main).exit_code == 0
    without_generator = _resolved_aliases(project_dir, "alias_generator_client")

    assert with_generator == without_generator
    # Sanity: fields the generator reconstructs really do carry a derived alias.
    assert with_generator["ListUsersUsers.first_name"] == "firstName"
    assert with_generator["ListUsersUsers.some_field"] == "some_field"
    assert with_generator["GetAccountAccountUser.typename__"] == "__typename"


def _resolved_aliases(project_dir: Path, package_name: str) -> dict[str, str]:
    """Ask pydantic which name each generated field validates/serialises under."""
    script = textwrap.dedent(
        f"""
        import importlib, json, pkgutil
        import {package_name} as package

        aliases = {{}}
        for module_info in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{package_name}.{{module_info.name}}")
            for attribute_name in dir(module):
                model = getattr(module, attribute_name)
                if (
                    isinstance(model, type)
                    and hasattr(model, "model_fields")
                    and model.__module__ == module.__name__
                ):
                    for field_name, field in model.model_fields.items():
                        key = f"{{attribute_name}}.{{field_name}}"
                        aliases[key] = field.alias or field_name
        print(json.dumps(aliases, sort_keys=True))
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=project_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)
