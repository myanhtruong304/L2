import asyncio
import json
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app.db.redis.cache import cache
from app.main import app

client = TestClient(app)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def clear_cache():
    await cache.clear()


@pytest.mark.anyio
async def test_recommendations_valid():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:
        response = await ac.get("/recommendations?country=Canada&season=winter")
        assert response.status_code == 200
        data = response.json()
        assert data["country"] == "Canada"
        assert data["season"] == "winter"
        assert isinstance(data["recommendations"], list)
        assert len(data["recommendations"]) > 0


@pytest.mark.anyio
async def test_recommendations_cached():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:
        response1 = await ac.get("/recommendations?country=Canada&season=winter")
        assert response1.status_code == 200

        response2 = await ac.get("/recommendations?country=Canada&season=winter")
        assert response2.status_code == 200

        assert response1.json() == response2.json()


@pytest.mark.anyio
async def test_recommendations_invalid_season():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:
        response = await ac.get("/recommendations?country=Canada&season=monsoon")
        assert response.status_code == 422
        data = response.json()
        assert (
            data["detail"][0]["msg"]
            == "Input should be 'summer', 'winter', 'spring' or 'fall'"
        )


@pytest.mark.anyio
async def test_recommendations_missing_params():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:
        response = await ac.get("/recommendations?country=Canada")
        assert (
            response.status_code == 422
        )  # Unprocessable Entity due to missing season parameter
        assert (
            response.status_code == 422
        )  # Unprocessable Entity due to missing season parameter


@pytest.mark.anyio
async def test_concurrent_requests():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:
        responses = await asyncio.gather(
            ac.get("/recommendations?country=Canada&season=winter"),
            ac.get("/recommendations?country=Canada&season=winter"),
            ac.get("/recommendations?country=Canada&season=winter"),
        )

        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["country"] == "Canada"
            assert data["season"] == "winter"
            assert isinstance(data["recommendations"], list)
            assert len(data["recommendations"]) > 0


@pytest.mark.anyio
async def test_recommendations_invalid_country():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:
        response = await ac.get("/recommendations?country=InvalidCountry&season=winter")
        assert response.status_code == 200
        data = response.json()
        assert data["country"] == "InvalidCountry"
        assert data["season"] == "winter"
        assert isinstance(data["recommendations"], list)
        assert data["season"] == "winter"
        assert isinstance(data["recommendations"], list)
