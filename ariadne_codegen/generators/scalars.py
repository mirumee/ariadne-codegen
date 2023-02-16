import ast
from dataclasses import dataclass
from typing import List, Optional, cast

from .codegen import (
    generate_ann_assign,
    generate_dict,
    generate_import_from,
    generate_list,
    generate_module,
    generate_name,
    generate_subscript,
    generate_tuple,
)
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

    @property
    def names_to_import(self) -> List[str]:
        return [name for name in (self.type_, self.serialize, self.parse) if name]


class ScalarsDefinitionsGenerator:
    def __init__(self, scalars_data: Optional[List[ScalarData]] = None) -> None:
        self._imports: List[ast.ImportFrom] = [
            generate_import_from(names=[DICT, ANY, CALLABLE], from_=TYPING_MODULE)
        ]
        self._serialize_dict: ast.Dict = generate_dict()
        self._parse_dict: ast.Dict = generate_dict()

        if scalars_data:
            for data in scalars_data:
                self.add_scalar(data)

    def add_scalar(self, data: ScalarData) -> None:
        if data.parse:
            self._parse_dict.keys.append(generate_name(data.type_))
            self._parse_dict.values.append(generate_name(data.parse))

        if data.serialize:
            self._serialize_dict.keys.append(generate_name(data.type_))
            self._serialize_dict.values.append(generate_name(data.serialize))

        if (data.parse or data.serialize) and data.import_:
            self._imports.append(
                generate_import_from(names=data.names_to_import, from_=data.import_)
            )

    def generate(self) -> ast.Module:
        return generate_module(
            body=cast(
                List[ast.stmt],
                [
                    self._imports,
                    self._generate_dict_assignment(
                        name=SCALARS_PARSE_DICT_NAME,
                        dict_=self._parse_dict,
                        callable_annotation=generate_tuple(
                            [
                                generate_list([generate_name("str")]),
                                generate_name(ANY),
                            ]
                        ),
                    ),
                    self._generate_dict_assignment(
                        name=SCALARS_SERIALIZE_DICT_NAME,
                        dict_=self._serialize_dict,
                        callable_annotation=generate_tuple(
                            [
                                generate_list([generate_name(ANY)]),
                                generate_name("str"),
                            ]
                        ),
                    ),
                ],
            )
        )

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
