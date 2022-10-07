import ast
from typing import Union

import pytest
from graphql import (
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLField,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType,
)

from graphql_sdk_gen.generators.codegen import (
    generate_ann_assign,
    generate_annotation_name,
    generate_arg,
    generate_arguments,
    generate_assign,
    generate_async_method_definition,
    generate_class_def,
    generate_constant,
    generate_import_from,
    generate_list_annotation,
    generate_name,
    generate_nullable_annotation,
    generate_union_annotation,
    parse_field_type,
)
from graphql_sdk_gen.generators.constants import ANY, LIST, OPTIONAL, UNION


def test_generate_import_from_returns_correct_object():
    object1, object2 = "Obj1", "Obj2"
    from_ = "objects"

    import_ = generate_import_from([object1, object2], from_, level=1)

    assert isinstance(import_, ast.ImportFrom)
    assert import_.module == from_
    assert [n.name for n in import_.names] == [object1, object2]
    assert import_.level == 1


def test_generate_nullable_annotation_returns_subscript_with_correct_value():
    slice_ = ast.Name(id="xyz")

    result = generate_nullable_annotation(slice_)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL


def test_generate_annotation_name_returns_not_optional_annotation():
    name = "xyz"

    result = generate_annotation_name(name, False)

    assert isinstance(result, ast.Name)
    assert result.id == name


def test_generate_annotation_name_returns_optional_annotation():
    name = "xyz"

    result = generate_annotation_name(name, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Name)
    assert result.slice.id == name


def test_generate_list_annotation_returns_list_annotation():
    slice_ = ast.Name(id="xyz")

    result = generate_list_annotation(slice_, False)

    assert isinstance(result.value, ast.Name)
    assert result.value.id == LIST
    assert result.slice == slice_


def test_generate_list_annotation_returns_optional_list_annotation():
    slice_ = ast.Name(id="xyz")

    result = generate_list_annotation(slice_, True)

    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Subscript)
    assert isinstance(result.slice.value, ast.Name)
    assert result.slice.value.id == LIST
    assert result.slice.slice == slice_


def test_generate_arg_returns_arg_with_correct_data():
    name = "xyz"
    annotation = ast.Name(id="str")

    result = generate_arg(name, annotation)

    assert isinstance(result, ast.arg)
    assert result.arg == name
    assert result.annotation == annotation


def test_generate_arguments_returns_arguments_with_given_args():
    args = [ast.arg(arg="self")]

    result = generate_arguments(args)

    assert isinstance(result, ast.arguments)
    assert result.args == args


def test_generate_async_method_definition_returns_async_function_definition():
    name = "xyz"
    return_type = ast.Name("Xyz")
    arguments = ast.arguments(
        posonlyargs=[],
        args=[ast.arg(arg="self")],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[],
    )

    result = generate_async_method_definition(name, arguments, return_type)

    assert isinstance(result, ast.AsyncFunctionDef)
    assert result.name == name
    assert result.returns == return_type
    assert result.args == arguments


def test_generate_class_def_returns_class_def_with_correct_bases():
    name = "Xyz"
    base_name = "BaseClass"

    result = generate_class_def(name, [base_name])

    assert isinstance(result, ast.ClassDef)
    assert result.name == name
    base = result.bases[0]
    assert isinstance(base, ast.Name)
    assert base.id == base_name


def test_generate_class_def_returns_class_def_without_base():
    name = "Xyz"

    result = generate_class_def(name)

    assert isinstance(result, ast.ClassDef)
    assert result.name == name
    assert not result.bases


def test_generate_name_returns_name_object():
    value = "xyz"

    result = generate_name(value)

    assert isinstance(result, ast.Name)
    assert result.id == value


@pytest.mark.parametrize("value", [1, "a", "xyz", True, None])
def test_generate_constant_returns_object_with_given_value(value):
    result = generate_constant(value)

    assert isinstance(result, ast.Constant)
    assert result.value == value


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


def test_generate_union_annotation_returns_union_annotation():
    types: list[Union[ast.Name, ast.Subscript]] = [
        ast.Name(id="Xyz1"),
        ast.Name(id="Xyz2"),
    ]

    result = generate_union_annotation(types, False)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == UNION
    assert isinstance(result.slice, ast.Tuple)
    assert result.slice.elts == types


def test_generate_union_annotation_returns_optional_union_annotation():
    types: list[Union[ast.Name, ast.Subscript]] = [
        ast.Name(id="Xyz1"),
        ast.Name(id="Xyz2"),
    ]

    result = generate_union_annotation(types, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Subscript)
    assert isinstance(result.slice.value, ast.Name)
    assert result.slice.value.id == UNION
    assert isinstance(result.slice.slice, ast.Tuple)
    assert result.slice.slice.elts == types


@pytest.mark.parametrize(
    "type_name, expected_repr",
    [
        ("String", "str"),
        ("ID", "str"),
        ("Int", "int"),
        ("Boolean", "bool"),
        ("Float", "float"),
        ("Unknown", ANY),
    ],
)
def test_parse_field_type_given_scalar_type_returns_name_object(
    type_name, expected_repr
):
    type_ = GraphQLScalarType(name=type_name)

    result = parse_field_type(type_, False)

    assert isinstance(result, ast.Name)
    assert result.id == expected_repr


