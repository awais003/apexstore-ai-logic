import json
from app.core.exceptions import DomainValidationError
from typing import List, Dict


def parse_tags(raw_response: str) -> List[Dict]:
    try:
        products_tags = []
        json_result = json.loads(raw_response)  # type: ignore
        products_array = json_result["products"]

        for r in products_array:
            products_tags.append(
                {"product_id": r.get("product_id"), "tags": r.get("tags", [])}
            )

        return products_tags
    except json.JSONDecodeError:
        raise DomainValidationError("LLM did not return valid JSON.")
