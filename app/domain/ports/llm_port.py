from typing import List, Protocol


class LLMPort:

    async def get_llm_response(
        self, prompt: str, system_instruction: str, response_format: str = "text"
    ) -> str: ...

    async def generate_embedding(self, text: str) -> List[float]: ...

    async def generate_batch_embeddings(
        self, texts: List[str]
    ) -> List[List[float]]: ...

    async def warm_up(self): ...
