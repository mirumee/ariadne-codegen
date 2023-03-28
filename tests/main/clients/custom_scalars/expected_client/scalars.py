from typing import Any, Callable, Dict

from .custom_scalars import Code, parse_code, serialize_code

SCALARS_PARSE_FUNCTIONS: Dict[Any, Callable[[str], Any]] = {Code: parse_code}
SCALARS_SERIALIZE_FUNCTIONS: Dict[Any, Callable[[Any], str]] = {Code: serialize_code}
