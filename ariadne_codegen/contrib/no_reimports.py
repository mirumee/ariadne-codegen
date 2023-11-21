import ast

from ariadne_codegen.plugins.base import Plugin


class NoReimportsPlugin(Plugin):
    def generate_init_module(self, module: ast.Module) -> ast.Module:
        module.body = []
        return module
