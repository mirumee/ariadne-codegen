import ast

from ariadne_codegen.codegen import generate_import_from


def test_generate_import_from_returns_correct_object():
    object1, object2 = "Obj1", "Obj2"
    from_ = "objects"

    import_ = generate_import_from([object1, object2], from_, level=1)

    assert isinstance(import_, ast.ImportFrom)
    assert import_.module == from_
    assert [n.name for n in import_.names] == [object1, object2]
    assert import_.level == 1
