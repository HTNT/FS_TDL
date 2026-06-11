import redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_cache(key: str):
    return redis_client.get(key)

def set_cache(key: str, value: str, expire: int = 3600):
    return redis_client.setex(key, expire, value)

def delete_cache(key: str):
    return redis_client.delete(key)
