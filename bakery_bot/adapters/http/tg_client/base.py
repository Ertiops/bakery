from abc import abstractmethod
from io import BytesIO
from typing import Protocol


class ITGClient(Protocol):
    @abstractmethod
    async def fetch_photo(self, *, path: str) -> BytesIO:
        raise NotImplementedError
