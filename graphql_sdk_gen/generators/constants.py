from enum import Enum
from typing import Dict, Final

SIMPLE_TYPE_MAP: Final[Dict[str, str]] = {
    "String": "str",
    "ID": "str",
    "Int": "int",
    "Boolean": "bool",
    "Float": "float",
}
OPTIONAL: Final[str] = "Optional"
LIST: Final[str] = "list"
UNION: Final[str] = "Union"
ANY: Final[str] = "Any"


class ClassType(str, Enum):
    ENUM = "ENUM"
    INPUT = "INPUT"
    OBJECT = "OBJECT"
    INTERFACE = "INTERFACE"
