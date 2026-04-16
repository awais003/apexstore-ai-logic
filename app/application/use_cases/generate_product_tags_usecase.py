from typing import List

from app.ai.prompts.product_tag_prompt import ProductTagPrompt
from app.api.v1.schemas.product import ProductTagRequestSchema
from app.core.exceptions import AppError
from app.domain.entities.product_tag import ProductTag
from app.domain.ports.llm_port import LLMPort


class GenerateProductTagsUsecase:

    def __init__(self, llm_port: LLMPort) -> None:
        self.llm_port = llm_port

    async def execute(self, command: ProductTagRequestSchema) -> List[str]:
        # 1. generate tags with llm
        result = await self.llm_port.get_llm_response(
            prompt=ProductTagPrompt.get_user_content(
                name=command.name,
                category=command.category,
                description=command.description,
            ),
            system_instruction=ProductTagPrompt.get_system_instruction(),
        )

        # 2. split tags from llm result and remove duplicate
        raw_tags = result.split(",")

        if not raw_tags:
            raise AppError("Unable to generate tags. try again")

        clean_tags = sorted(list(set(t.strip().lower() for t in raw_tags if t.strip())))

        return clean_tags[:12]
