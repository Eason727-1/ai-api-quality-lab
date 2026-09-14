from typing import Annotated

from pydantic import BaseModel, Field, field_validator


Keyword = Annotated[str, Field(min_length=1, max_length=80)]


class EvaluationRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    answer: str = Field(min_length=1, max_length=4000)
    expected_keywords: list[Keyword] = Field(default_factory=list, max_length=20)
    forbidden_phrases: list[Keyword] = Field(default_factory=list, max_length=20)
    pass_threshold: int = Field(default=70, ge=0, le=100)

    @field_validator("question", "answer")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text must not be blank")
        return value

    @field_validator("expected_keywords", "forbidden_phrases")
    @classmethod
    def normalize_phrase_lists(cls, values: list[str]) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()
        for item in values:
            cleaned = item.strip()
            if not cleaned:
                raise ValueError("phrases must not be blank")
            key = cleaned.casefold()
            if key not in seen:
                normalized.append(cleaned)
                seen.add(key)
        return normalized


class QualityDimensions(BaseModel):
    keyword_coverage: int = Field(ge=0, le=100)
    clarity: int = Field(ge=0, le=100)
    safety: int = Field(ge=0, le=100)


class EvaluationResponse(BaseModel):
    passed: bool
    score: int = Field(ge=0, le=100)
    dimensions: QualityDimensions
    matched_keywords: list[str]
    missing_keywords: list[str]
    risk_flags: list[str]
    trace_id: str

