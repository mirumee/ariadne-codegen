from ast import Assign, ImportFrom, List, Module

from graphql_sdk_gen.generators.init_file import InitFileGenerator


def test_add_import_adds_correct_objects_to_list():
    from_ = "file_name"
    class_name = "TestClass"
    generator = InitFileGenerator()

    generator.add_import(modules=[class_name], from_=from_, level=1)

    import_ = generator.imports[0]
    assert len(generator.imports) == 1
    assert isinstance(import_, ImportFrom)
    assert import_.module == from_
    assert [alias.name for alias in import_.names] == [class_name]
    assert import_.level == 1


def test_generate_without_imports_returns_empty_module():
    generator = InitFileGenerator()

    module = generator.generate()

    assert isinstance(module, Module)
    assert not module.body


def test_generate_with_added_imports_returns_module():
    generator = InitFileGenerator()
    name1, name2 = "Abcd", "Xyz"
    generator.add_import([name1], "abcd", 1)
    generator.add_import([name2], "xyz", 1)

    module = generator.generate()

    assign_stmt = module.body[2]
    assert len(module.body) == 3
    assert isinstance(assign_stmt, Assign)
    assert [n.id for n in assign_stmt.targets] == ["__all__"]
    assert isinstance(assign_stmt.value, List)
    assert [c.value for c in assign_stmt.value.elts] == [name1, name2]
