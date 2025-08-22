from abc import ABC, abstractmethod
from typing import List


class FlightDataSource(ABC):
    """
    Abstract base class for flight data sources.
    Defines the interface for filtering and aggregating flight data.
    Implementations should provide methods for filtering by airline, months, delays, and origin airport,
    as well as computing mean, max, unique counts, and checking for emptiness.
    """

    @abstractmethod
    def filter_by_airline(self, airline: str) -> "FlightDataSource":
        """
        Return a new FlightDataSource filtered by the given airline code.
        Args:
            airline (str): Airline code to filter by.
        Returns:
            FlightDataSource: Filtered data source.
        """
        ...

    @abstractmethod
    def filter_by_months(self, months: List[int]) -> "FlightDataSource":
        """
        Return a new FlightDataSource filtered by the given list of months.
        Args:
            months (List[int]): List of month numbers (1-12).
        Returns:
            FlightDataSource: Filtered data source.
        """
        ...

    @abstractmethod
    def filter_positive_delays(self) -> "FlightDataSource":
        """
        Return a new FlightDataSource containing only flights with positive delays.
        Returns:
            FlightDataSource: Filtered data source.
        """
        ...

    @abstractmethod
    def filter_by_origin_airport(self, airport: str) -> "FlightDataSource":
        """
        Return a new FlightDataSource filtered by the given origin airport code.
        Args:
            airport (str): Origin airport code to filter by.
        Returns:
            FlightDataSource: Filtered data source.
        """
        ...

    @abstractmethod
    def mean(self, column: str) -> float:
        """
        Compute the mean value of the specified column in the data source.
        Args:
            column (str): Column name to compute mean for.
        Returns:
            float: Mean value.
        """
        ...

    @abstractmethod
    def max(self, column: str) -> float:
        """
        Compute the maximum value of the specified column in the data source.
        Args:
            column (str): Column name to compute max for.
        Returns:
            float: Maximum value.
        """
        ...

    @abstractmethod
    def count_unique(self, column: str) -> int:
        """
        Count the number of unique values in the specified column.
        Args:
            column (str): Column name to count unique values for.
        Returns:
            int: Number of unique values.
        """
        ...

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Check if the data source contains no records.
        Returns:
            bool: True if empty, False otherwise.
        """
        ...
