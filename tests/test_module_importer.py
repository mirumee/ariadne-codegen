import os
import sys
from pathlib import Path
from textwrap import dedent

import pytest

from ariadne_codegen.exceptions import ModuleImportError
from ariadne_codegen.module_importer import (
    get_attribute_from_module,
    get_module_or_attribute,
    is_module_str,
)


@pytest.fixture
def tmp_path_cwd(tmp_path):
    old_cwd = Path.cwd()
    os.chdir(tmp_path)
    sys.path.append(tmp_path.as_posix())

    yield tmp_path

    os.chdir(old_cwd)
    sys.path.remove(tmp_path.as_posix())


def create_module_dir(base: Path, module_str: str) -> Path:
    path = base
    for dir_name in module_str.split("."):
        path = path / dir_name
        path.mkdir()
        path.joinpath("__init__.py").touch()
    return path


@pytest.mark.parametrize(
    "module_str",
    [
        ("test_a",),
        ("test_a.sub_b.sub_c",),
    ],
)
def test_get_module_or_attribute_returns_module_for_module_string(
    module_str, tmp_path_cwd
):
    module_str = "test_a.sub_b.sub_c"
    create_module_dir(tmp_path_cwd, module_str)

    imported_module = get_module_or_attribute(module_str)

    assert imported_module.__name__ == "test_a.sub_b.sub_c"
    assert imported_module.__package__ == "test_a.sub_b.sub_c"


def test_get_module_or_attribute_returns_attribute_from_module(tmp_path_cwd):
    module_path = create_module_dir(tmp_path_cwd, "test_module_a")
    file_content = """
    from ariadne_codegen import Plugin

    class TestClass:
        pass
    """
    module_path.joinpath("xyz.py").write_text(dedent(file_content))

    test_class = get_module_or_attribute("test_module_a.xyz.TestClass")

    assert test_class.__name__ == "TestClass"
    assert test_class.__module__ == "test_module_a.xyz"


def test_is_module_str_returns_true_if_string_points_to_existing_module(tmp_path_cwd):
    module_str = "test_a.sub_b.sub_c"
    create_module_dir(tmp_path_cwd, module_str)

    assert is_module_str(module_str)


def test_is_module_str_returns_false_if_string_points_to_specific_file(tmp_path_cwd):
    module_str = "test_a.sub_b.sub_c"
    module_path = create_module_dir(tmp_path_cwd, module_str)
    module_path.joinpath("abcd.py").touch()

    assert not is_module_str(module_str + ".abcd.py")


def test_get_attribute_from_module_returns_attribute(tmp_path_cwd):
    module_path = create_module_dir(tmp_path_cwd, "test_module_b")
    file_content = """
    from ariadne_codegen import Plugin

    class TestClass:
        pass
    """
    module_path.joinpath("xyz.py").write_text(dedent(file_content))

    test_class = get_attribute_from_module("test_module_b.xyz.TestClass")

    assert test_class.__name__ == "TestClass"
    assert test_class.__module__ == "test_module_b.xyz"


def test_get_attribute_from_module_raises_module_import_error_for_class():
    with pytest.raises(ModuleImportError):
        get_attribute_from_module("TestClass")


def test_get_attribute_from_module_raises_module_import_error_for_not_existing_module():
    with pytest.raises(ModuleImportError):
        get_attribute_from_module("test_module.TestClass")


def test_get_attribute_from_module_raises_module_import_error_for_not_existing_class(
    tmp_path_cwd,
):
    module_str = "test_module"
    create_module_dir(tmp_path_cwd, module_str)

    with pytest.raises(ModuleImportError):
        get_attribute_from_module(f"{module_str}.TestClass")
