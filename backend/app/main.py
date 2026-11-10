from contextlib import asynccontextmanager
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.init_db import init_db
from app.api.v1.router import api_router
from app.services.user_service import ensure_bootstrap_admin
from app.api.v1.health import record_request
import logging

setup_logging()
logger = logging.getLogger("nexus.http")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await ensure_bootstrap_admin(
        settings.NEXUS_BOOTSTRAP_USERNAME,
        settings.NEXUS_BOOTSTRAP_PASSWORD,
    )
    yield

app = FastAPI(title="Paytm NEXUS AI", version="0.1.0", lifespan=lifespan)


@app.middleware("http")
async def request_observability(request, call_next):
    started = time.perf_counter()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        record_request(status_code, duration_ms)
        logger.info(
            "http_request method=%s path=%s status=%s duration_ms=%s",
            request.method,
            request.url.path,
            status_code,
            duration_ms,
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"service": "paytm-nexus-ai", "docs": "/docs"}
