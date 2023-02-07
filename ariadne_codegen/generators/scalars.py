from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ExtraImportData:
    from_: str
    import_: str


@dataclass
class ScalarData:
    type_name: str
    serialize_method: Optional[str] = None
    serialize_function: Optional[str] = None
    extra_imports: List[ExtraImportData] = field(default_factory=list)

    def __post_init__(self):
        imports_data = []
        for extra_import in self.extra_imports:
            if isinstance(extra_import, dict):
                imports_data.append(ExtraImportData(**extra_import))
        self.extra_imports = imports_data
