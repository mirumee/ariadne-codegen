from ast import ImportFrom, alias


def generate_import_from(modules: list[str], from_: str, level: int = 0) -> ImportFrom:
    names = [alias(m) for m in modules]
    return ImportFrom(module=from_, names=names, level=level)
