from unittest.mock import MagicMock


class CustomScalar:
    def __init__(self, value: str) -> None:
        self.value = value


def _parse_custom_scalar(value: str) -> CustomScalar:
    return CustomScalar(value)


mocked_parse = MagicMock(side_effect=_parse_custom_scalar)


def parse_custom_scalar(value: str) -> CustomScalar:
    return mocked_parse(value)


def _serialize_custom_scalar(obj: CustomScalar) -> str:
    return obj.value


mocked_serialize = MagicMock(side_effect=_serialize_custom_scalar)


def serialize_custom_scalar(obj: CustomScalar) -> str:
    return mocked_serialize(obj)
