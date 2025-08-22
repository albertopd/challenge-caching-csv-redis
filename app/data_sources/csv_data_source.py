import polars as pl
from typing import List
from app.data_sources.data_source import FlightDataSource
from app.domain.flight_attributes import FlightAttributes


# Map domain attributes to actual CSV columns
COLUMN_MAPPING = {
    FlightAttributes.AIRLINE: "AIRLINE",
    FlightAttributes.DEPARTURE_DELAY: "DEPARTURE_DELAY",
    FlightAttributes.MONTH: "MONTH",
    FlightAttributes.ORIGIN_AIRPORT: "ORIGIN_AIRPORT",
    FlightAttributes.FLIGHT_NUMBER: "FLIGHT_NUMBER",
}


class CsvFlightDataSource(FlightDataSource):
    """
    FlightDataSource implementation for CSV-backed flight data using Polars.
    Translates logical domain attributes to physical CSV columns via COLUMN_MAPPING.
    Supports filtering and aggregation operations on flight data.
    """

    def __init__(self, lf: pl.LazyFrame):
        """
        Initialize with a Polars LazyFrame containing flight data.
        Args:
            df (pl.LazyFrame): The flight data as a Polars LazyFrame.
        """
        self.lf = lf

    @classmethod
    def from_csv(cls, filepath: str) -> "CsvFlightDataSource":
        """
        Create a CsvFlightDataSource from a CSV file path.
        Args:
            filepath (str): Path to the CSV file.
        Returns:
            CsvFlightDataSource: Instance with loaded flight data.
        """
        df = pl.scan_csv(filepath).select(list(COLUMN_MAPPING.values()))
        return cls(df)

    def filter_by_airline(self, airline: str):
        """
        Return a new CsvFlightDataSource filtered by airline code.
        Args:
            airline (str): Airline code to filter by.
        Returns:
            CsvFlightDataSource: Filtered data source.
        """
        return CsvFlightDataSource(
            self.lf.filter(pl.col(COLUMN_MAPPING[FlightAttributes.AIRLINE]) == airline)
        )

    def filter_by_months(self, months: List[int]):
        """
        Return a new CsvFlightDataSource filtered by a list of months.
        Args:
            months (List[int]): List of month numbers (1-12).
        Returns:
            CsvFlightDataSource: Filtered data source.
        """
        return CsvFlightDataSource(
            self.lf.filter(pl.col(COLUMN_MAPPING[FlightAttributes.MONTH]).is_in(months))
        )

    def filter_positive_delays(self):
        """
        Return a new CsvFlightDataSource containing only flights with positive departure delays.
        Returns:
            CsvFlightDataSource: Filtered data source.
        """
        return CsvFlightDataSource(
            self.lf.filter(pl.col(COLUMN_MAPPING[FlightAttributes.DEPARTURE_DELAY]) > 0)
        )

    def filter_by_origin_airport(self, airport: str):
        """
        Return a new CsvFlightDataSource filtered by origin airport code.
        Args:
            airport (str): Origin airport code to filter by.
        Returns:
            CsvFlightDataSource: Filtered data source.
        """
        return CsvFlightDataSource(
            self.lf.filter(
                pl.col(COLUMN_MAPPING[FlightAttributes.ORIGIN_AIRPORT]) == airport
            )
        )

    def mean(self, column: str) -> float:
        """
        Compute the mean value of the specified logical column.
        Args:
            column (str): Logical domain attribute name.
        Returns:
            float: Mean value.
        """
        return float(
            self.lf.select(pl.col(COLUMN_MAPPING[column]).mean()).collect()[0, 0]
        )

    def max(self, column: str) -> float:
        """
        Compute the maximum value of the specified logical column.
        Args:
            column (str): Logical domain attribute name.
        Returns:
            float: Maximum value.
        """
        return float(
            self.lf.select(pl.col(COLUMN_MAPPING[column]).max()).collect()[0, 0]
        )

    def count_unique(self, column: str) -> int:
        """
        Count the number of unique values in the specified logical column.
        Args:
            column (str): Logical domain attribute name.
        Returns:
            int: Number of unique values.
        """
        return int(
            self.lf.select(pl.col(COLUMN_MAPPING[column]).n_unique()).collect()[0, 0]
        )

    def is_empty(self) -> bool:
        """
        Check if the data source contains no records.
        Returns:
            bool: True if empty, False otherwise.
        """
        return self.lf.limit(1).collect().is_empty()
