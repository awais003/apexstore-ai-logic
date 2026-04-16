from app.domain.entities.entity import Entity
from app.core.exceptions import DomainValidationError


class ProductDescription(Entity):

    def __init__(self, name: str, category: str) -> None:
        self.name = name
        self.category = category

    def _validate(self):
        if not self.name:
            raise DomainValidationError("name cannot be empty")
        if not self.category:
            raise DomainValidationError("category cannot be empty")

    def get_system_instruction(self) -> str:
        return (
            "You are a high-end e-commerce copywriter for ApexStore AI. "
            "Your goal is to write persuasive product descriptions. "
            "Constraints: Use bullet points for features, keep it under 150 words, "
            "and always output in text format."
        )

    def get_user_content(self) -> str:
        return f"Generate a description for the product '{self.name}' in the '{self.category}' category."
