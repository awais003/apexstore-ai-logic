import json
from typing import Any, Dict, List

from app.api.v1.schemas.categoy import ProductVisionCategorySchema


def get_image_to_product_prompt(categories: List[Dict[str, Any]]) -> str:
    category_instruction = _get_category_instruction(categories=categories)

    prompt = f"""
ACT AS: A Senior E-commerce Merchandiser and SEO Copywriter.
TASK: Analyze the attached images to generate a professional product listing.

### 1. IDENTITY & TITLE
- Generate a premium Title using this EXACT formula: 
  [Gender]'s [Color] [Brand/Style] [Material] [Category] – [Benefit 1] [Benefit 2]
- Example: "Men's Black UrbanFlex Knit Mesh Sneakers – Lightweight Breathable Comfort"
- Use an En Dash (–) to separate the name from the benefits.
- Do not exceed 75 characters.

### 2. DYNAMIC CATEGORIZATION (CRITICAL)
{category_instruction}

### 3. BENEFIT-DRIVEN DESCRIPTION
- Write 2 professional paragraphs. 
- The Hook (Paragraph 1): Write 2 professional sentences focusing on Lifestyle Fit. Start with the "When" and "Where" (e.g., "From urban commutes to weekend adventures...").
- The Value (Paragraph 2): Write 2 professional sentences focusing on Emotional Value and long-term comfort. Why does the customer need this?
- Key Features (Bullet Points): Include a section titled "Key Features" followed by 3-5 bullet points using the * symbol.
  - Each bullet must follow the Feature -> Benefit formula (e.g., "Knit Mesh Upper: Provides maximum breathability to keep feet cool during high-intensity activity").
- NO Repetition: Do NOT repeat the product title verbatim.
- Formatting: Use a single line break between paragraphs and a double line break before the bullet points.
- Tone: Maintain an aspirational yet practical tone (like Nike or Allbirds).
- Scannability: Ensure the most important technical spec (e.g., "Lightweight") is mentioned in the first bullet point.

### 4. TECHNICAL ATTRIBUTES
- Extract 5-8 specific key-value pairs (e.g., 'closure_type', 'sole_material', 'water_resistance').
- Omit any 'null' or 'unknown' values. Do not use a generic 'other' field.

### 5. SEO & SEARCH
- 12-15 Long-Tail tags (e.g., "breathable gym sneakers" instead of "shoes").
- A Google-optimized meta_title (max 60 chars).

### 6. OUTPUT FORMAT
Return strictly valid JSON:
{{
  "name": "string",
  "description": "string",
  "category": {{"id": value, "name": "value"}} or null,
  "attributes": {{ "key": "value" }},
  "tags": ["string"],
  "seo_meta_title": "string",
  "slug": "string",
  "sku": "string"
}}
"""
    return prompt


def _get_category_instruction(categories: List[Dict[str, Any]]) -> str:
    categories_json = json.dumps([cat for cat in categories], ensure_ascii=False)
    """
        Generates the conditional instruction for the AI.
        """
    if not categories:
        return "CATEGORIZATION: Do not suggest a category. Return an empty string for the 'category' field."

    return (
        f"CATEGORIZATION: You must select the most appropriate category ONLY from this list: [{categories_json}]. "
        f"If none match perfectly, leave it null. Do not invent new categories."
    )
