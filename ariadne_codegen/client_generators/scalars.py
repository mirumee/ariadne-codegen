import ast
from dataclasses import dataclass
from typing import List, Optional, cast
from warnings import warn

from ..codegen import (
    generate_ann_assign,
    generate_dict,
    generate_import_from,
    generate_list,
    generate_module,
    generate_name,
    generate_subscript,
    generate_tuple,
)
from ..plugins.manager import PluginManager
from .constants import (
    ANY,
    CALLABLE,
    DICT,
    SCALARS_PARSE_DICT_NAME,
    SCALARS_SERIALIZE_DICT_NAME,
    TYPING_MODULE,
)


@dataclass
class ScalarData:
    type_: str
    serialize: Optional[str] = None
    parse: Optional[str] = None
    import_: Optional[str] = None

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


def generate_scalar_imports(data: ScalarData) -> List[ast.ImportFrom]:
    names_to_import = data.names_to_import
    if data.import_:
        warn(
            'Support for "import" key has been deprecated '
            "and will be dropped in future release. "
            "Instead provide module in type/serialize/parse string.",
            DeprecationWarning,
        )
        return (
            [generate_import_from(names=names_to_import, from_=data.import_)]
            if names_to_import
            else []
        )

    imports = []
    for name in names_to_import:
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

        self._imports: List[ast.ImportFrom] = [
            generate_import_from(names=[DICT, ANY, CALLABLE], from_=TYPING_MODULE)
        ]
        self._serialize_dict: ast.Dict = generate_dict()
        self._parse_dict: ast.Dict = generate_dict()

        for data in scalars_data or []:
            self.add_scalar(data)

    def add_scalar(self, data: ScalarData) -> None:
        if data.parse_name:
            self._parse_dict.keys.append(generate_name(data.type_name))
            self._parse_dict.values.append(generate_name(data.parse_name))

        if data.serialize_name:
            self._serialize_dict.keys.append(generate_name(data.type_name))
            self._serialize_dict.values.append(generate_name(data.serialize_name))

        if data.parse_name or data.serialize_name:
            self._imports.extend(generate_scalar_imports(data))

    def generate(self) -> ast.Module:
        if self.plugin_manager:
            self._parse_dict = self.plugin_manager.generate_scalars_parse_dict(
                self._parse_dict
            )
            self._serialize_dict = self.plugin_manager.generate_scalars_serialize_dict(
                self._serialize_dict
            )
        module = generate_module(
            body=cast(
                List[ast.stmt],
                self._imports
                + [
                    self._generate_dict_assignment(
                        name=SCALARS_PARSE_DICT_NAME,
                        dict_=self._parse_dict,
                        callable_annotation=generate_tuple(
                            [generate_list([generate_name(ANY)]), generate_name(ANY)]
                        ),
                    ),
                    self._generate_dict_assignment(
                        name=SCALARS_SERIALIZE_DICT_NAME,
                        dict_=self._serialize_dict,
                        callable_annotation=generate_tuple(
                            [generate_list([generate_name(ANY)]), generate_name(ANY)]
                        ),
                    ),
                ],
            )
        )
        if self.plugin_manager:
            module = self.plugin_manager.generate_scalars_module(module)
        return module

    def _generate_dict_assignment(
        self,
        name: str,
        dict_: ast.Dict,
        callable_annotation: ast.Tuple,
    ) -> ast.AnnAssign:
        return generate_ann_assign(
            target=generate_name(name),
            annotation=generate_subscript(
                value=generate_name(DICT),
                slice_=generate_tuple(
                    [
                        generate_name(ANY),
                        generate_subscript(
                            value=generate_name(CALLABLE),
                            slice_=callable_annotation,
                        ),
                    ]
                ),
            ),
            value=dict_,
        )
