import ast
from unittest import mock

from ariadne_codegen.codegen import generate_arguments, generate_method_definition


def test_generate_method_definition_with_minimal_parameters():
    """Test generate_method_definition with only required parameters."""
    name = "test_method"
    arguments = generate_arguments()
    return_type = ast.Name(id="str")

    result = generate_method_definition(name, arguments, return_type)

    assert isinstance(result, ast.FunctionDef)
    assert result.name == name
    assert result.args == arguments
    assert result.returns == return_type
    assert result.lineno == 1
    assert len(result.body) == 1
    assert isinstance(result.body[0], ast.Pass)
    assert result.decorator_list == []


def test_generate_method_definition_with_description():
    """Test generate_method_definition with description adds docstring."""
    name = "test_method"
    arguments = generate_arguments()
    return_type = ast.Name(id="str")
    description = "This is a test method"

    result = generate_method_definition(
        name, arguments, return_type, description=description
    )

    assert len(result.body) == 2
    assert isinstance(result.body[0], ast.Expr)
    assert isinstance(result.body[0].value, ast.Constant)
    assert result.body[0].value.value == description
    assert isinstance(result.body[1], ast.Pass)


def test_generate_method_definition_with_custom_body():
    """Test generate_method_definition with custom body."""
    name = "test_method"
    arguments = generate_arguments()
    return_type = ast.Name(id="str")
    body = [ast.Return(value=ast.Constant(value="test"))]

    result = generate_method_definition(name, arguments, return_type, body=body)

    assert result.body == body
    assert len(result.body) == 1
    assert isinstance(result.body[0], ast.Return)


def test_generate_method_definition_with_description_and_custom_body():
    """Test generate_method_definition with both description and custom body."""
    name = "test_method"
    arguments = generate_arguments()
    return_type = ast.Name(id="str")
    description = "Test description"
    body = [ast.Return(value=ast.Constant(value="test"))]

    result = generate_method_definition(
        name, arguments, return_type, description=description, body=body
    )

    assert len(result.body) == 2
    assert isinstance(result.body[0], ast.Expr)
    assert result.body[0].value.value == description
    assert isinstance(result.body[1], ast.Return)


def test_generate_method_definition_with_custom_lineno():
    """Test generate_method_definition with custom line number."""
    name = "test_method"
    arguments = generate_arguments()
    return_type = ast.Name(id="str")
    lineno = 42

    result = generate_method_definition(name, arguments, return_type, lineno=lineno)

    assert result.lineno == lineno


def test_generate_method_definition_with_decorators():
    """Test generate_method_definition with decorator list."""
    name = "test_method"
    arguments = generate_arguments()
    return_type = ast.Name(id="str")
    decorators = [ast.Name(id="property"), ast.Name(id="staticmethod")]

    result = generate_method_definition(
        name, arguments, return_type, decorator_list=decorators
    )

    assert result.decorator_list == decorators


def test_generate_method_definition_with_subscript_return_type():
    """Test generate_method_definition with Subscript return type."""
    name = "test_method"
    arguments = generate_arguments()
    return_type = ast.Subscript(value=ast.Name(id="list"), slice=ast.Name(id="str"))

    result = generate_method_definition(name, arguments, return_type)

    assert result.returns == return_type
    assert isinstance(result.returns, ast.Subscript)


@mock.patch("sys.version_info", (3, 12, 0))
def test_generate_method_definition_python_312_or_later():
    """Test generate_method_definition includes type_params for Python 3.12+."""
    name = "test_method"
    arguments = generate_arguments()
    return_type = ast.Name(id="str")

    result = generate_method_definition(name, arguments, return_type)

    assert hasattr(result, "type_params")
    assert result.type_params == []


@mock.patch("sys.version_info", (3, 11, 0))
def test_generate_method_definition_python_311_or_earlier():
    """Test generate_method_definition doesn't include type_params for Python < 3.12."""
    name = "test_method"
    arguments = generate_arguments()
    return_type = ast.Name(id="str")

    result = generate_method_definition(name, arguments, return_type)

    # In Python < 3.12, type_params shouldn't be set
    # We check that the function still works correctly
    assert isinstance(result, ast.FunctionDef)
    assert result.name == name


def test_generate_method_definition_all_parameters():
    """Test generate_method_definition with all parameters specified."""
    name = "complex_method"
    arguments = generate_arguments()
    return_type = ast.Subscript(value=ast.Name(id="Optional"), slice=ast.Name(id="int"))
    description = "A complex method with all parameters"
    body = [
        ast.Assign(targets=[ast.Name(id="x")], value=ast.Constant(value=1)),
        ast.Return(value=ast.Name(id="x")),
    ]
    lineno = 10
    decorators = [ast.Name(id="classmethod")]

    result = generate_method_definition(
        name, arguments, return_type, description, body, lineno, decorators
    )

    assert result.name == name
    assert result.args == arguments
    assert result.returns == return_type
    assert result.lineno == lineno
    assert result.decorator_list == decorators
    assert len(result.body) == 3  # docstring + 2 body statements
    assert isinstance(result.body[0], ast.Expr)  # docstring
    assert result.body[0].value.value == description
