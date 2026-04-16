import json
from app.ai.prompts.image_to_product_prompt import get_image_to_product_prompt
from app.api.v1.schemas.product import ProductVisionRequestSchema
from app.core.exceptions import DomainValidationError, InvalidAIResponse
from app.domain.ports.image_download_port import ImageDownlaodPort
from app.domain.ports.vision_analysis_port import VisionAnalysisPort


class ImageToProductUsecase:

    def __init__(
        self,
        vision_analysis_port: VisionAnalysisPort,
        image_download_port: ImageDownlaodPort,
    ) -> None:
        self.vision_analysis_port = vision_analysis_port
        self.image_download_port = image_download_port

    async def execute(
        self,
        command: ProductVisionRequestSchema,
    ) -> dict:
        # 1. download images
        images = await self.image_download_port.download_batch(command.images)

        # 2. get result from llm
        raw_response = await self.vision_analysis_port.generate(
            prompt=get_image_to_product_prompt(
                categories=[dict(cat) for cat in command.categories]
            ),
            images=images,
            response_type="application/json",
        )

        # 3. parse and validate llm response
        result = self._parse_and_validate_response(raw_response)

        return result

    # validate json data
    def _parse_and_validate_response(self, raw_response: str) -> dict:
        # 1. Parse JSON (Keep this, it's essential)
        try:
            json_data = json.loads(raw_response)
        except json.JSONDecodeError:
            raise DomainValidationError("Invalid JSON returned from LLM")

        # 2. Key Validation (Keep this, but make it flexible)
        required_keys = ["name", "description", "tags", "attributes", "slug", "sku"]
        for key in required_keys:
            if key not in json_data:
                # Logic to log and perhaps re-try or set default
                pass

        # 3. SMART Tag Normalization (Don't kill single words!)
        tags = json_data.get("tags", [])
        # Just clean whitespace and lower-case; let the AI decide the length
        json_data["tags"] = list(dict.fromkeys([t.lower().strip() for t in tags]))[:15]

        # 4. DYNAMIC Attributes (The "Phase 4" Way)
        # Stop forcing 'color/size/material/other'.
        # Let whatever Gemini found STAY as a key-value pair.
        attributes = json_data.get("attributes", {})
        # Only ensure it's a flat dictionary
        json_data["attributes"] = {str(k): v for k, v in attributes.items()}

        category = json_data.get("category")
        # If it's an empty string, a non-dict, or "value" from your prompt template, kill it.
        if not isinstance(category, dict) or not category:
            json_data["category"] = None

        return json_data
