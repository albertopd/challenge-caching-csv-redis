import logging
import os
from app.data_sources.csv_data_source import CsvFlightDataSource
from app.data_sources.data_source import FlightDataSource
from app.domain.flight_insights import FlightInsights
from app.caching.redis_cache import RedisCache


def setup_redis_cache() -> RedisCache:
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


def setup_data_source() -> FlightDataSource:
    """
    Set up and return the flight data source.
    By default, uses CsvFlightDataSource. To swap out for another source (e.g., database),
    implement a new class inheriting FlightDataSource and update this function accordingly.
    Returns:
        FlightDataSource: Configured flight data source instance.
    """
    data_source = CsvFlightDataSource.from_csv("data/flights.csv")
    return data_source


def main():
    """
    Main entry point for the application. Sets up cache and data, then prints flight insights.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    try:
        cache = setup_redis_cache()
        data_source = setup_data_source()
        flight_insights = FlightInsights(data_source, cache)

        avg_departure_delay = int(flight_insights.avg_dep_delay_per_airline("VX"))
        print(
            f"\nAverage departure delay for VX airline: {avg_departure_delay} minutes\n"
        )

        avg_departure_delay_summer = int(
            flight_insights.avg_dep_delay_per_airline("VX", [6, 7, 8])
        )
        print(
            f"\nAverage departure delay for VX airline in summer months (Jun, Jul, Aug): {avg_departure_delay_summer} minutes\n"
        )

        max_departure_delay = int(flight_insights.max_dep_delay_per_airline("VX"))
        print(f"\nMax departure delay for VX airline: {max_departure_delay} minutes\n")

        max_departure_delay_december = int(
            flight_insights.max_dep_delay_per_airline("VX", [12])
        )
        print(
            f"\nMax departure delay for VX airline in December: {max_departure_delay_december} minutes\n"
        )

        total_flights_sfo = int(flight_insights.total_flights_per_origin_airport("SFO"))
        print(f"\nTotal flights originating from SFO airport: {total_flights_sfo}\n")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
