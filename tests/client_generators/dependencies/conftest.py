from io import BytesIO

import pytest

from ariadne_codegen.client_generators.dependencies.base_model import Upload


@pytest.fixture
def txt_file(tmp_path):
    file_path = tmp_path / "txt_file.txt"
    file_path.write_text("abcdefgh", encoding="utf-8")
    with open(file_path, "rb") as file_:
        yield Upload(filename="txt_file.txt", content=file_, content_type="text/plain")


@pytest.fixture
def png_file(tmp_path):
    file_path = tmp_path / "png_file.png"
    file_path.write_bytes(b"image_content")
    with open(file_path, "rb") as file_:
        yield Upload(filename="png_file.png", content=file_, content_type="image/png")


@pytest.fixture
def in_memory_txt_file():
    return Upload(
        filename="in_memory.txt", content=BytesIO(b"123456"), content_type="text/plain"
    )
