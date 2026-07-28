---
title: Standard plugins
---

# Standard plugins

Ariadne Codegen ships with optional plugins importable from the `ariadne_codegen.contrib` package:

- [`ariadne_codegen.contrib.shorter_results.ShorterResultsPlugin`](https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/contrib/shorter_results.py#L62) - This plugin processes generated client methods for operations where only single top field is requested, so they return this field's value directly instead of operation's result type. For example get_user method generated for query `GetUser() { user(...) { ... }}` will return value of user field directly instead of `GetUserResult`.

- [`ariadne_codegen.contrib.extract_operations.ExtractOperationsPlugin`](https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/contrib/extract_operations.py#L31) - This extracts query strings from generated client's methods into separate `operations.py` module. It also modifies the generated client to import these definitions. Generated module name can be customized by adding `operations_module_name="custom_name"` to the `[tool.ariadne-codegen.extract-operations]` section in config. Eg.:

  ```toml
  [tool.ariadne-codegen]
  ...
  plugins = ["ariadne_codegen.contrib.extract_operations.ExtractOperationsPlugin"]

  [tool.ariadne-codegen.extract-operations]
  operations_module_name = "custom_operations_module_name"
  ```

- [`ariadne_codegen.contrib.client_forward_refs.ClientForwardRefsPlugin`](https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/contrib/client_forward_refs.py#L32) - This plugin changes generated client module moving all Pydantic models imports under the `TYPE_CHECKING` condition, making them forward references. This greatly improves the import performance of the `client` module.

- [`ariadne_codegen.contrib.no_reimports.NoReimportsPlugin`](https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/contrib/no_reimports.py#L6) - This plugin removes content of generated `__init__.py`. This is useful in scenarios where generated modules contain so many Pydantic models that client's eager initialization of entire package on first import is very slow.

- [`ariadne_codegen.contrib.single_file_client.SingleFileClientPlugin`](https://github.com/mirumee/ariadne-codegen/blob/main/ariadne_codegen/contrib/single_file_client.py#L38) - This plugin reads all the generated files, merge them into a single file, and removes the package. This can be useful for small clients with limited number of types and operations. The behavior can be customized as follows; see package file for details:

  ```toml
  [tool.ariadne-codegen]
  ...
  plugins = ["ariadne_codegen.contrib.single_file_client.SingleFileClientPlugin"]

  [tool.ariadne-codegen.single-file-client]
  output_file_name = "my_client.py" # default: client.py
  should_remove_package = false     # default: true

  ```
