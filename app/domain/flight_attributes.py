class FlightAttributes:
    """
    Logical names for flight data attributes used throughout the domain.

    These constants represent the conceptual attributes in our domain model.
    - The FlightInsights logic only refers to these logical attributes, never the raw database or CSV columns.
    - Each data source implementation is responsible for translating these logical domain attributes into the correct physical column names for its source.
    - This abstraction means FlightInsights does not care if the column names in the source data change; only the data source needs to know how to map them.
    """

    AIRLINE = "airline"
    DEPARTURE_DELAY = "departure_delay"
    MONTH = "month"
    ORIGIN_AIRPORT = "origin_airport"
    FLIGHT_NUMBER = "flight_number"
