import logging
import os

import pandas as pd
from app.domain.flight_insights import FlightInsights
from app.caching.redis_cache import RedisCache

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def setup_redis_cache():
    """
    Set up and return a RedisCache instance using environment variables or defaults.
    Returns:
        RedisCache: Configured Redis cache instance.
    """
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_db = int(os.getenv("REDIS_DB", 0))
    default_exp_in_mins = int(os.getenv("CACHE_EXP_IN_MINS", 1))

    return RedisCache(
        redis_host=redis_host,
        redis_port=redis_port,
        redis_db=redis_db,
        default_exp_in_mins=default_exp_in_mins,
    )


def load_flights_dataframe():
    """
    Load the flights CSV data into a pandas DataFrame.
    Returns:
        pd.DataFrame: DataFrame containing flight data.
    """
    logging.info("Loading flights data...")
    df = pd.read_csv("data/flights.csv", low_memory=False)
    logging.info("Finished loading flights data.")
    return df


def main():
    """
    Main entry point for the application. Sets up cache and data, then prints flight insights.
    """
    try:
        cache = setup_redis_cache()
        flights_df = load_flights_dataframe()
        flight_insights = FlightInsights(flights_df, cache)

        print(f"\nAverage departure delay for VX airline: {int(flight_insights.avg_dep_delay_per_airline('VX'))} minutes\n")

        print(f"\nAverage departure delay for VX airline in summer months (Jun, Jul, Aug): {int(flight_insights.avg_dep_delay_per_airline('VX', [6, 7, 8]))} minutes\n")

        print(f"\nMax departure delay for VX airline: {int(flight_insights.max_dep_delay_per_airline('VX'))} minutes\n")

        print(f"\nMax departure delay for VX airline in December: {int(flight_insights.max_dep_delay_per_airline('VX', [12]))} minutes\n")

        print(f"\nTotal flights for SFO airport: {flight_insights.total_flights_per_origin_airport('SFO')}\n")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
