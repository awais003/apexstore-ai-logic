from typing import List, Dict
from app.application.dto.product_dto import ProductDto


def build_tagging_prompt(products: List[ProductDto]) -> str:
    items = []
    for product in products:
        block = (
            f"----PRODUCT START----"
            f"Product ID: {product.id}\n"
            f"Product Name: {product.name}\n"
            f"Product Description: {product.description}\n"
            f"----PRODUCT END----\n"
        )
        items.append(block)

    products_text = "\n\n".join(items)
    prompt = """
        Generate up to 5 highly relevant tags for the following products:

        Rules:
        1. Tags should be highly relevant to the product.
        2. Tags should be in lowercase.
        3. Return only a JSON array of objects.

        Products Data:
        {products_text}

        Example Output format(JSON):
        {{
            "products": [
                {{
                    "product_id": 1,
                    "tags": ["wireless", "bluetooth", "electronics"]
                }}
            ]
        }}
        """

    return prompt.format(products_text=products_text)
