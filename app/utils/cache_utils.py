from typing import Callable, Any
from functools import wraps


def cacheable(func: Callable):
    """
    Decorator to cache method results using the class's `cache` attribute.

    The decorated method must belong to a class that has a `self.cache`
    attribute implementing the Cache interface, or None.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        cache = getattr(self, "cache", None)
        if cache is None:
            # No cache available → fallback to direct execution
            return func(self, *args, **kwargs)

        # Build a unique readable cache key from method name + args + kwargs
        key = f"{func.__qualname__}({args}, {kwargs})"

        # Try to fetch from cache
        cached_value = cache.get(key)
        if cached_value is not None:
            return cached_value

        # Otherwise compute & cache
        result = func(self, *args, **kwargs)
        cache.set(key, result)
        return result

    return wrapper
