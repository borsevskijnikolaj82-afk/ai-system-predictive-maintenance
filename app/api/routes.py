import os
import time
from fastapi import APIRouter, Header, HTTPException
from prometheus_client import Counter, Histogram
from app.api.schemas import HealthResponse, PredictionRequest, PredictionResponse

router = APIRouter()
REQUESTS = Counter("http_requests_total", "HTTP requests", ["endpoint", "status"])
LATENCY = Histogram("http_request_duration_seconds", "HTTP request duration")
MODEL_LATENCY = Histogram("model_inference_duration_seconds", "Model inference duration")
STARTED_AT = time.time()

API_KEY = os.getenv("API_KEY", "dev-secret")


def check_key(x_api_key: str | None) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


@router.post("/api/v1/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest, x_api_key: str | None = Header(default=None)):
    check_key(x_api_key)
    from app.main import prediction_service, repository
    started = time.perf_counter()
    result = prediction_service.predict(payload.model_dump())
    MODEL_LATENCY.observe(time.perf_counter() - started)
    repository.save(result)
    REQUESTS.labels("/api/v1/predict", "200").inc()
    return result


@router.get("/health", response_model=HealthResponse)
def health(x_api_key: str | None = Header(default=None)):
    check_key(x_api_key)
    from app.main import model
    return {
        "status": "healthy" if model.loaded else "degraded",
        "model_loaded": model.loaded,
        "model_version": model.version,
        "uptime_seconds": int(time.time() - STARTED_AT),
    }


@router.get("/metrics")
def metrics():
    from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
    from fastapi.responses import Response
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
