import importlib
import importlib.util
import inspect
from typing import Any, List, Type

from ..exceptions import PluginImportError
from .base import Plugin


def get_plugins_types(plugins_strs: List[str]) -> List[Type[Plugin]]:
    classes = []
    for plugin_str in plugins_strs:
        if is_module_str(plugin_str):
            classes.extend(get_plugins_types_from_module(module_str=plugin_str))
        else:
            classes.append(get_plugin_type(plugin_str))
    return classes


def is_module_str(plugin_str: str) -> bool:
    try:
        spec = importlib.util.find_spec(plugin_str)
        return spec is not None
    except ModuleNotFoundError:
        return False


def get_plugins_types_from_module(module_str: str) -> List[Type[Plugin]]:
    module = importlib.import_module(module_str)
    return [obj for _, obj in inspect.getmembers(module) if is_plugin_type(obj)]


def is_plugin_type(obj: Any) -> bool:
    return inspect.isclass(obj) and obj is not Plugin and issubclass(obj, Plugin)


def get_plugin_type(class_str: str) -> Type[Plugin]:
    last_dot_index = class_str.rfind(".")
    if last_dot_index < 0:
        raise PluginImportError("Incorrect plugin path. Use an absolute import path.")
    module_str, class_name = (
        class_str[:last_dot_index],
        class_str[last_dot_index + 1 :],
    )

    try:
        module = importlib.import_module(module_str)
        class_obj = getattr(module, class_name)
    except ModuleNotFoundError as exc:
        raise PluginImportError(
            f"Incorrect plugin module. Cannot import from {module_str}"
        ) from exc
    except AttributeError as exc:
        raise PluginImportError(
            f"Class {class_name} not found in module {module_str}"
        ) from exc

    if not is_plugin_type(class_obj):
        raise PluginImportError(f"Selected object {class_str} is not a plugin class.")

    return class_obj
