# app/services/redis_service.py

from typing import Any
from app.core.redis import get_redis
import redis.asyncio as redis

class RedisService:
    def __init__(self, redis_client: redis.Redis | None = None):
        self.redis: redis.Redis = redis_client or get_redis()

    # ---------------------------
    # Basic CRUD
    # ---------------------------
    async def set(self, key: str, value: Any, expire: int | None = None):
        """Set key with optional expiration (seconds)"""
        return await self.redis.set(name=key, value=value, ex=expire)

    async def get(self, key: str):
        """Get key value"""
        return await self.redis.get(key)

    async def delete(self, key: str):
        """Delete key"""
        return await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        return await self.redis.exists(key) > 0

    # ---------------------------
    # Helpers
    # ---------------------------
    async def incr(self, key: str, amount: int = 1):
        """Increment integer key"""
        return await self.redis.incr(name=key, amount=amount)

    async def expire(self, key: str, seconds: int):
        """Set expiration for key"""
        return await self.redis.expire(name=key, time=seconds)

    async def ping(self):
        """Check Redis connection"""
        return await self.redis.ping()
