import os
import sys
from pathlib import Path
from textwrap import dedent

import pytest

from ariadne_codegen.exceptions import PluginImportError
from ariadne_codegen.plugins.base import Plugin
from ariadne_codegen.plugins.explorer import (
    get_plugin_class,
    get_plugins_classes,
    get_plugins_classes_from_module,
    is_module_str,
    is_plugin_type,
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


def test_get_plugins_classes_returns_plugin_classes_from_all_modules(tmp_path_cwd):
    module_xyz_path = create_module_dir(tmp_path_cwd, "module_xyz")
    init_xyz_content = """
    from .x import PluginX
    from .y import PluginY

    __all__ = ["PluginX", "PluginY"]
    """
    x_content = """
    from ariadne_codegen import Plugin

    class PluginX(Plugin):
        pass
    """
    y_content = """
    from ariadne_codegen.plugins.base import Plugin

    class PluginY(Plugin):
        pass
    """
    module_xyz_path.joinpath("__init__.py").write_text(dedent(init_xyz_content))
    module_xyz_path.joinpath("x.py").write_text(dedent(x_content))
    module_xyz_path.joinpath("y.py").write_text(dedent(y_content))

    module_abc_path = create_module_dir(tmp_path_cwd, "module_abc")
    a_content = """
    from ariadne_codegen import Plugin

    class PluginA(Plugin):
        pass
    """
    b_content = """
    from ariadne_codegen.plugins.base import Plugin

    class PluginB(Plugin):
        pass
    """
    module_abc_path.joinpath("a.py").write_text(dedent(a_content))
    module_abc_path.joinpath("b.py").write_text(dedent(b_content))

    classes = get_plugins_classes(
        ["module_xyz", "module_abc.a.PluginA", "module_abc.b.PluginB"]
    )

    assert len(classes) == 4
    assert isinstance(classes[0], type)
    assert isinstance(classes[1], type)
    assert isinstance(classes[2], type)
    assert isinstance(classes[3], type)
    assert {
        "module_abc.a.PluginA",
        "module_abc.b.PluginB",
        "module_xyz.x.PluginX",
        "module_xyz.y.PluginY",
    } == {f"{c.__module__}.{c.__name__}" for c in classes}


def test_is_module_str_returns_true_if_string_points_to_existing_module(tmp_path_cwd):
    module_str = "test_a.sub_b.sub_c"
    create_module_dir(tmp_path_cwd, module_str)

    assert is_module_str(module_str)


def test_is_module_str_returns_false_if_string_points_to_specific_file(tmp_path_cwd):
    module_str = "test_a.sub_b.sub_c"
    module_path = create_module_dir(tmp_path_cwd, module_str)
    module_path.joinpath("abcd.py").touch()

    assert not is_module_str(module_str + ".abcd.py")


def test_get_plugins_classes_from_module_returns_all_public_plugins(tmp_path_cwd):
    module_str = "module_ab"
    module_path = create_module_dir(tmp_path_cwd, module_str)
    init_content = """
    from .a import PluginA
    from .b import PluginB

    __all__ = ["PluginA", "PluginB"]
    """
    a_content = """
    from ariadne_codegen import Plugin

    class PluginA(Plugin):
        pass
    """
    b_content = """
    from ariadne_codegen.plugins.base import Plugin

    class PluginB(Plugin):
        pass
    """
    module_path.joinpath("__init__.py").write_text(dedent(init_content))
    module_path.joinpath("a.py").write_text(dedent(a_content))
    module_path.joinpath("b.py").write_text(dedent(b_content))

    classes = get_plugins_classes_from_module(module_str)

    assert len(classes) == 2
    assert isinstance(classes[0], type)
    assert isinstance(classes[1], type)
    assert {
        f"{module_str}.a.PluginA",
        f"{module_str}.b.PluginB",
    } == {f"{c.__module__}.{c.__name__}" for c in classes}


def test_is_plugin_type_returns_false_for_not_class():
    assert not is_plugin_type(lambda: None)


def test_is_plugin_type_returns_false_for_base_plugin_class():
    assert not is_plugin_type(Plugin)


def test_is_plugin_type_returns_false_for_class_not_inheriting_from_base_plugin():
    class InvalidPlugin:
        pass

    assert not is_plugin_type(InvalidPlugin)


def test_is_plugin_type_returns_true_for_class_inheriting_from_base_plugin():
    class ValidPlugin(Plugin):
        pass

    assert is_plugin_type(ValidPlugin)


def test_get_plugin_class_returns_plugin_class(tmp_path_cwd):
    module_path = create_module_dir(tmp_path_cwd, "test_module")
    file_content = """
    from ariadne_codegen import Plugin

    class TestPlugin(Plugin):
        pass
    """
    module_path.joinpath("xyz.py").write_text(dedent(file_content))

    test_plugin = get_plugin_class("test_module.xyz.TestPlugin")

    assert isinstance(test_plugin, type)
    assert test_plugin.__name__ == "TestPlugin"
    assert test_plugin.__module__ == "test_module.xyz"


def test_get_plugin_class_raises_plugin_import_error_for_class_without_module():
    with pytest.raises(PluginImportError):
        get_plugin_class("TestPlugin")


def test_get_plugin_class_raises_plugin_import_error_for_not_existing_module():
    with pytest.raises(PluginImportError):
        get_plugin_class("test_module.TestPlugin")


def test_get_plugin_class_raises_plugin_import_error_for_not_existing_class(
    tmp_path_cwd,
):
    module_str = "test_module"
    create_module_dir(tmp_path_cwd, module_str)

    with pytest.raises(PluginImportError):
        get_plugin_class(f"{module_str}.TestPlugin")


@pytest.mark.parametrize(
    "file_content,object_name",
    [
        ("class Test:\n    pass", "Test"),
        ("def test():\n    pass", "test"),
        ("from ariadne_codegen import Plugin", "Plugin"),
    ],
)
def test_get_plugin_class_raises_plugin_import_error_for_not_plugin(
    tmp_path_cwd, file_content, object_name
):
    module_str = "test_module"
    module_path = create_module_dir(tmp_path_cwd, module_str)
    module_path.joinpath("xyz.py").write_text(file_content)

    with pytest.raises(PluginImportError):
        get_plugin_class(f"{module_str}.xyz.{object_name}")
