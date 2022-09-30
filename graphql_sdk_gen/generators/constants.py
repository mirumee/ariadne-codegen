from typing import Final, Dict

SIMPLE_TYPE_MAP: Final[Dict[str, str]] = {
    "String": "str",
    "ID": "str",
    "Int": "int",
    "Boolean": "bool",
    "Float": "float",
}
OPTIONAL: Final[str] = "Optional"
LIST: Final[str] = "list"
