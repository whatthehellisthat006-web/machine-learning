import time

from fastapi import FastAPI, HTTPException

from app.config import MODE, MODEL_ID, REVIEW_THRESHOLD
from app.providers import get_provider
from app.schemas import LanguageRequest, LanguageResponse


app = FastAPI(
    title="Guichet ML",
    version="1.0.0",
)

provider = get_provider(MODE)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": MODE,
        "provider": provider.name,
    }


@app.post(
    "/detect-language",
    response_model=LanguageResponse,
)
def detect_language(payload: LanguageRequest):
    start_time = time.perf_counter()

    try:
        predictions = provider.detect_language(payload.text)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="Service d'inference indisponible",
        ) from error

    best_prediction = max(
        predictions,
        key=lambda prediction: prediction.score,
    )

    latency_ms = round(
        (time.perf_counter() - start_time) * 1000,
        1,
    )

    return LanguageResponse(
        provider=provider.name,
        model=MODEL_ID,
        latency_ms=latency_ms,
        language=best_prediction.label,
        requires_review=best_prediction.score < REVIEW_THRESHOLD,
        predictions=predictions,
    )