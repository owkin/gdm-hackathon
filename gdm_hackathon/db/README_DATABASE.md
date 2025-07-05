# Local Database API

A simple local database that stores data in JSON format with a heap queue for accuracy-based sorting. The database is exposed as a REST API for easy integration with other scripts.

## Features

- **JSON Storage**: Data is persisted in a JSON file
- **Accuracy-based Sorting**: Uses a heap queue to maintain entries sorted by accuracy
- **REST API**: Exposed as a web service for easy integration
- **Simple Interface**: Clean API with all the required methods

## Quick Start

### 1. Start the API Server

```bash
# From the gdm_hackathon directory
python db/start_db_api.py
```

The API will be available at `http://localhost:5000`

### 2. Use the Client

```python
from gdm_hackathon.db import DatabaseClient

# Create client
client = DatabaseClient()

# Add an entry
entry = {
    "patient_id": "MW_B_001",
    "diagnosis": "Bladder cancer",
    "stage": "T2",
    "accuracy": 0.94,
    "confidence": "high"
}
client.set_key("MW_B_001", entry)

# Get the best entry
best = client.get_best_entry()
print(f"Best entry: {best['key']} with accuracy {best['accuracy']}")
```

## API Endpoints

### Health Check
- **GET** `/health` - Check if database is healthy

### Keys Management
- **GET** `/keys` - Get all keys in the database
- **GET** `/cache/<key>` - Check if key exists in cache

### Entry Operations
- **GET** `/entry/<key>` - Get entry for a specific key
- **POST** `/entry/<key>` - Add/update entry for a key
- **GET** `/best` - Get entry with highest accuracy
- **GET** `/entries` - Get all entries
- **GET** `/entries/sorted` - Get entries sorted by accuracy

### Database Management
- **POST** `/clear` - Clear all data from database

## Required Methods Implementation

All the required methods are implemented:

1. **`is_healthy()`** - Returns True if database is healthy, False otherwise
2. **`is_key_in_cache(key)`** - Returns True if key in cache, else False
3. **`get_key(key)`** - Returns the dict in the JSON at the key position
4. **`set_key(key, entry)`** - Adds a new entry in the JSON, updates heap queue and key list
5. **`get_best_entry()`** - Uses the heap queue to find the best key and return the corresponding entry

## Example Usage

### Direct Database Usage

```python
from gdm_hackathon.db import LocalDatabase

# Create database
db = LocalDatabase("my_data.json")

# Add entries
db.set_key("patient_001", {"name": "John", "accuracy": 0.95})
db.set_key("patient_002", {"name": "Jane", "accuracy": 0.87})

# Get best entry
best = db.get_best_entry()
print(f"Best: {best[0]} with accuracy {best[1]['accuracy']}")
```

### API Usage

```python
import requests

# Add entry
entry = {"name": "John", "accuracy": 0.95}
response = requests.post("http://localhost:5000/entry/patient_001", json=entry)

# Get best entry
response = requests.get("http://localhost:5000/best")
best = response.json()
print(f"Best: {best['best_key']} with accuracy {best['accuracy']}")
```

### Client Usage

```python
from gdm_hackathon.db import DatabaseClient

client = DatabaseClient()

# Add entry
client.set_key("patient_001", {"name": "John", "accuracy": 0.95})

# Check if exists
exists = client.is_key_in_cache("patient_001")  # True

# Get entry
entry = client.get_key("patient_001")

# Get best
best = client.get_best_entry()
```

## Data Structure

Each entry in the database should have an `accuracy` field for sorting:

```json
{
  "patient_id": "MW_B_001",
  "diagnosis": "Bladder cancer",
  "stage": "T2",
  "accuracy": 0.94,
  "confidence": "high"
}
```

## Files

- `local_db.py` - Core database implementation
- `db_api.py` - Flask API server
- `db_client.py` - Python client for API
- `start_db_api.py` - Startup script with dependency checking
- `test_local_db.py` - Test script for direct database usage

## Dependencies

- `flask` - For the web API
- `requests` - For the client (optional, for API usage)

The startup script will automatically install missing dependencies. 