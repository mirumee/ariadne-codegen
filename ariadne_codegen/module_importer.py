import importlib
import importlib.util
from typing import Any

from .exceptions import ModuleImportError


def get_module_or_attribute(import_str: str) -> Any:
    """Returns module or module's attribute for arbitrary import path."""
    if is_module_str(import_str):
        try:
            module = importlib.import_module(import_str)
        except ModuleNotFoundError as exc:
            raise ModuleImportError(
                f"Incorrect module. Cannot import from {import_str}"
            ) from exc
        return module
    return get_attribute_from_module(import_str)


def is_module_str(import_str: str) -> bool:
    """Returns True if given import path points to module."""
    try:
        spec = importlib.util.find_spec(import_str)
        return spec is not None
    except ModuleNotFoundError:
        return False


def get_attribute_from_module(module_attribute_str: str) -> Any:
    """Returns imported attribute from the module."""
    if "." not in module_attribute_str:
        raise ModuleImportError("Incorrect path. Use an absolute import path.")
    module_str, attribute_name = module_attribute_str.rsplit(".", 1)

    try:
        module = importlib.import_module(module_str)
        attribute = getattr(module, attribute_name)
    except ModuleNotFoundError as exc:
        raise ModuleImportError(
            f"Incorrect module. Cannot import from {module_str}"
        ) from exc
    except AttributeError as exc:
        raise ModuleImportError(
            f"Attribute {attribute_name} not found in module {module_str}"
        ) from exc

    return attribute
