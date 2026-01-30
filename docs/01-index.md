---
id: intro
title: Introduction
---

# Ariadne Client based on code generator

Python code generator that takes graphql schema, queries, mutations and subscriptions and generates Python package with fully typed and asynchronous GraphQL client.

It's available as `ariadne-codegen` command and reads configuration from the `pyproject.toml` file:

```
$ ariadne-codegen
```

It can also be run as `python -m ariadne_codegen`.

## Features

- Generate pydantic models from schema types, inputs and enums.
- Generate pydantic models for GraphQL results.
- Generate client package with each GraphQL operation available as async method.

## Installation

Ariadne Code Generator can be installed with pip:

```
$ pip install ariadne-codegen
```

To support subscriptions, default base client requires `websockets` package:

```
$ pip install ariadne-codegen[subscriptions]
```
