from typing import Optional


class ProductTagPrompt:

    @classmethod
    def get_system_instruction(cls) -> str:

        instructions = """You are a Senior E-commerce SEO Specialist. Generate 8-10 highly relevant, high-conversion search tags for this product.
CRITICAL SEO RULES:

Include 2 'Broad Category' tags (e.g., 'men's running shoes').
Include 3 'Long-Tail' descriptive tags (e.g., 'lightweight marathon trainers', 'breathable mesh sneakers').
Include 3 'Feature/Use-case' tags (e.g., 'daily road running', 'cushioned arch support', 'all-black athletic gear').

Avoid generic one-word tags like 'shoes' or 'footwear'.

Focus on 'Buyer Intent' keywords that real customers type into Google in 2026.

OUTPUT FORMAT: > Return ONLY the tags separated by commas. No quotes, no numbers, no introductory text."""

        return instructions

    @classmethod
    def get_user_content(
        cls, name: str, category: str, description: Optional[str] = None
    ) -> str:
        content = f"Product: {name}\nCategory: {category}"
        if description:
            content += f"\nDescription: {description}"

        content += "\n\nGenerate SEO tags:"
        return content
