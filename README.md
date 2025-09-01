# Caching Flights Data Redis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/) ![Polars](https://img.shields.io/badge/polars-0.20-%23013243.svg?logo=polars) ![Redis](https://img.shields.io/badge/redis-6.4-red?logo=redis&logoColor=white) ![Docker](https://img.shields.io/badge/docker-26.1-%230db7ed.svg?logo=docker&logoColor=white)

This project demonstrates the use of Redis as a caching layer for processing flights data. By caching intermediate results, data processing tasks become significantly faster, especially with large datasets.

## ✨ Features

* Memory-efficient data processing using **lazy Polars**.
* Flexible data sources — supports CSV, future DB sources, or other adapters.
* Speed up computations — cache expensive aggregations in Redis to avoid recalculating.
* Automatic cache refresh — expired keys are recomputed on demand.
* Pluggable design — generic cache interface allows swapping Redis for another backend.
* Dockerized setup — run both Redis and the Python app easily.

## 📂 Project Structure

```
challenge-caching-csv-redis/
|
├── app/                            # Application source code
|   ├── caching/                    # All cache-related logic
│   │   ├── cache.py                # Generic cache interface
│   │   └── redis_cache.py          # Redis cache implementation
│   │
│   ├── data_sources/               # Data source adapters
│   │   ├── data_source.py       	# Abstract FlightDataSource interface
│   │   └── csv_data_source.py      # CSV/Polars implementation
│   │
│   ├── domain/                     # Domain-specific logic
│   |   ├── flight_attributes.py    # Generic flight attributes
│   │   └── flight_insights.py      # Flight insights logic
│   │
│   ├── utils/                      # Helpers and utilities
|   |   ├── cache_utils.py          # Caching decorator
│   │   └── timing.py               # Execution timing decorator
│   │
│   └── main.py                     # Application entry point
|
├── data/                           # Directory for datasets
│   ├── flights.csv                 # CSV file containing flight records (must be downloaded manually)
│   └── README.md                   # Documentation about how to download the CSV file
|
├── .env                            # Local environment variables
├── LICENSE                         # License information
├── README.md                       # Project documentation
└── requirements.txt                # Python dependencies
```

## 📋 Requirements

- Python 3.13 or later
- Redis server (if not using Docker)
- Required Python packages listed in [requirements.txt](requirements.txt)

## 📦 Installation

### Manual Installation (without Docker)

1. Clone the repository:
	```sh
	git clone https://github.com/albertopd/challenge-caching-csv-redis.git
	cd challenge-caching-csv-redis
	```
2. Install Python dependencies:
	```sh
	pip install -r requirements.txt
	```
3. Install and start Redis (see [official docs](https://redis.io/docs/)).

### Using Docker & Docker Compose

1. Clone the repository:
	```sh
	git clone https://github.com/albertopd/challenge-caching-csv-redis.git
	cd challenge-caching-csv-redis
	```

2. Build and start service and app:
	```sh
	docker-compose up --build
	```

	This starts both Redis and the Python app in separate containers.

## ⚙️ Configuration

Configuration is managed via the `.env` file. Example:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
CACHE_EXP_IN_MINS=1
```

* Adjust these values to match your environment or Docker setup.
* The `docker-compose.yml` automatically loads `.env` for the app service.

## 🚀 Usage

### Running Manually

Start Redis, then run the app:

```sh
python -m app.main
```

### Running with Docker Compose

```sh
docker-compose up --build
docker compose logs -f app
```

## 📝 Example Output Logs

**On first run (no cache):**

```
2025-08-21 21:12:08 [INFO] Successfully connected to Redis!
2025-08-21 21:12:08 [INFO] Loading flights data...
2025-08-21 21:12:18 [INFO] Finished loading flights data.
2025-08-21 21:12:18 [INFO] STARTED function 'avg_dep_delay_per_airline'
2025-08-21 21:12:18 [INFO] Cache miss for key: [avg_dep_delay_VX]
2025-08-21 21:12:18 [INFO] Set key: [avg_dep_delay_VX] with expiration: 1 minutes
2025-08-21 21:12:18 [INFO] FINISHED function 'avg_dep_delay_per_airline' in 0.261304 seconds

Average departure delay for VX airline: 30 minutes
...
```

**On second run (cache hit):**

```
2025-08-21 21:13:51 [INFO] Successfully connected to Redis!
2025-08-21 21:13:51 [INFO] Loading flights data...
2025-08-21 21:14:00 [INFO] Finished loading flights data.
2025-08-21 21:14:00 [INFO] STARTED function 'avg_dep_delay_per_airline'
2025-08-21 21:14:00 [INFO] Cache hit for key: [avg_dep_delay_VX]
2025-08-21 21:14:00 [INFO] FINISHED function 'avg_dep_delay_per_airline' in 0.001438 seconds

Average departure delay for VX airline: 30 minutes
...
```

## ⚡ Performance Comparison

| Function                            | First run (no cache)         | Second run (cache hit)      |
|:------------------------------------|:-----------------------------|:----------------------------|
| avg_dep_delay_per_airline           | 0.261304 seconds             | 0.001438 seconds            |
| avg_dep_delay_per_airline (summer)  | 0.228608 seconds             | 0.000891 seconds            |
| max_dep_delay_per_airline           | 0.272232 seconds             | 0.000811 seconds            |
| max_dep_delay_per_airline (Dec)     | 0.232055 seconds             | 0.000798 seconds            |
| total_flights_per_origin_airport    | 0.276766 seconds             | 0.001875 seconds            |

Redis caching dramatically reduces repeated computation time for the same queries.

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## 👤 Author

[Alberto Pérez Dávila](https://github.com/albertopd)
