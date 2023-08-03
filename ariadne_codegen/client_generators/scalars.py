import ast
from dataclasses import dataclass
from typing import List, Optional, cast
from warnings import warn

from ..codegen import (
    generate_assign,
    generate_call,
    generate_import_from,
    generate_module,
    generate_name,
    generate_subscript,
    generate_tuple,
)
from ..plugins.manager import PluginManager
from .constants import (
    ANNOTATED,
    BEFORE_VALIDATOR,
    PLAIN_SERIALIZER,
    PYDANTIC_MODULE,
    TYPING_MODULE,
)


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

    @property
    def annotation_type_name(self) -> str:
        name = self.graphql_name
        if self.graphql_name == self.type_name:
            name += "_"

        return name


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


class ScalarsDefinitionsGenerator:
    def __init__(
        self,
        scalars_data: Optional[List[ScalarData]] = None,
        plugin_manager: Optional[PluginManager] = None,
    ) -> None:
        self.plugin_manager = plugin_manager
        self.scalars_data = scalars_data or []

        self._imports: List[ast.ImportFrom] = [
            generate_import_from(names=[ANNOTATED], from_=TYPING_MODULE),
            generate_import_from(
                names=[PLAIN_SERIALIZER, BEFORE_VALIDATOR], from_=PYDANTIC_MODULE
            ),
        ]
        self._types_assigns: List[ast.Assign] = []
        for data in self.scalars_data:
            self.add_scalar(data)

    def add_scalar(self, data: ScalarData) -> None:
        annotated_values: List[ast.expr] = [generate_name(data.type_name)]
        if data.serialize_name:
            annotated_values.append(
                generate_call(
                    func=generate_name(PLAIN_SERIALIZER),
                    args=[generate_name(data.serialize_name)],
                )
            )
        if data.parse_name:
            annotated_values.append(
                generate_call(
                    func=generate_name(BEFORE_VALIDATOR),
                    args=[generate_name(data.parse_name)],
                )
            )

        if len(annotated_values) > 1:
            type_assign = generate_assign(
                targets=[data.annotation_type_name],
                value=generate_subscript(
                    value=generate_name(ANNOTATED),
                    slice_=generate_tuple(annotated_values),
                ),
            )
        else:
            type_assign = generate_assign(
                targets=[data.annotation_type_name], value=annotated_values[0]
            )

        if self.plugin_manager:
            type_assign = self.plugin_manager.generate_scalar_annotation(
                type_assign, scalar_name=data.graphql_name
            )
        self._types_assigns.append(type_assign)

        imports = generate_scalar_imports(data)
        if self.plugin_manager:
            imports = self.plugin_manager.generate_scalar_imports(
                imports, scalar_name=data.graphql_name
            )
        self._imports.extend(imports)

    def generate(self) -> ast.Module:
        module = generate_module(
            body=cast(
                List[ast.stmt],
                self._imports + self._types_assigns,
            )
        )
        if self.plugin_manager:
            module = self.plugin_manager.generate_scalars_module(module)
        return module
