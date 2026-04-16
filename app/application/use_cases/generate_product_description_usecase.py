from app.domain.ports.llm_port import LLMPort
from app.api.v1.schemas.product import ProductDescriptionRequestSchema
from app.domain.entities.product_description import ProductDescription


class GenerateProductDescriptionUsecase:

    def __init__(self, llm_port: LLMPort) -> None:
        self.llm_port = llm_port

    async def execute(self, command: ProductDescriptionRequestSchema) -> str:
        # 1. convert command to entity
        description = ProductDescription(name=command.name, category=command.category)

        # 2. get llm response
        result = await self.llm_port.get_llm_response(
            prompt=description.get_user_content(),
            system_instruction=description.get_system_instruction(),
        )

        return result
