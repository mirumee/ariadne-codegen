import ast

from graphql import GraphQLSchema

from ariadne_codegen.plugins.base import Plugin
from ariadne_codegen.plugins.manager import PluginManager


def test_init_creates_plugins_instances():
    class TestPlugin(Plugin):
        pass

    manager = PluginManager(schema=GraphQLSchema(), plugins_classes=[TestPlugin])

    assert len(manager.plugins) == 1
    assert isinstance(manager.plugins[0], TestPlugin)


def test_generate_init_module_calls_all_plugins(mocker):
    mocked_plugin_class1 = mocker.MagicMock()
    mocked_plugin_class2 = mocker.MagicMock()
    manager = PluginManager(
        schema=GraphQLSchema(),
        plugins_classes=[mocked_plugin_class1, mocked_plugin_class2],
    )

    manager.generate_init_module(ast.Module(body=[]))

    assert manager.plugins[0].generate_init_module.called
    assert manager.plugins[1].generate_init_module.called
