from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    country: str
    season: str
    recommendations: list[str]
