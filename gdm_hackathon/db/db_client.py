"""
Client script to interact with the Local Database API.
"""

import requests
import json
from typing import Dict, Any, Optional

class DatabaseClient:
    """Client for interacting with the Local Database API."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialize the client.
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url.rstrip('/')
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the database is healthy."""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def get_keys(self) -> Dict[str, Any]:
        """Get all keys in the database."""
        response = requests.get(f"{self.base_url}/keys")
        return response.json()
    
    def is_key_in_cache(self, key: str) -> bool:
        """Check if a key exists in the database."""
        response = requests.get(f"{self.base_url}/cache/{key}")
        return response.json()['exists']
    
    def get_key(self, key: str) -> Optional[Dict[str, Any]]:
        """Get the entry for a specific key."""
        response = requests.get(f"{self.base_url}/entry/{key}")
        if response.status_code == 404:
            return None
        return response.json()['entry']
    
    def set_key(self, key: str, entry: Dict[str, Any]) -> bool:
        """Add or update an entry in the database."""
        response = requests.post(
            f"{self.base_url}/entry/{key}",
            json=entry,
            headers={'Content-Type': 'application/json'}
        )
        return response.status_code == 200
    
    def get_best_entry(self) -> Optional[Dict[str, Any]]:
        """Get the entry with the highest accuracy."""
        response = requests.get(f"{self.base_url}/best")
        if response.status_code == 404:
            return None
        data = response.json()
        return {
            'key': data['best_key'],
            'entry': data['best_entry'],
            'accuracy': data['accuracy']
        }
    
    def get_all_entries(self) -> Dict[str, Any]:
        """Get all entries in the database."""
        response = requests.get(f"{self.base_url}/entries")
        return response.json()
    
    def get_sorted_entries(self) -> Dict[str, Any]:
        """Get all entries sorted by accuracy."""
        response = requests.get(f"{self.base_url}/entries/sorted")
        return response.json()
    
    def clear_database(self) -> bool:
        """Clear all data from the database."""
        response = requests.post(f"{self.base_url}/clear")
        return response.status_code == 200


def test_client():
    """Test the database client with clinical data."""
    
    client = DatabaseClient()
    
    print("=== Testing Database Client ===\n")
    
    # Check health
    health = client.health_check()
    print(f"Database health: {health}")
    print()
    
    # Add some clinical entries
    clinical_entries = [
        ("MW_B_001", {
            "patient_id": "MW_B_001",
            "diagnosis": "Bladder cancer",
            "stage": "T2",
            "accuracy": 0.94,
            "confidence": "high"
        }),
        ("MW_B_002", {
            "patient_id": "MW_B_002",
            "diagnosis": "Bladder cancer", 
            "stage": "T1",
            "accuracy": 0.87,
            "confidence": "medium"
        }),
        ("MW_B_003", {
            "patient_id": "MW_B_003",
            "diagnosis": "Bladder cancer",
            "stage": "T3", 
            "accuracy": 0.91,
            "confidence": "high"
        })
    ]
    
    print("Adding clinical entries...")
    for key, entry in clinical_entries:
        success = client.set_key(key, entry)
        print(f"  Added {key}: {success}")
    
    print()
    
    # Test all methods
    print("=== Testing Client Methods ===")
    
    # Get keys
    keys_data = client.get_keys()
    print(f"1. Keys: {keys_data['keys']}")
    
    # Check if key exists
    print(f"2. MW_B_001 in cache: {client.is_key_in_cache('MW_B_001')}")
    print(f"   NONEXISTENT in cache: {client.is_key_in_cache('NONEXISTENT')}")
    
    # Get specific entry
    entry = client.get_key('MW_B_001')
    print(f"3. MW_B_001 entry: {entry}")
    
    # Get best entry
    best = client.get_best_entry()
    if best:
        print(f"4. Best entry: {best['key']} with accuracy {best['accuracy']}")
    
    # Get sorted entries
    sorted_data = client.get_sorted_entries()
    print(f"5. Sorted entries count: {sorted_data['count']}")
    for item in sorted_data['entries']:
        print(f"   {item['key']}: accuracy={item['entry']['accuracy']}")
    
    print("\n=== Client Test Complete ===")


if __name__ == "__main__":
    test_client() 