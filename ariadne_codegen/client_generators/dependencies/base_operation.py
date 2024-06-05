from graphql import (
    ArgumentNode,
    BooleanValueNode,
    FieldNode,
    FloatValueNode,
    IntValueNode,
    NameNode,
    SelectionSetNode,
    StringValueNode,
)


class GraphQLArgument:
    def __init__(self, argument_name, value):
        self._name = argument_name
        self._value = self._convert_value(value)

    def _convert_value(self, value):
        if isinstance(value, str):
            return StringValueNode(value=value)
        elif isinstance(value, int):
            return IntValueNode(value=str(value))
        elif isinstance(value, float):
            return FloatValueNode(value=str(value))
        elif isinstance(value, bool):
            return BooleanValueNode(value=value)
        else:
            raise TypeError(f"Unsupported argument type: {type(value)}")

    def to_ast(self):
        return ArgumentNode(name=NameNode(value=self._name), value=self._value)


class GraphQLField:
    def __init__(self, field_name, **kwargs):
        self._field_name = field_name
        self._arguments = [GraphQLArgument(k, v) for k, v in kwargs.items() if v]
        self._subfields = []
        self._alias = None

    def fields(self, *args):
        self._subfields.extend(args)
        return self

    def alias(self, alias):
        self._alias = alias
        return self

    def _build_field_name(self):
        if self._alias:
            return f"{self._alias}: {self._field_name}"
        return self._field_name

    def to_ast(self):
        return FieldNode(
            name=NameNode(value=self._build_field_name()),
            arguments=[arg.to_ast() for arg in self._arguments],
            selection_set=SelectionSetNode(
                selections=[sub_field.to_ast() for sub_field in self._subfields]
            )
            if self._subfields
            else None,
        )
