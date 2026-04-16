from app.domain.ports.llm_port import LLMPort
from app.core.exceptions import LLMSafetyBlockedError
from re import S
from google import genai
from app.core.config import settings
from google.genai import types
from app.logger import setup_logger
from google.api_core import exceptions as google_exceptions
from groq import AsyncGroq
from app.core.exceptions import (
    AppError,
    InfrastractureError,
    LLMSafetyBlockedError,
)
import groq
from typing import Any, Dict


class LLMAdapter(LLMPort):

    def __init__(self):
        self.logger = setup_logger("AI Engine")
        self.client = genai.Client()
        self.async_client = self.client.aio
        self.groq_client = AsyncGroq()
        self.embedding_model = settings.GEMINI_EMBEDDING_MODEL
        self.llm_model = settings.GEMINI_LLM_MODEL
        self.groq_llm_model = settings.GROQ_LLM_MODEL

    async def warm_up(self):
        """
        Verification Check: Validates API Key and Network connectivity.
        Runs during the FastAPI lifespan.
        """
        print(f"✨ AI Engine: Warming up {self.llm_model}...")

        # generate embedding
        # embedding_response = await self.generate_embedding("Hello, how are you?")
        llm_response = await self.get_llm_response(
            "Hello, how are you?", system_instruction="You are helpfull assistant"
        )

        if llm_response:
            print("✅ AI Engine: Connectivity verified. Brain is online.")
        else:
            print("❌ AI Engine: Warm-up failed! Check your API_KEY.")

    async def get_llm_response(
        self, prompt, system_instruction, response_format: str = "text"
    ):
        try:
            response = await self.groq_client.chat.completions.create(
                model=self.groq_llm_model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                response_format={"type": response_format},  # type: ignore
                # max_tokens=1024,
            )

            # 🛑 CRITICAL CHECK: safety blocks return a 200 OK
            # but the .text property will be EMPTY or throw an error.
            if not response or not response.choices[0].message.content:
                self.logger.error("❌ AI Engine: No candidates returned from model.")
                raise AppError("No candidates returned from model.")

            # Check for safety blocks
            finish_reason = response.choices[0].finish_reason
            if finish_reason == "SAFETY":
                self.logger.warning(f"🛡️ AI Engine: Response blocked by Safety Filters.")
                raise LLMSafetyBlockedError("Response blocked by Safety Filters.")

            if response.choices[0].message.content is None:
                raise AppError("Response is Empty.")

            return response.choices[0].message.content
        except (groq.APIConnectionError, groq.APITimeoutError) as e:
            raise InfrastractureError("LLM Timeout Error: {str(e)}")
        except Exception as e:
            self.logger.error(
                f"🚨 AI Engine: LLM Generation failed: {str(e)}", exc_info=True
            )
            # For a storefront, we return a graceful fallback instead of crashing
            raise AppError(str(e))

    async def generate_embedding(self, text):
        if not text or len(text.strip()) == 0:
            self.logger.warning("⚠️ Empty text passed for embedding. Skipping.")
            raise AppError("Empty text passed for embedding. Skipping.")

        try:
            response = await self.async_client.models.embed_content(
                model=self.embedding_model,
                contents=text,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT", output_dimensionality=768
                ),
            )

            if not response or not response.embeddings:
                raise AppError("Failed to generate embedding.")

            return response.embeddings[0].values  # type: ignore
        except google_exceptions.GatewayTimeout as e:
            self.logger.error(f"🛑 AI Engine: Timeout error. {e}")
            # In Phase 5, we would add a 'retry' logic here.
            raise InfrastractureError("LLM Timeout Error: {str(e)}")
        except google_exceptions.ResourceExhausted as e:
            self.logger.error(f"🛑 AI Engine: Quota exceeded (Rate Limit). {e}")
            # In Phase 5, we would add a 'retry' logic here.
            raise InfrastractureError("LLM Timeout Error: {str(e)}")
        except google_exceptions.InvalidArgument as e:
            self.logger.error(f"❌ AI Engine: Invalid text or parameters. {e}")
            raise AppError("Invalid text or parameters: {str(e)}")
        except Exception as e:
            self.logger.error(
                f"🚨 AI Engine: Unexpected Error: {str(e)}", exc_info=True
            )
            raise InfrastractureError(str(e))

    async def generate_batch_embeddings(self, texts):
        if not texts:
            self.logger.warning("⚠️ Empty text passed for embedding. Skipping.")
            raise AppError("Empty text passed for embedding. Skipping.")

        try:
            response = await self.async_client.models.embed_content(
                model=self.embedding_model,
                contents=texts,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT", output_dimensionality=768
                ),
            )

            if not response or not response.embeddings:
                raise AppError("Failed to generate embedding.")

            return [embedding.values for embedding in response.embeddings]  # type: ignore
        except google_exceptions.GatewayTimeout as e:
            self.logger.error(f"🛑 AI Engine: Timeout error. {e}")
            # In Phase 5, we would add a 'retry' logic here.
            raise InfrastractureError("LLM Timeout Error: {str(e)}")
        except google_exceptions.ResourceExhausted as e:
            self.logger.error(f"🛑 AI Engine: Quota exceeded (Rate Limit). {e}")
            # In Phase 5, we would add a 'retry' logic here.
            raise InfrastractureError("LLM Timeout Error: {str(e)}")
        except google_exceptions.InvalidArgument as e:
            self.logger.error(f"❌ AI Engine: Invalid text or parameters. {e}")
            raise AppError("Invalid text or parameters: {str(e)}")
        except Exception as e:
            self.logger.error(
                f"🚨 AI Engine: Unexpected Error: {str(e)}", exc_info=True
            )
            raise AppError(str(e))
