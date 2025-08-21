# Challenge: Caching CSV Data Processing with Redis in Python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/) ![Pandas](https://img.shields.io/badge/pandas-2.3-%23150458.svg?logo=pandas) ![NumPy](https://img.shields.io/badge/numpy-2.3-%23013243.svg?logo=numpy) ![Redis](https://img.shields.io/badge/redis-6.4-red?logo=redis&logoColor=white)

This project aims to demonstrate the use of Redis as a caching layer for processing CSV data in Python. By caching intermediate results, we can significantly speed up data processing tasks, especially when dealing with large datasets.

## ✨ Features

- Caching of CSV data processing results using Redis.
- Efficient retrieval of cached data.
- Easy integration with existing Python data processing workflows.

## 📂 Project Structure

```
challenge-caching-csv-redis/
├── app/
│   ├── cache.py
│   ├── flight_insights.py
│   ├── main.py
│   ├── redis_cache.py
│   └── time_utils.py
├── data/
│   ├── flights.csv
│   └── README.md
├── .env
├── LICENSE
├── README.md
└── requirements.txt
```

## 🚀 How to Install & Run Redis

1. **Install Redis**
	- On Windows: Download from https://github.com/microsoftarchive/redis/releases and run the installer.
	- On macOS: `brew install redis`
	- On Linux: `sudo apt-get install redis-server`

2. **Start Redis Server**
	- On Windows: Run `redis-server.exe` from the installation directory.
	- On macOS/Linux: Run `redis-server`

3. **Verify Redis is Running**
	- Run `redis-cli ping` and expect a reply: `PONG`

## 🏃 How to Run the App

1. Install Python dependencies:
	```sh
	pip install -r requirements.txt
	```

2. Start Redis server (see above).

3. Run the application:
	```sh
	python app/main.py
	```

## 📝 Sample Logs

### On first run (no cache):

```
2025-08-21 21:12:08 [INFO] Successfully connected to Redis!
2025-08-21 21:12:08 [INFO] Loading flights data...
2025-08-21 21:12:18 [INFO] Finished loading flights data.
2025-08-21 21:12:18 [INFO] STARTED function 'avg_dep_delay_per_airline'
2025-08-21 21:12:18 [INFO] Cache miss for key: [avg_dep_delay_VX]
2025-08-21 21:12:18 [INFO] Set key: [avg_dep_delay_VX] with expiration: 1 minutes
2025-08-21 21:12:18 [INFO] FINISHED function 'avg_dep_delay_per_airline' in 0.261304 seconds

Average departure delay for VX airline: 30 minutes

2025-08-21 21:12:18 [INFO] STARTED function 'avg_dep_delay_per_airline'
2025-08-21 21:12:18 [INFO] Cache miss for key: [avg_dep_delay_VX_[8, 6, 7]]
2025-08-21 21:12:18 [INFO] Set key: [avg_dep_delay_VX_[8, 6, 7]] with expiration: 1 minutes
2025-08-21 21:12:18 [INFO] FINISHED function 'avg_dep_delay_per_airline' in 0.228608 seconds

Average departure delay for VX airline in summer months (Jun, Jul, Aug): 28 minutes

2025-08-21 21:12:18 [INFO] STARTED function 'max_dep_delay_per_airline'
2025-08-21 21:12:18 [INFO] Cache miss for key: [max_dep_delay_VX]
2025-08-21 21:12:18 [INFO] Set key: [max_dep_delay_VX] with expiration: 1 minutes
2025-08-21 21:12:18 [INFO] FINISHED function 'max_dep_delay_per_airline' in 0.272232 seconds

Max departure delay for VX airline: 644 minutes

2025-08-21 21:12:18 [INFO] STARTED function 'max_dep_delay_per_airline'
2025-08-21 21:12:18 [INFO] Cache miss for key: [max_dep_delay_VX_[12]]
2025-08-21 21:12:19 [INFO] Set key: [max_dep_delay_VX_[12]] with expiration: 1 minutes
2025-08-21 21:12:19 [INFO] FINISHED function 'max_dep_delay_per_airline' in 0.232055 seconds

Max departure delay for VX airline in December: 363 minutes

2025-08-21 21:12:19 [INFO] STARTED function 'total_flights_per_origin_airport'
2025-08-21 21:12:19 [INFO] Cache miss for key: [total_flights_origin_SFO]
2025-08-21 21:12:19 [INFO] Set key: [total_flights_origin_SFO] with expiration: 1 minutes
2025-08-21 21:12:19 [INFO] FINISHED function 'total_flights_per_origin_airport' in 0.276766 seconds

Total flights for SFO airport: 2640
```

