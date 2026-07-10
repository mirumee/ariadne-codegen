import importlib
import inspect
from typing import Any

from ..exceptions import ModuleImportError, PluginImportError
from ..module_importer import get_attribute_from_module, is_module_str
from .base import Plugin


def get_plugins_types(plugins_strs: list[str]) -> list[type[Plugin]]:
    classes = []
    for plugin_str in plugins_strs:
        if is_module_str(plugin_str):
            classes.extend(get_plugins_types_from_module(module_str=plugin_str))
        else:
            classes.append(get_plugin_type(plugin_str))
    return classes


def get_plugins_types_from_module(module_str: str) -> list[type[Plugin]]:
    module = importlib.import_module(module_str)
    return [obj for _, obj in inspect.getmembers(module) if is_plugin_type(obj)]


def is_plugin_type(obj: Any) -> bool:
    return inspect.isclass(obj) and obj is not Plugin and issubclass(obj, Plugin)


def get_plugin_type(class_str: str) -> type[Plugin]:
    try:
        class_obj = get_attribute_from_module(class_str)
    except ModuleImportError as e:
        raise PluginImportError(str(e)) from e

    if not is_plugin_type(class_obj):
        raise PluginImportError(f"Selected object {class_str} is not a plugin class.")

    return class_obj
