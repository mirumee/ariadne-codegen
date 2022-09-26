from ast import Assign, ClassDef, Constant, Import, ImportFrom, List, Name, Pass, alias

import pytest

from graphql_sdk_gen.generators.utils import ast_to_str, generate_import_from


def test_generate_import_from_returns_correct_object():
    object1, object2 = "Obj1", "Obj2"
    from_ = "objects"

    import_ = generate_import_from([object1, object2], from_, level=1)

    assert isinstance(import_, ImportFrom)
    assert import_.module == from_
    assert [n.name for n in import_.names] == [object1, object2]
    assert import_.level == 1


@pytest.mark.parametrize(
    ["ast_object", "expected_result"],
    [
        (
            ImportFrom(module="xyz", names=[alias(name="Xyz")], level=1),
            "from .xyz import Xyz\n",
        ),
        (Import(names=[alias(name="xyz")]), "import xyz\n"),
        (
            ClassDef(
                name="Xyz", bases=[], keywords=[], body=[Pass()], decorator_list=[]
            ),
            "class Xyz:\n    pass\n",
        ),
        (
            Assign(
                targets=[Name(id="__all__")],
                value=List(elts=[Constant(value="Xyz")]),
                lineno=1,
            ),
            '__all__ = ["Xyz"]\n',
        ),
    ],
)
def test_ast_to_str_returns_correct_string(ast_object, expected_result):
    assert ast_to_str(ast_object) == expected_result
