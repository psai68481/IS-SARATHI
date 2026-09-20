import json
import logging
from typing import Optional, Any
from app.core.config import settings

logger = logging.getLogger("is_sarathi.redis")

class RedisService:
    def __init__(self):
        self.client = None
        self.memory_cache = {}
        if settings.REDIS_ENABLED:
            try:
                import redis
                self.client = redis.from_url(settings.REDIS_URL, decode_responses=True, socket_timeout=2)
                self.client.ping()
                logger.info("Connected to Redis cache.")
            except Exception as e:
                logger.warning(f"Redis unavailable ({e}), using in-memory cache fallback.")
                self.client = None

    def get(self, key: str) -> Optional[Any]:
        try:
            if self.client:
                val = self.client.get(key)
                if val:
                    return json.loads(val)
            else:
                return self.memory_cache.get(key)
        except Exception as e:
            logger.error(f"Error reading from cache: {e}")
            return None

    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> bool:
        try:
            val_str = json.dumps(value)
            if self.client:
                self.client.setex(key, ttl_seconds, val_str)
            else:
                self.memory_cache[key] = value
            return True
        except Exception as e:
            logger.error(f"Error writing to cache: {e}")
            return False

    def delete(self, key: str) -> bool:
        try:
            if self.client:
                self.client.delete(key)
            else:
                self.memory_cache.pop(key, None)
            return True
        except Exception:
            return False

redis_service = RedisService()
