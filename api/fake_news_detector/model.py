from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

MIN_TITLE_LENGTH = 10
MAX_TITLE_LENGTH = 300


def _normalize_title(value: str) -> str:
    title = value.strip()
    if not title:
        raise PydanticCustomError("empty_title", "title must not be empty or only spaces")
    if len(title) < MIN_TITLE_LENGTH:
        raise PydanticCustomError("title_too_short", f"title must have at least {MIN_TITLE_LENGTH} characters")
    if len(title) > MAX_TITLE_LENGTH:
        raise PydanticCustomError("title_too_long", f"title must have at most {MAX_TITLE_LENGTH} characters")
    return title


class TitleInput(BaseModel):
    title: str = Field()

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return _normalize_title(value)


class TitlesInput(BaseModel):
    titles: list[str] = Field(min_length=1, max_length=50)

    @field_validator("titles")
    @classmethod
    def validate_titles(cls, value: list[str]) -> list[str]:
        return [_normalize_title(title) for title in value]


class PredictionResponse(BaseModel):
    title: str
    label: str
    confidence: float


class PredictionsResponse(BaseModel):
    predictions: list[PredictionResponse]
