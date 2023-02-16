from dataclasses import dataclass


@dataclass
class Code:
    prefix: str
    value: str
    suffix: str


def serialize_code(obj: Code) -> str:
    return f"{obj.prefix}-{obj.value}-{obj.suffix}"


def parse_code(obj: str) -> Code:
    prefix, value, suffix = obj.split("-")
    return Code(prefix=prefix, value=value, suffix=suffix)
