---
title: Custom scalars
---

# Custom scalars

By default, non built-in scalars are represented as `typing.Any` in the generated
client. You can provide information about a specific scalar by adding a section to
`pyproject.toml`:

```toml
[tool.ariadne-codegen.scalars.{graphql scalar name}]
type = "(required) python type name"
serialize = "function used to serialize scalar"
parse = "function used to create scalar instance from serialized form"
```

For each custom scalar the client will use the given `type` in all occurrences of
`{graphql scalar name}`. If provided, `serialize` and `parse` will be used for
serialization and deserialization. In result models `type` will be annotated with
`BeforeValidator`, eg. `Annotated[type, BeforeValidator(parse)]`. In inputs the
annotation will use `PlainSerializer`, eg. `Annotated[type, PlainSerializer(serialize)]`.

If `type`/`serialize`/`parse` contains at least one `.` then the string will be
split by its last occurrence. The first part will be used as the module to import
from, and the second part as the type/method name. For example,
`type = "custom_scalars.a.ScalarA"` will produce
`from custom_scalars.a import ScalarA`.

## Example with scalar mapped to built-in type

In this case the scalar is mapped to the built-in `str` which doesn't require custom
`serialize` and `parse` methods.

```toml
[tool.ariadne-codegen.scalars.SCALARA]
type = "str"
```

## Example with type supported by pydantic

In this scenario the scalar is represented as `datetime`, so it needs to be imported.
Pydantic handles serialization and deserialization so custom `parse` and `serialize`
is not necessary.

```toml
[tool.ariadne-codegen.scalars.DATETIME]
type = "datetime.datetime"
```

## Example with fully custom type

In this example the scalar is represented as class `TypeB`. Pydantic can't handle
serialization and deserialization so custom `parse` and `serialize` is necessary.
To provide `type`, `parse` and `serialize` implementation we can use
`files_to_include` to copy the `type_b.py` file.

```toml
[tool.ariadne-codegen]
...
files_to_include = [".../type_b.py"]

[tool.ariadne-codegen.scalars.SCALARB]
type = ".type_b.TypeB"
parse = ".type_b.parse_b"
serialize = ".type_b.serialize_b"
```

```py
# inputs.py

class TestInput(BaseModel):
    value_b: Annotated[TypeB, PlainSerializer(serialize_b)]
```

```py
# get_b.py

class GetB(BaseModel):
    query_b: Annotated[TypeB, BeforeValidator(parse_b)]
```

```py
# client.py

class Client(AsyncBaseClient):
    async def test_mutation(self, value: TypeB) -> TestMutation:
        ...
        variables: dict[str, object] = {
            "value": serialize_b(value),
        }
        ...
```
