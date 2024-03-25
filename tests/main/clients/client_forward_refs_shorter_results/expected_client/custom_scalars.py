SimpleScalar = str


class ComplexScalar:
    def __init__(self, value: str) -> None:
        self.value = value


def parse_complex_scalar(value: str) -> ComplexScalar:
    return ComplexScalar(value)


def serialize_complex_scalar(value: ComplexScalar) -> str:
    return value.value
