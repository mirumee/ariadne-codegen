from typing import Any, Callable, Dict

SCALARS_PARSE_FUNCTIONS: Dict[Any, Callable[[Any], Any]] = {}
SCALARS_SERIALIZE_FUNCTIONS: Dict[Any, Callable[[Any], Any]] = {}
