from typing import Any, Callable, Dict

from .custom_scalars import Code, parse_code, serialize_code

SCALARS_PARSE_FUNCTIONS: Dict[Any, Callable[[Any], Any]] = {Code: parse_code}
SCALARS_SERIALIZE_FUNCTIONS: Dict[Any, Callable[[Any], Any]] = {Code: serialize_code}
