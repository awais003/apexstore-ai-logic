from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.routes import tagging_api, indexing_api, product_api
from app.core.logging_config import setup_logging
from app.core.vector_provider import init_vector_db
from app.core.llm_provider import init_llm, init_vision_analysis


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create ai engine
    await init_llm()

    # create vector db
    await init_vector_db()

    # create vision analysis
    init_vision_analysis()

    yield

    print("🔌 ApexStore AI shutting down...")


app = FastAPI(
    lifespan=lifespan, title="ApexStore AI", description="ApexStore AI", version="1.0.0"
)

app.include_router(tagging_api.router, prefix="/api/v1")
app.include_router(indexing_api.router, prefix="/api/v1")
app.include_router(product_api.router, prefix="/api/v1/products")


@app.get("/health")
async def health_check():
    return {"status": "online", "brain": "ready"}
