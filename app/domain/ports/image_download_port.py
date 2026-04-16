from abc import abstractmethod
from typing import List

from app.domain.entities.image import Image


class ImageDownlaodPort:

    @abstractmethod
    async def download(self, url: str) -> Image:
        pass

    @abstractmethod
    async def download_batch(self, urls: List[str]) -> List[Image]:
        pass
