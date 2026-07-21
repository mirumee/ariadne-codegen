---
title: Extending generated types
---

# Extending generated types

## Extending models with custom mixins

The `mixin` directive allows you to extend a generated class with custom logic.
`mixin` takes two required arguments:

- `from` - name of a module to import from
- `import` - name of a parent class

The generated class will use `import` as an extra base class, and the import will be
added to the file.

```py
from {from} import {import}
...
class OperationNameField(BaseModel, {import}):
    ...
```

You don't need to declare the directive in your schema - `ariadne-codegen` registers
it automatically before processing your operations, so you can use `@mixin` right
away.

Both arguments must be string literals; if either `from` or `import` is missing (or
a non-string value is passed), generation fails with a `ParsingError`.

The directive only emits the `from {from} import {import}` line - it does not copy any
code - so the imported module must be reachable from the generated package. This
depends on what `from` points to:

- a **relative import** (e.g. `from: ".mixins"`) refers to a module inside the generated
  package, so you must copy that module in with the [`files_to_include`](../03-reference/01-configuration.md) option.
- an **absolute import** (e.g. `from: "my_package.mixins"`) just has to be importable in
  the environment where the generated code runs; `files_to_include` is not needed.

### Where `@mixin` can be used

The directive is valid in two locations:

- on a **field** - extends the model generated for that field's selection set.
- on a **fragment definition** - extends the model generated for that fragment.

```gql
fragment UserData on User @mixin(from: ".mixins", import: "UsersMixin") {
    id
}
```

### Applying multiple mixins

`@mixin` is repeatable, so you can apply it several times to the same field or
fragment to add multiple base classes (they are added in the order they appear):

```gql
query listUsers {
    users
        @mixin(from: ".mixins", import: "UsersMixin")
        @mixin(from: ".mixins", import: "AuditMixin") {
        id
    }
}
```

```py
from .mixins import AuditMixin, UsersMixin
...
class ListUsersUsers(BaseModel, UsersMixin, AuditMixin):
    ...
```

### Example of usage of `mixin` and `files_to_include`

Query with `mixin` directive:

```gql
query listUsers {
    users @mixin(from: ".mixins", import: "UsersMixin") {
        id
    }
}
```

Part of `pyproject.toml` with `files_to_include` (`mixins.py` contains the
`UsersMixin` implementation):

```toml
files_to_include = [".../mixins.py"]
```

Part of generated `list_users.py` file:

```py
...
from .mixins import UsersMixin
...
class ListUsersUsers(BaseModel, UsersMixin):
    ...
```
