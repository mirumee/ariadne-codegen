import pytest


@pytest.fixture
def txt_file(tmp_path):
    file_path = tmp_path / "txt_file.txt"
    file_path.write_text("abcdefgh", encoding="utf-8")
    return file_path


@pytest.fixture
def png_file(tmp_path):
    file_path = tmp_path / "png_file.png"
    file_path.write_bytes(b"image_content")
    return file_path
