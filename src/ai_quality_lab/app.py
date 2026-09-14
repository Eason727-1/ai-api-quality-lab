from uuid import uuid4

from fastapi import FastAPI, Response

from . import __version__
from .models import EvaluationRequest, EvaluationResponse
from .quality import evaluate_quality


app = FastAPI(
    title="AI API Quality Lab",
    version=__version__,
    description="Deterministic quality gates for AI-generated answers.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/v1/evaluate", response_model=EvaluationResponse)
def evaluate(payload: EvaluationRequest, response: Response) -> EvaluationResponse:
    trace_id = str(uuid4())
    response.headers["X-Trace-Id"] = trace_id
    result = evaluate_quality(payload)
    return EvaluationResponse(
        passed=result.passed,
        score=result.score,
        dimensions=result.dimensions,
        matched_keywords=result.matched_keywords,
        missing_keywords=result.missing_keywords,
        risk_flags=result.risk_flags,
        trace_id=trace_id,
    )

