import ast
from dataclasses import dataclass, field
from typing import List, Optional, cast

from .codegen import (
    generate_ann_assign,
    generate_dict,
    generate_import_from,
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
class ExtraImportData:
    from_: str
    import_: str


@dataclass
class ScalarData:
    type: str
    serialize: Optional[str] = None
    parse: Optional[str] = None
    extra_imports: List[ExtraImportData] = field(default_factory=list)

    def __post_init__(self):
        imports_data = []
        for extra_import in self.extra_imports:
            if isinstance(extra_import, dict):
                imports_data.append(ExtraImportData(**extra_import))
        self.extra_imports = imports_data


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
            self._parse_dict.keys.append(generate_name(data.type))
            self._parse_dict.values.append(generate_name(data.parse))

        if data.serialize:
            self._serialize_dict.keys.append(generate_name(data.type))
            self._serialize_dict.values.append(generate_name(data.serialize))

        if (data.parse or data.serialize) and data.extra_imports:
            for extra_import in data.extra_imports:
                self._imports.append(
                    generate_import_from(
                        names=[extra_import.import_], from_=extra_import.from_
                    )
                )

    def generate(self) -> ast.Module:
        return generate_module(
            body=cast(
                List[ast.stmt],
                [
                    self._imports,
                    self._generate_dict_assignment(
                        SCALARS_PARSE_DICT_NAME, self._parse_dict
                    ),
                    self._generate_dict_assignment(
                        name=SCALARS_SERIALIZE_DICT_NAME, dict_=self._serialize_dict
                    ),
                ],
            )
        )

    def _generate_dict_assignment(self, name: str, dict_: ast.Dict) -> ast.AnnAssign:
        return generate_ann_assign(
            target=generate_name(name),
            annotation=generate_subscript(
                value=generate_name(DICT),
                slice_=generate_tuple([generate_name(ANY), generate_name(CALLABLE)]),
            ),
            value=dict_,
        )
