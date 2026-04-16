from app.domain.ports.llm_port import LLMPort
from app.domain.ports.webhook_port import WebhookPort
from app.application.dto.product_dto import ProductDto
from app.ai.prompts.tagging_prompt import build_tagging_prompt
from app.domain.parsers.tag_parser import parse_tags
from app.core.exceptions import (
    InfrastractureError,
    TransientError,
    FetalError,
)


class TagProductsUseCase:

    def __init__(
        self,
        llm_Port: LLMPort,
    ):
        self.llm_port = llm_Port

    async def execute(self, products: list[ProductDto]):
        try:
            # 1. build prompt
            prompt = build_tagging_prompt(products=products)

            # 2. generate tags
            system_instruction = "You are expert product tagging assistance"
            raw_response = await self.llm_port.get_llm_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_format="json_object",
            )

            # 3. convert raw response to json
            tags = parse_tags(raw_response=raw_response)

            return tags
        except InfrastractureError as e:
            raise TransientError(f"Infrastracture error : {str(e)}") from e
        except FetalError as e:
            raise FetalError(str(e)) from e
        except Exception as e:
            raise TransientError(f"Unexpected error: {str(e)}") from e
