from typing import Any  # this file needs to pass mypy --strict


class CustomAsyncBaseClient:
    async def execute(self, query: Any, variables: Any) -> Any:
        pass

    def get_data(self, response: Any) -> Any:
        pass
