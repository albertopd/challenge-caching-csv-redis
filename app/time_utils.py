import logging
import time
from functools import wraps


def time_execution(func):
    """
    Decorator to measure and log the execution time of a function.
    Args:
        func (callable): The function to be wrapped.
    Returns:
        callable: The wrapped function with timing.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"STARTED function '{func.__name__}'")

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        logging.info(f"FINISHED function '{func.__name__}' in {end - start:.6f} seconds")
        return result

    return wrapper
