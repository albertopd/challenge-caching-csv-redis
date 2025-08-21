import logging
import redis
from typing import Any
from app.cache import Cache


class RedisCache(Cache):
    """
    Redis-backed cache implementation.
    Provides methods to set, get, and clear cache using Redis.
    """

    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        default_exp_in_mins: int = 60,
    ):
        """
        Initialize RedisCache and establish connection with Redis server.
        Args:
            redis_host (str): Redis server hostname.
            redis_port (int): Redis server port.
            redis_db (int): Redis database number.
            default_exp_in_mins (int): Default expiration time in minutes.
        """
        client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
        )
        self.default_exp_in_mins = default_exp_in_mins

        # Verify that Redis is responding
        ping = client.ping()
        if ping is True:
            self.client = client
            logging.info("Successfully connected to Redis!")
        else:
            raise redis.ConnectionError("Connection established but ping failed.")

    def set(self, key: str, value: Any, exp_in_mins: int | None = None):
        """
        Set a value in Redis cache with an optional expiration time.
        Args:
            key (str): The cache key.
            value (Any): The value to cache.
            exp_in_mins (int | None): Expiration time in minutes. If None, use default.
        """
        if exp_in_mins is None:
            exp_in_mins = self.default_exp_in_mins

        self.client.set(key, value, ex=exp_in_mins * 60)
        logging.info(f"Set key: [{key}] with expiration: {exp_in_mins} minutes")

    def get(self, key: str) -> Any:
        """
        Retrieve a value from Redis cache by key.
        Args:
            key (str): The cache key.
        Returns:
            Any: The cached value, or None if not found.
        """
        value = self.client.get(key)

        if value is not None:
            logging.info(f"Cache hit for key: [{key}]")
            return value

        logging.info(f"Cache miss for key: [{key}]")
        return None

    def clear(self):
        """
        Clear all keys from Redis cache.
        """
        self.client.flushdb()
        logging.info("Cleared all keys from Redis")
