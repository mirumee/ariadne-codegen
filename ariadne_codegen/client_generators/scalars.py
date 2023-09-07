import ast
from dataclasses import dataclass
from typing import List, Optional
from warnings import warn

from ..codegen import (
    generate_call,
    generate_import_from,
    generate_name,
    generate_subscript,
    generate_tuple,
)
from .constants import ANNOTATED, BEFORE_VALIDATOR, PLAIN_SERIALIZER
from .types import Annotation


@dataclass
class ScalarData:
    type_: str
    serialize: Optional[str] = None
    parse: Optional[str] = None
    import_: Optional[str] = None
    graphql_name: str = ""

    def __post_init__(self) -> None:
        self.type_name: str = self._get_object_name(self.type_)
        self.parse_name: Optional[str] = (
            self._get_object_name(self.parse) if self.parse else None
        )
        self.serialize_name: Optional[str] = (
            self._get_object_name(self.serialize) if self.serialize else None
        )

        self.names_to_import: List[str] = [
            name for name in (self.type_, self.serialize, self.parse) if name
        ]

    def _get_object_name(self, name: str) -> str:
        if "." in name:
            _, object_name = name.rsplit(".", maxsplit=1)
            return object_name
        return name


def generate_result_scalar_annotation(data: ScalarData) -> Annotation:
    name_annotation = generate_name(name=data.type_name)

    if data.parse_name:
        return generate_subscript(
            value=generate_name(ANNOTATED),
            slice_=generate_tuple(
                [
                    name_annotation,
                    generate_call(
                        func=generate_name(BEFORE_VALIDATOR),
                        args=[generate_name(data.parse_name)],
                    ),
                ]
            ),
        )

    return name_annotation


def generate_input_scalar_annotation(data: ScalarData) -> Annotation:
    name_annotation = generate_name(name=data.type_name)

    if data.serialize_name:
        return generate_subscript(
            value=generate_name(ANNOTATED),
            slice_=generate_tuple(
                [
                    name_annotation,
                    generate_call(
                        func=generate_name(PLAIN_SERIALIZER),
                        args=[generate_name(data.serialize_name)],
                    ),
                ]
            ),
        )

    return name_annotation


def generate_scalar_imports(data: ScalarData) -> List[ast.ImportFrom]:
    imports = []

    if data.import_:
        warn(
            'Support for "import" key has been deprecated '
            "and will be dropped in future release. "
            "Instead provide module in type/serialize/parse string.",
            DeprecationWarning,
        )
        if data.names_to_import:
            imports.append(
                generate_import_from(names=data.names_to_import, from_=data.import_)
            )

    for name in data.names_to_import:
        if "." in name:
            module_name, object_name = name.rsplit(".", maxsplit=1)
            imports.append(generate_import_from(names=[object_name], from_=module_name))

    return imports
