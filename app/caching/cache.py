from abc import ABC, abstractmethod
from typing import Any


class Cache(ABC):
    """
    Abstract base class for cache implementations.
    """

    @abstractmethod
    def set(self, key: str, value: Any, exp_in_mins: int | None = None):
        """
        Set a value in the cache with an optional expiration time in minutes.
        Args:
            key (str): The cache key.
            value (Any): The value to cache.
            exp_in_mins (int | None): Expiration time in minutes. If None, use default.
        """
        ...

    @abstractmethod
    def get(self, key: str) -> Any:
        """
        Retrieve a value from the cache by key.
        Args:
            key (str): The cache key.
        Returns:
            Any: The cached value, or None if not found.
        """
        ...

    @abstractmethod
    def clear(self):
        """
        Clear all values from the cache.
        """
        ...
