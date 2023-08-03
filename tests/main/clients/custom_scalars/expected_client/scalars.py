from datetime import datetime
from typing import Annotated

from pydantic import BeforeValidator, PlainSerializer

from .custom_scalars import Code, parse_code, serialize_code

CUSTOMID = int
DATETIME = datetime
CODE = Annotated[Code, PlainSerializer(serialize_code), BeforeValidator(parse_code)]
