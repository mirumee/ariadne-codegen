from io import BytesIO

import pytest


@pytest.fixture
def txt_file(tmp_path):
    file_path = tmp_path / "txt_file.txt"
    file_path.write_text("abcdefgh", encoding="utf-8")
    with open(file_path, "rb") as file_:
        setattr(file_, "content_type", "text/plain")
        yield file_


@pytest.fixture
def png_file(tmp_path):
    file_path = tmp_path / "png_file.png"
    file_path.write_bytes(b"image_content")
    with open(file_path, "rb") as file_:
        setattr(file_, "content_type", "image/png")
        yield file_


@pytest.fixture
def in_memory_txt_file():
    file_ = BytesIO(b"123456")
    setattr(file_, "name", "in_memory.txt")
    setattr(file_, "content_type", "text/plain")
    return file_
