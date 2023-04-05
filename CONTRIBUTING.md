# Contributing

Thank you for your interest in contributing to Ariadne Code Generator!

We welcome bug reports, questions, pull requests, and general feedback.

We also ask all contributors to familiarize themselves with and follow code of conduct, available in the [CODE_OF_CONDUCT.md](https://github.com/mirumee/ariadne/blob/master/CODE_OF_CONDUCT.md) file kept in the main project's repository.


# Reporting bugs, asking for help, offering feedback and ideas

You can use [GitHub issues](https://github.com/mirumee/ariadne-codegen/issues) to report bugs, ask for help, share your ideas, or simply offer feedback. We are curious what you think of Ariadne!


## Development setup

Ariadne Code Generator is written to support Python 3.9, 3.10 and 3.11.

Codebase is formatted using [black](https://github.com/ambv/black) and [isort](https://github.com/PyCQA/isort), the contents of the `ariadne-codegen` package are annotated with types and validated using [mypy](http://mypy-lang.org/index.html). [Pylint](https://github.com/pylint-dev/pylint) is used to catch errors in code.

Tests are developed using [pytest](https://pytest.org/).

Dev requirements can be installed using Pip extras. For example, to install all dependencies for doing local development and running the tests, run `pip install -e .[dev]`.

We require all changes to be done via pull requests, and to be approved by member-ranked users before merging.

All changes should pass these linter checks:

```bash
pylint ariadne_codegen tests
mypy ariadne_codegen --ignore-missing-imports
mypy --strict tests/main/clients/*/expected_client
mypy --strict tests/main/graphql_schemas/*/expected_schema.py
black --check .
isort . --check-only
```


## Working on issues

We consider all issues which are not assigned to anybody as being available for contributors. The **[help wanted](https://github.com/mirumee/ariadne-codegen/labels/help%20wanted)** label is used to single out issues that we consider easier or higher priority on the list of things that we would like to see.

If you've found issue you want to help with, please add your comment to it - this lets other contributors know what issues are being worked on, as well as allowing maintainers to offer guidance and help.


## Pull requests

We don't require pull requests to be followed with bug reports. If you've found a typo or a silly little bug that has no issue or pull request already, you can open your own pull request. We only ask that this PR provides context or explanation for what problem it fixes, or which area of the project it improves.