@pytest.mark.parametrize(
    "type_name, expected_repr",
    [
        ("String", "str"),
        ("ID", "str"),
        ("Int", "int"),
        ("Boolean", "bool"),
        ("Float", "float"),
        ("Unknown", ANY),
    ],
)
def test_parse_field_type_given_scalar_type_returns_optional_annotation(
    type_name, expected_repr
):
    type_ = GraphQLScalarType(name=type_name)

    result = parse_field_type(type_, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Name)
    assert result.slice.id == expected_repr


@pytest.mark.parametrize(
    "type_class",
    [GraphQLObjectType, GraphQLInputObjectType, GraphQLInterfaceType],
)
def test_parse_field_type_given_custom_type_returns_name_object(type_class):
    type_name = "Xyz"
    type_ = type_class(
        name=type_name,
        fields={"field": GraphQLField(type_=GraphQLScalarType(name="String"))},
    )

    result = parse_field_type(type_, False)

    assert isinstance(result, ast.Name)
    assert result.id == f'"{type_name}"'


@pytest.mark.parametrize(
    "type_class",
    [GraphQLObjectType, GraphQLInputObjectType, GraphQLInterfaceType],
)
def test_parse_field_type_given_custom_type_returns_optional_annotation(type_class):
    type_name = "Xyz"
    type_ = type_class(
        name=type_name,
        fields={"field": GraphQLField(type_=GraphQLScalarType(name="String"))},
    )

    result = parse_field_type(type_, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Name)
    assert result.slice.id == f'"{type_name}"'


def test_parse_field_type_given_enum_type_returns_name_object():
    type_name = "Xyz"
    type_ = GraphQLEnumType(name=type_name, values={"X": GraphQLEnumValue(value="X")})

    result = parse_field_type(type_, False)

    assert isinstance(result, ast.Name)
    assert result.id == f'"{type_name}"'


def test_parse_field_type_given_enum_type_returns_optional_annotation():
    type_name = "Xyz"
    type_ = GraphQLEnumType(name=type_name, values={"X": GraphQLEnumValue(value="X")})

    result = parse_field_type(type_, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Name)
    assert result.slice.id == f'"{type_name}"'


def test_parse_field_type_given_union_type_returns_union_annotation():
    type_ = GraphQLUnionType(
        name="xyz",
        types=[
            GraphQLObjectType(
                name="String",
                fields={"field": GraphQLField(type_=GraphQLScalarType(name="String"))},
            )
        ],
    )

    result = parse_field_type(type_, False)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == UNION
    assert isinstance(result.slice, ast.Tuple)


def test_parse_field_type_given_union_type_returns_optional_union_annotation():
    type_ = GraphQLUnionType(
        name="xyz",
        types=[
            GraphQLObjectType(
                name="String",
                fields={"field": GraphQLField(type_=GraphQLScalarType(name="String"))},
            )
        ],
    )

    result = parse_field_type(type_, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Subscript)
    assert isinstance(result.slice.value, ast.Name)
    assert result.slice.value.id == UNION
    assert isinstance(result.slice.slice, ast.Tuple)


def test_parse_field_type_given_list_type_returns_list_annotation():
    type_ = GraphQLList(GraphQLScalarType(name="String"))

    result = parse_field_type(type_, False)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == LIST


def test_parse_field_type_given_list_type_returns_optional_list_annotation():
    type_ = GraphQLList(GraphQLScalarType(name="String"))

    result = parse_field_type(type_, True)

    assert isinstance(result, ast.Subscript)
    assert isinstance(result.value, ast.Name)
    assert result.value.id == OPTIONAL
    assert isinstance(result.slice, ast.Subscript)
    assert isinstance(result.slice.value, ast.Name)
    assert result.slice.value.id == LIST


@pytest.mark.parametrize(
    "subtype",
    [
        GraphQLScalarType(name="String"),
        GraphQLObjectType(
            name="Xyz",
            fields={"field": GraphQLField(type_=GraphQLScalarType(name="String"))},
        ),
        GraphQLInputObjectType(
            name="Xyz",
            fields={"field": GraphQLInputField(type_=GraphQLScalarType(name="String"))},
        ),
        GraphQLInterfaceType(
            name="Xyz",
            fields={"field": GraphQLField(type_=GraphQLScalarType(name="String"))},
        ),
        GraphQLEnumType(name="Xyz", values={"X": GraphQLEnumValue(value="X")}),
    ],
)
def test_parse_field_type_given_non_null_type_returns_not_optional_annotation(
    subtype,
):
    type_ = GraphQLNonNull(subtype)

    result = parse_field_type(type_)

    assert not isinstance(result, ast.Subscript)


def test_parse_field_type_given_non_null_list_type_returns_not_optional_annotation():
    type_ = GraphQLNonNull(GraphQLList(GraphQLScalarType(name="String")))

    result = parse_field_type(type_)

    assert isinstance(result, ast.Subscript)
    assert result.value != OPTIONAL


def test_parse_field_type_given_non_null_union_type_returns_not_optional_annotation():
    type_ = GraphQLNonNull(
        GraphQLUnionType(
            name="xyz",
            types=[
                GraphQLObjectType(
                    name="String",
                    fields={
                        "field": GraphQLField(type_=GraphQLScalarType(name="String"))
                    },
                )
            ],
        )
    )

    result = parse_field_type(type_)

    assert isinstance(result, ast.Subscript)
    assert result.value != OPTIONAL
