from fastapi import APIRouter, Query

from app.core.enum import SeasonEnum
from app.db.redis.cache import (
    get_cached_recommendations,
    set_cached_recommendations,
    set_recommendation_cache_key,
)
from app.schemas import RecommendationResponse
from app.services.open_ai import get_recommendations
from app.utils.validator import is_valid_country

router: APIRouter = APIRouter()


@router.get("/recommendations", response_model=RecommendationResponse)
async def recommend(
    country: str = Query(..., min_length=1), season: SeasonEnum = Query(...)
):
    if not is_valid_country(country):
        raise ValueError("Invalid country")
    cache_key = set_recommendation_cache_key(country, season)
    cached_result = await get_cached_recommendations(cache_key)
    if cached_result:
        return RecommendationResponse(
            country=country, season=season, recommendations=cached_result
        )

    recommendations = await get_recommendations(country, season)
    await set_cached_recommendations(cache_key, recommendations)
    return RecommendationResponse(
        country=country, season=season, recommendations=recommendations
    )
