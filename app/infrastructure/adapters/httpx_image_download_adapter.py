import asyncio
from typing import Any, List

import httpx
from langchain_core.utils import raise_for_status_with_text

from app.core.exceptions import ImageDownloadError, InfrastractureError
from app.domain.entities.image import Image
from app.domain.ports.image_download_port import ImageDownlaodPort


class HttpxImageDownloadAdapter(ImageDownlaodPort):

    def __init__(self, timeout: float = 30.0) -> None:
        self.timeout = timeout

    async def download(self, url: str) -> Image:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()

                mime_type = response.headers.get("Content-Type", "")

                image = Image(content=response.content, mime_type=mime_type)

                return image
            except httpx.HTTPStatusError as e:
                raise ImageDownloadError("Unable to download image")
            except (httpx.TimeoutException, httpx.ConnectTimeout) as e:
                raise InfrastractureError("Connection timout")

    async def download_batch(self, urls: List[str]) -> List[Image]:
        tasks = [self.download(url) for url in urls]
        return await asyncio.gather(*tasks)
