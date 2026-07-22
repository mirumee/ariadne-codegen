import ast
import importlib
import sys

import pytest

from ariadne_codegen.client_generators.init_file import InitFileGenerator

from ..utils import filter_imports


def test_add_import_adds_correct_objects_to_list():
    from_ = "file_name"
    class_name = "TestClass"
    generator = InitFileGenerator()

    generator.add_import(names=[class_name], from_=from_, level=1)

    import_ = generator.imports[0]
    assert len(generator.imports) == 1
    assert isinstance(import_, ast.ImportFrom)
    assert import_.module == from_
    assert [alias.name for alias in import_.names] == [class_name]
    assert import_.level == 1


def test_add_import_triggers_generate_init_import_hook_method(mocked_plugin_manager):
    generator = InitFileGenerator(plugin_manager=mocked_plugin_manager)

    generator.add_import(names=["TestClass"], from_="test", level=1)

    assert mocked_plugin_manager.generate_init_import.called


def test_add_import_with_empty_names_list_doesnt_add_invalid_import():
    generator = InitFileGenerator()

    generator.add_import(names=[], from_="abcd", level=1)
    module = generator.generate()

    imports = filter_imports(module)
    assert not imports


def test_generate_without_imports_returns_empty_module():
    generator = InitFileGenerator()

    module = generator.generate()

    assert isinstance(module, ast.Module)
    assert not module.body


def test_generate_with_added_imports_returns_module():
    generator = InitFileGenerator()
    name1, name2 = "Abcd", "Xyz"
    generator.add_import([name1], "abcd", 1)
    generator.add_import([name2], "xyz", 1)

    module = generator.generate()

    assign_stmt = module.body[2]
    assert len(module.body) == 3
    assert isinstance(assign_stmt, ast.Assign)
    assert [n.id for n in assign_stmt.targets] == ["__all__"]
    assert isinstance(assign_stmt.value, ast.List)
    assert [c.value for c in assign_stmt.value.elts] == [name1, name2]


def test_generate_triggers_generate_init_module_from_plugin_manager(
    mocked_plugin_manager,
):
    generator = InitFileGenerator(plugin_manager=mocked_plugin_manager)

    generator.generate()

    assert mocked_plugin_manager.generate_init_module.called


def test_generate_with_lazy_imports_moves_imports_under_type_checking():
    generator = InitFileGenerator(lazy_imports=True)
    generator.add_import(["Abcd"], "abcd", 1)
    generator.add_import(["Xyz"], "xyz", 1)

    module = generator.generate()

    # Nothing generated is imported at module level: the only top-level imports
    # are the machinery the `__getattr__` hook itself needs.
    top_level = {
        alias.name for import_ in filter_imports(module) for alias in import_.names
    }
    assert top_level == {"TYPE_CHECKING"}

    type_checking_block = next(n for n in module.body if isinstance(n, ast.If))
    assert type_checking_block.test.id == "TYPE_CHECKING"
    assert [
        alias.name for import_ in type_checking_block.body for alias in import_.names
    ] == ["Abcd", "Xyz"]


def test_generate_with_lazy_imports_maps_every_name_to_its_module():
    generator = InitFileGenerator(lazy_imports=True)
    generator.add_import(["Abcd"], "abcd", 1)
    generator.add_import(["Xyz"], "xyz", 1)

    module = generator.generate()

    lazy_map = next(
        n
        for n in module.body
        if isinstance(n, ast.Assign) and n.targets[0].id == "_LAZY_IMPORTS"
    )
    mapped = {
        key.value: value.value
        for key, value in zip(lazy_map.value.keys, lazy_map.value.values, strict=True)
    }
    assert mapped == {"Abcd": ".abcd", "Xyz": ".xyz"}


def test_generate_with_lazy_imports_keeps_the_same_public_api():
    """`__all__` is the package's contract, so it must not depend on the setting."""
    names = {"Abcd": "abcd", "Xyz": "xyz"}

    all_values = []
    for lazy_imports in (False, True):
        generator = InitFileGenerator(lazy_imports=lazy_imports)
        for name, from_ in names.items():
            generator.add_import([name], from_, 1)
        module = generator.generate()
        assign = next(
            n
            for n in module.body
            if isinstance(n, ast.Assign) and n.targets[0].id == "__all__"
        )
        all_values.append([c.value for c in assign.value.elts])

    eager_all, lazy_all = all_values
    assert lazy_all == eager_all == ["Abcd", "Xyz"]


def test_generate_with_lazy_imports_and_no_imports_returns_empty_module():
    generator = InitFileGenerator(lazy_imports=True)

    module = generator.generate()

    assert not module.body


def test_generate_with_lazy_imports_triggers_plugin_hooks(mocked_plugin_manager):
    generator = InitFileGenerator(
        plugin_manager=mocked_plugin_manager, lazy_imports=True
    )
    generator.add_import(["Abcd"], "abcd", 1)

    generator.generate()

    assert mocked_plugin_manager.generate_init_import.called
    assert mocked_plugin_manager.generate_init_module.called


@pytest.fixture
def lazy_package(tmp_path, monkeypatch):
    """Write a package whose init the generator produced, and import it."""
    generator = InitFileGenerator(lazy_imports=True)
    generator.add_import(["Alpha"], "alpha", 1)
    generator.add_import(["Beta"], "beta", 1)

    package = tmp_path / "lazy_package"
    package.mkdir()
    (package / "__init__.py").write_text(ast.unparse(generator.generate()))
    (package / "alpha.py").write_text("class Alpha:\n    pass\n")
    (package / "beta.py").write_text("class Beta:\n    pass\n")

    monkeypatch.syspath_prepend(tmp_path)
    yield importlib.import_module("lazy_package")
    for name in [n for n in sys.modules if n.startswith("lazy_package")]:
        del sys.modules[name]


def test_lazy_imports_init_imports_a_module_only_when_a_name_from_it_is_used(
    lazy_package,
):
    assert "lazy_package.alpha" not in sys.modules
    assert "lazy_package.beta" not in sys.modules

    assert lazy_package.Alpha.__name__ == "Alpha"

    # Touching `Alpha` pulls in its module, and only its module.
    assert "lazy_package.alpha" in sys.modules
    assert "lazy_package.beta" not in sys.modules


def test_lazy_imports_init_caches_the_name_after_the_first_use(lazy_package):
    first = lazy_package.Alpha

    # The hook writes the name into the module globals, which takes it out of the
    # path for every later access; `is` catches a hook that re-imports instead.
    assert lazy_package.Alpha is first
    assert vars(lazy_package)["Alpha"] is first


def test_lazy_imports_init_raises_attribute_error_for_unknown_name(lazy_package):
    with pytest.raises(AttributeError, match="has no attribute 'Nope'"):
        _ = lazy_package.Nope


def test_lazy_imports_init_reports_the_public_api_through_dir(lazy_package):
    assert dir(lazy_package) == ["Alpha", "Beta"]
