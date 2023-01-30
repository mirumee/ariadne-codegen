import ast

from ariadne_codegen.generators.codegen import generate_ann_assign, generate_assign


def test_generate_assign_returns_objects_with_correct_targets_and_value():
    target_name = "xyz"
    value = ast.Name(id="abc")

    result = generate_assign([target_name], value)

    assert isinstance(result, ast.Assign)
    target = result.targets[0]
    assert isinstance(target, ast.Name)
    assert target.id == target_name
    assert result.value == value


def test_generate_ann_assign_returns_object_with_given_annotation_and_tartget():
    target_name = "xyz"
    annotation = ast.Name(id="Xyz")

    result = generate_ann_assign(target_name, annotation)

    assert isinstance(result, ast.AnnAssign)
    assert isinstance(result.target, ast.Name)
    assert result.target.id == target_name
    assert result.annotation == annotation
