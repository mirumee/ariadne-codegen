import asyncio
import json
from io import BytesIO
from typing import Any

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


class _MockWebSocket:
    """Fake websocket that yields a sequence of messages and records sent data."""

    def __init__(self, messages: list[str]) -> None:
        self._messages = list(messages)
        self._index = 0
        self.sent: list[str] = []

    async def send(self, data: str) -> None:
        self.sent.append(data)

    async def recv(self) -> str:
        if self._index >= len(self._messages):
            await asyncio.Future()  # wait forever
        msg = self._messages[self._index]
        self._index += 1
        return msg

    def __aiter__(self) -> "_MockWebSocket":
        return self

    async def __anext__(self) -> str:
        if self._index >= len(self._messages):
            raise StopAsyncIteration
        msg = self._messages[self._index]
        self._index += 1
        return msg

    async def close(self) -> None:
        pass


def _ws_message(type: str, **payload: Any) -> str:
    if payload:
        return json.dumps({"type": type, "payload": payload})
    return json.dumps({"type": type})
