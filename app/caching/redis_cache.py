import logging
import pickle
import redis
from typing import Any, cast
from app.caching.cache import Cache


class RedisCache(Cache):
    """
    Implements a cache using Redis as the backend.
    Stores Python objects using pickle serialization and supports expiration.
    """

    def __init__(
        self,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        default_exp_in_mins: int = 60,
    ):
        """
        Create a RedisCache instance and connect to Redis.

        Parameters:
            redis_host (str): Hostname for Redis server.
            redis_port (int): Port for Redis server.
            redis_db (int): Database index for Redis.
            default_exp_in_mins (int): Default expiration time for cache entries (minutes).

        Raises:
            redis.ConnectionError: If connection or ping to Redis fails.
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
        Store a value in Redis under the given key, with optional expiration.
        The value is serialized using pickle.

        Parameters:
            key (str): Cache key.
            value (Any): Python object to cache.
            exp_in_mins (int | None): Expiration time in minutes. Uses default if None.
        """
        if exp_in_mins is None:
            exp_in_mins = self.default_exp_in_mins

        self.client.set(key, pickle.dumps(value), ex=exp_in_mins * 60)
        logging.info(f"Set key: [{key}] with expiration: {exp_in_mins} minutes")

    def get(self, key: str) -> Any:
        """
        Retrieve a value from Redis by key and deserialize it.

        Parameters:
            key (str): Cache key.

        Returns:
            Any: Cached Python object, or None if not found.
        """
        value = cast(bytes | None, self.client.get(key))

        if value is None:
            logging.info(f"Cache miss for key: [{key}]")
            return None
        
        logging.info(f"Cache hit for key: [{key}]")
        return pickle.loads(value)

    def clear(self):
        """
        Remove all keys from the Redis database for this cache instance.
        """
        self.client.flushdb()
        logging.info("Cleared all keys from Redis")
