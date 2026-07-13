---
title: File uploads
---

# File uploads

The default base client (`AsyncBaseClient` or `BaseClient`) checks if any part of
the `variables` dictionary is an instance of `Upload`. If at least one instance is
found then the client sends a multipart request according to the
[GraphQL multipart request specification](https://github.com/jaydenseric/graphql-multipart-request-spec).

The `Upload` class is included in the generated client and can be imported from it:

```py
from {target_package_name} import Upload
```

By default this class is used to represent the GraphQL scalar `Upload`. For a schema
with a different name for this scalar, you can still use `Upload` and the default
client for file uploads:

```toml
[tool.ariadne-codegen.scalars.OTHERSCALAR]
type = "Upload"
```

## Constructing an `Upload`

`Upload` takes three required arguments:

- `filename` (`str`) - name reported to the server for the file.
- `content` (a file-like object / `IOBase`, e.g. the result of `open(...)` or an `io.BytesIO`) - the file contents. It is streamed as-is, so open binary files in binary mode (`"rb"`).
- `content_type` (`str`) - MIME type of the file, e.g. `"image/png"`.

```py
from graphql_client import Upload

upload = Upload(
    filename="avatar.png",
    content=open("avatar.png", "rb"),
    content_type="image/png",
)
```

## Full example

Given a mutation that accepts the `Upload` scalar:

```graphql
mutation uploadFile($file: Upload!) {
  fileUpload(file: $file)
}
```

`ariadne-codegen` generates an `upload_file` method that takes a typed `Upload`
argument. Pass an `Upload` instance and the client automatically sends a multipart
request:

```py
import asyncio
from graphql_client.client import Client
from graphql_client import Upload


async def main():
    client = Client(url="https://example.com/graphql")
    with open("avatar.png", "rb") as f:
        result = await client.upload_file(
            file=Upload(filename="avatar.png", content=f, content_type="image/png")
        )
    print(result)


asyncio.run(main())
```

Opening the file inside a `with` block ensures it is closed after the request
completes. Any `Upload` found anywhere in the operation's variables triggers the
multipart request, so this also works for lists of files or nested input objects.

## Disabling multipart uploads

If your schema does not use file uploads, you can set `multipart_uploads = false`
in your config to generate a lighter client that omits multipart handling entirely:

```toml
[tool.ariadne-codegen]
multipart_uploads = false
```
