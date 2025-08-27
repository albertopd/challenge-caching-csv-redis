from app.caching.cache import Cache
from app.utils.cache_utils import cacheable
from app.utils.time_utils import timed
from app.domain.flight_attributes import FlightAttributes
from app.data_sources.data_source import FlightDataSource


class FlightInsights:
    """
    Provides analytical methods for flight data, including delay statistics and flight counts.

    This class operates on a logical flight data source (FlightDataSource), not directly on raw DataFrames or CSVs.
    All queries use logical domain attributes (see FlightAttributes), and never reference physical column names.
    The data source implementation is responsible for mapping logical attributes to the actual columns in the underlying data.
    This abstraction allows FlightInsights to remain agnostic to changes in the source data format or column names.
    """

    def __init__(
        self, 
        data_source: FlightDataSource, 
        cache: Cache | None = None
    ):
        """
        Initialize FlightInsights with a logical flight data source and optional cache.
        Args:
            data_source (FlightDataSource): Logical flight data source implementing filtering and aggregation.
            cache (Cache | None): Optional cache instance for storing results.
        """
        self.data_source = data_source
        self.cache = cache

    def __validate_months(
        self, 
        months: list[int]
    ) -> list[int]:
        """
        Validate that months is a list of integers between 1 and 12.
        Args:
            months (list[int]): List of month numbers.
        Raises:
            ValueError: If months is not a valid list of integers in range.
        Returns:
            list[int]: Unique, validated month numbers.
        """
        if not all(isinstance(m, int) and 1 <= m <= 12 for m in months):
            raise ValueError("Months must be integers between 1 and 12")
        return list(set(months))

    @timed
    @cacheable
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
            months = self.__validate_months(months)

        ds = self.data_source.filter_by_airline(airline)

        if months:
            ds = ds.filter_by_months(months)

        if ds.is_empty():
            raise ValueError(f"No data found for airline: {airline}" + (f" with months: {months}" if months else ""))

        ds = ds.filter_positive_delays()
        average_delay = ds.mean(FlightAttributes.DEPARTURE_DELAY)

        return average_delay

    @timed
    @cacheable
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
            months = self.__validate_months(months)

        ds = self.data_source.filter_by_airline(airline)

        if months:
            ds = ds.filter_by_months(months)

        if ds.is_empty():
            raise ValueError(f"No data found for airline: {airline}" + (f" with months: {months}" if months else ""))

        ds = ds.filter_positive_delays()
        max_delay = ds.max(FlightAttributes.DEPARTURE_DELAY)

        return max_delay

    @timed
    @cacheable
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

        ds = self.data_source.filter_by_origin_airport(airport)

        if ds.is_empty():
            raise ValueError(f"No data found for airport: {airport}")

        total_flights = ds.count_unique(FlightAttributes.FLIGHT_NUMBER)

        return total_flights
