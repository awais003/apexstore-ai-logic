from abc import ABC, abstractmethod
from typing import List
from fastapi import UploadFile

from app.domain.entities.image import Image


class VisionAnalysisPort(ABC):

    @abstractmethod
    async def generate(
        self, prompt: str, images: List[Image], response_type: str = "text/plain"
    ) -> str:
        pass
