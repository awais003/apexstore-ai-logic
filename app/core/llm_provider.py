from app.infrastructure.adapters.llm.gemini_vision_analysis_adapter import (
    GeminiVisionAnalysisAdapter,
)
from app.infrastructure.adapters.llm.llm_adapter import LLMAdapter
from app.core.exceptions import FetalError

_llm_instance: LLMAdapter | None = None


async def init_llm():
    global _llm_instance

    if _llm_instance is None:
        _llm_instance = LLMAdapter()
        await _llm_instance.warm_up()


def get_llm_adapter() -> LLMAdapter:
    if _llm_instance is None:
        raise FetalError("LLM is not initialized")

    return _llm_instance


_vision_analysis_instance: GeminiVisionAnalysisAdapter | None = None


def init_vision_analysis():
    global _vision_analysis_instance

    if _vision_analysis_instance is None:
        _vision_analysis_instance = GeminiVisionAnalysisAdapter()


def get_vision_analysis_adapter() -> GeminiVisionAnalysisAdapter:
    if _vision_analysis_instance is None:
        raise FetalError("Vision Analysis is not initialized")

    return _vision_analysis_instance
