from aiocache import Cache

cache = Cache(Cache.MEMORY)


def set_recommendation_cache_key(country: str, seasion: str):
    return f"recommendations:{country}:{seasion}"


async def get_cached_recommendations(key: str):
    return await cache.get(key)


async def set_cached_recommendations(key: str, recommendations: list[str]):
    await cache.set(key, recommendations, ttl=600)