### On second run (cache hit):

```
2025-08-21 21:13:51 [INFO] Successfully connected to Redis!
2025-08-21 21:13:51 [INFO] Loading flights data...
2025-08-21 21:14:00 [INFO] Finished loading flights data.
2025-08-21 21:14:00 [INFO] STARTED function 'avg_dep_delay_per_airline'
2025-08-21 21:14:00 [INFO] Cache hit for key: [avg_dep_delay_VX]
2025-08-21 21:14:00 [INFO] FINISHED function 'avg_dep_delay_per_airline' in 0.001438 seconds

Average departure delay for VX airline: 30 minutes

2025-08-21 21:14:00 [INFO] STARTED function 'avg_dep_delay_per_airline'
2025-08-21 21:14:00 [INFO] Cache hit for key: [avg_dep_delay_VX_[8, 6, 7]]
2025-08-21 21:14:00 [INFO] FINISHED function 'avg_dep_delay_per_airline' in 0.000891 seconds

Average departure delay for VX airline in summer months (Jun, Jul, Aug): 28 minutes

2025-08-21 21:14:00 [INFO] STARTED function 'max_dep_delay_per_airline'
2025-08-21 21:14:00 [INFO] Cache hit for key: [max_dep_delay_VX]
2025-08-21 21:14:00 [INFO] FINISHED function 'max_dep_delay_per_airline' in 0.000811 seconds

Max departure delay for VX airline: 644 minutes

2025-08-21 21:14:00 [INFO] STARTED function 'max_dep_delay_per_airline'
2025-08-21 21:14:00 [INFO] Cache hit for key: [max_dep_delay_VX_[12]]
2025-08-21 21:14:00 [INFO] FINISHED function 'max_dep_delay_per_airline' in 0.000798 seconds

Max departure delay for VX airline in December: 363 minutes

2025-08-21 21:14:00 [INFO] STARTED function 'total_flights_per_origin_airport'
2025-08-21 21:14:00 [INFO] Cache hit for key: [total_flights_origin_SFO]
2025-08-21 21:14:00 [INFO] FINISHED function 'total_flights_per_origin_airport' in 0.001875 seconds

Total flights for SFO airport: 2640
```

## ⚡ Performance Comparison

| Function                            | First run (no cache)         | Second run (cache hit)      |
|:------------------------------------|:-----------------------------|:----------------------------|
| avg_dep_delay_per_airline           | 0.261304 seconds             | 0.001438 seconds            |
| avg_dep_delay_per_airline (summer)  | 0.228608 seconds             | 0.000891 seconds            |
| max_dep_delay_per_airline           | 0.272232 seconds             | 0.000811 seconds            |
| max_dep_delay_per_airline (Dec)     | 0.232055 seconds             | 0.000798 seconds            |
| total_flights_per_origin_airport    | 0.276766 seconds             | 0.001875 seconds            |

Caching with Redis dramatically reduces repeated computation time for the same query.

## 📋 Requirements

- Python 3.13 or later
- Redis server
- Required Python packages listed in `requirements.txt`

## 📜 License

This project is licensed under the [MIT License](LICENSE).


## 👤 Author

- [Alberto Pérez Dávila](https://github.com/albertopd)