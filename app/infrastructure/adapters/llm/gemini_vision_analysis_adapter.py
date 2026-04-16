from typing import Any, List

from fastapi import UploadFile
from google import genai
from google.genai import types, errors
from app.core.exceptions import AppError, InfrastractureError, InvalidAIResponse
from app.domain.entities.image import Image
from app.domain.ports.vision_analysis_port import VisionAnalysisPort
from app.core.config import settings


class GeminiVisionAnalysisAdapter(VisionAnalysisPort):

    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_VISION_MODEL

    async def generate(
        self, prompt: str, images: List[Image], response_type: str = "text/plain"
    ) -> str:
        parts = []

        # 1. Process Images using the Part system
        for img_file in images:
            try:
                content = img_file.content
                # Use the SDK's internal Part helper for bytes
                image_part = types.Part.from_bytes(
                    data=content, mime_type=img_file.mime_type or "image/jpeg"
                )
                parts.append(image_part)
                # await img_file.seek(0)  # Reset for potential reuse
            except Exception:
                raise AppError(f"Failed to process")

        # 2. Add the text prompt as a Part
        parts.append(types.Part.from_text(text=prompt))

        # 3. Configure Controlled Generation
        config = types.GenerateContentConfig(
            response_mime_type=response_type,
            temperature=0.1,
        )

        try:
            # 4. Use the models.generate_content method
            response = self.client.models.generate_content(
                model=self.model, contents=parts, config=config
            )

            if not response.text:
                raise InvalidAIResponse("AI returned an empty response.")

            return response.text
        except (TimeoutError, ConnectionError) as e:
            raise InfrastractureError("Failed to connect to AI service.") from e
        except errors.ClientError as e:
            raise InfrastractureError(str(e)) from e
        except errors.ServerError as e:
            raise InfrastractureError(str(e)) from e
