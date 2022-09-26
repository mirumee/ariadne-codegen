from pathlib import Path

from .client import ClientGenerator
from .init_file import InitFileGenerator
from .utils import ast_to_str


class PackageGenerator:
    def __init__(self, module_name: str, target_path: str) -> None:
        self.module_name = module_name
        self.target_path = target_path
        self.module_path = Path(target_path) / module_name

        self.init_generator = InitFileGenerator()
        self.client_generator = ClientGenerator()

    def _create_init_file(self):
        init_file_path = self.module_path / "__init__.py"
        init_module = self.init_generator.generate()
        init_file_path.write_text(ast_to_str(init_module))

    def _create_client_file(self):
        client_file_path = self.module_path / "client.py"
        client_module = self.client_generator.generate()
        client_file_path.write_text(ast_to_str(client_module))

        self.init_generator.add_import(
            names=[self.client_generator.name], from_="client", level=1
        )

    def generate(self):
        """Generate package with graphql client."""
        self.module_path.mkdir()
        self._create_client_file()
        self._create_init_file()
