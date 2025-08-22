import pandas as pd
from app.caching.cache import Cache
from app.utils.timing import time_execution


class FlightInsights:
    """
    Provides analytical methods for flight data, including delay statistics and flight counts.
    """

    _AIRLINE_COLUMN = "AIRLINE"
    _DEPARTURE_DELAY_COLUMN = "DEPARTURE_DELAY"
    _ORIGIN_AIRPORT_COLUMN = "ORIGIN_AIRPORT"
    _FLIGHT_NUMBER_COLUMN = "FLIGHT_NUMBER"

    def __init__(
        self, 
        flights_df: pd.DataFrame, 
        cache: Cache | None = None
    ):
        """
        Initialize FlightInsights with a DataFrame and optional cache.
        Args:
            flights_df (pd.DataFrame): DataFrame containing flight data.
            cache (Cache | None): Optional cache instance for storing results.
        """
        self.flights_df = flights_df
        self.cache = cache

    def _validate_months(self, months: list[int]) -> list[int]:
        """
        Validate that months is a list of integers between 1 and 12.
        Args:
            months (list[int]): List of month numbers.
        Raises:
            ValueError: If months is not a valid list of integers in range.
        """
        if not isinstance(months, list):
            raise ValueError("Months must be a list of integers")
        if not all(isinstance(m, int) for m in months):
            raise ValueError("All months must be integers")
        if any(m < 1 or m > 12 for m in months):
            raise ValueError("Months must be between 1 and 12")

        # Ensure there months are unique
        return list(set(months))

    @time_execution
    def avg_dep_delay_per_airline(
        self, 
        airline: str, 
        months: list[int] | None = None
    ) -> float:
        """
        Calculate the average departure delay for a given airline, optionally filtered by months.
        Args:
            airline (str): Airline code.
            months (list[int] | None): Optional list of months to filter.
        Returns:
            float: Average departure delay in minutes.
        Raises:
            ValueError: If airline is empty or no data found.
        """
        if not airline or airline.strip() == "":
            raise ValueError("Airline name cannot be empty")

        if months:
            months = self._validate_months(months)

        cache_key = f"avg_dep_delay_{airline}_{months}" if months else f"avg_dep_delay_{airline}"

        if self.cache:
            cached_value = self.cache.get(cache_key)
            if cached_value is not None:
                return float(cached_value)

        airline_df = self.flights_df[self.flights_df[FlightInsights._AIRLINE_COLUMN] == airline]

        if months:
            airline_df = airline_df[airline_df["MONTH"].isin(months)]

        if airline_df.empty:
            if months:
                raise ValueError(f"No data found for airline: {airline} with months: {months}")
            else:
                raise ValueError(f"No data found for airline: {airline}")

        late_flights = airline_df[airline_df[FlightInsights._DEPARTURE_DELAY_COLUMN] > 0]
        average_delay = float(late_flights[FlightInsights._DEPARTURE_DELAY_COLUMN].mean(skipna=True))

        if self.cache:
            self.cache.set(cache_key, average_delay)

        return average_delay

    @time_execution
    def max_dep_delay_per_airline(
        self, airline: str, months: list[int] | None = None
    ) -> float:
        """
        Calculate the maximum departure delay for a given airline, optionally filtered by months.
        Args:
            airline (str): Airline code.
            months (list[int] | None): Optional list of months to filter.
        Returns:
            float: Maximum departure delay in minutes.
        Raises:
            ValueError: If airline is empty or no data found.
        """
        if not airline or airline.strip() == "":
            raise ValueError("Airline name cannot be empty")

        if months:
            months = self._validate_months(months)

        cache_key = f"max_dep_delay_{airline}_{months}" if months else f"max_dep_delay_{airline}"

        if self.cache:
            cached_value = self.cache.get(cache_key)
            if cached_value is not None:
                return float(cached_value)

        airline_df = self.flights_df[self.flights_df[FlightInsights._AIRLINE_COLUMN] == airline]

        if months:
            airline_df = airline_df[airline_df["MONTH"].isin(months)]

        if airline_df.empty:
            if months:
                raise ValueError(f"No data found for airline: {airline} with months: {months}")
            else:
                raise ValueError(f"No data found for airline: {airline}")

        late_flights = airline_df[airline_df[FlightInsights._DEPARTURE_DELAY_COLUMN] > 0]
        max_delay = float(late_flights[FlightInsights._DEPARTURE_DELAY_COLUMN].max(skipna=True))

        if self.cache:
            self.cache.set(cache_key, max_delay)

        return max_delay

    @time_execution
    def total_flights_per_origin_airport(self, airport: str) -> int:
        """
        Calculate the total number of unique flights departing from a given airport.
        Args:
            airport (str): Origin airport code.
        Returns:
            int: Total number of unique flights.
        Raises:
            ValueError: If airport is empty or no data found.
        """
        if not airport or airport.strip() == "":
            raise ValueError("Airport name cannot be empty")

        cache_key = f"total_flights_origin_{airport}"

        if self.cache:
            cached_value = self.cache.get(cache_key)
            if cached_value is not None:
                return int(cached_value)

        airport_df = self.flights_df[self.flights_df[FlightInsights._ORIGIN_AIRPORT_COLUMN] == airport]

        if airport_df.empty:
            raise ValueError(f"No data found for airport: {airport}")

        total_flights = int(airport_df[FlightInsights._FLIGHT_NUMBER_COLUMN].nunique(dropna=True))

        if self.cache:
            self.cache.set(cache_key, total_flights)

        return total_flights
