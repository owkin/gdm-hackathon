"""
Simple local database app that manages JSON data with heap queue for accuracy-based sorting.
"""

import json
import os
import heapq
from typing import Dict, Any, List, Tuple, Optional


class LocalDatabase:
    """
    A simple local database that stores data in JSON format with a heap queue
    for accuracy-based sorting.
    """
    
    def __init__(self, json_file_path: str = "local_db.json"):
        """
        Initialize the database.
        
        Args:
            json_file_path: Path to the JSON file for data storage
        """
        self.json_file_path = json_file_path
        self.data: Dict[str, Any] = {}
        self.keys: List[str] = []
        self.accuracy_heap: List[Tuple[float, str]] = []  # (accuracy, key) pairs
        
        # Load existing data if file exists
        self._load_data()
    
    def _load_data(self):
        """Load data from JSON file if it exists."""
        if os.path.exists(self.json_file_path):
            try:
                with open(self.json_file_path, 'r') as f:
                    self.data = json.load(f)
                self.keys = list(self.data.keys())
                self._rebuild_heap()
                print(f"Loaded {len(self.keys)} entries from {self.json_file_path}")
            except Exception as e:
                print(f"Error loading data: {e}")
                self.data = {}
                self.keys = []
                self.accuracy_heap = []
        else:
            print(f"Creating new database at {self.json_file_path}")
    
    def _save_data(self):
        """Save data to JSON file."""
        try:
            with open(self.json_file_path, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def _rebuild_heap(self):
        """Rebuild the accuracy heap from current data."""
        self.accuracy_heap = []
        for key, entry in self.data.items():
            accuracy = entry.get('accuracy', 0.0)
            heapq.heappush(self.accuracy_heap, (accuracy, key))
    
    def is_healthy(self) -> bool:
        """
        Check if the database is healthy.
        
        Returns:
            True if database is healthy, False otherwise
        """
        try:
            # Check if we can access the data
            _ = len(self.data)
            _ = len(self.keys)
            _ = len(self.accuracy_heap)
            return True
        except Exception:
            return False
    
    def is_key_in_cache(self, key: str) -> bool:
        """
        Check if a key exists in the database.
        
        Args:
            key: The key to check
            
        Returns:
            True if key exists, False otherwise
        """
        return key in self.data
    
    def get_key(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get the entry for a specific key.
        
        Args:
            key: The key to retrieve
            
        Returns:
            The entry dictionary if key exists, None otherwise
        """
        return self.data.get(key)
    
    def set_key(self, key: str, entry: Dict[str, Any]) -> bool:
        """
        Add or update an entry in the database.
        
        Args:
            key: The key for the entry
            entry: The entry data (must contain 'accuracy' field)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure entry has accuracy field
            if 'accuracy' not in entry:
                entry['accuracy'] = 0.0
            
            # Add/update the entry
            self.data[key] = entry
            
            # Update keys list if new key
            if key not in self.keys:
                self.keys.append(key)
            
            # Update heap
            accuracy = entry['accuracy']
            heapq.heappush(self.accuracy_heap, (accuracy, key))
            
            # Save to file
            self._save_data()
            
            return True
        except Exception as e:
            print(f"Error setting key {key}: {e}")
            return False
    
    def get_best_entry(self) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        Get the entry with the highest accuracy.
        
        Returns:
            Tuple of (key, entry) for the best entry, or None if database is empty
        """
        if not self.accuracy_heap:
            return None
        
        # Get the entry with highest accuracy (heap stores min-heap, so we need to find max)
        best_accuracy = max(acc for acc, _ in self.accuracy_heap)
        best_key = None
        
        # Find the key with best accuracy
        for accuracy, key in self.accuracy_heap:
            if accuracy == best_accuracy:
                best_key = key
                break
        
        if best_key and best_key in self.data:
            return best_key, self.data[best_key]
        
        return None
    
    def get_all_entries(self) -> Dict[str, Any]:
        """
        Get all entries in the database.
        
        Returns:
            Dictionary of all entries
        """
        return self.data.copy()
    
    def get_accuracy_sorted_entries(self) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Get all entries sorted by accuracy (highest first).
        
        Returns:
            List of (key, entry) tuples sorted by accuracy
        """
        sorted_entries = []
        for accuracy, key in sorted(self.accuracy_heap, reverse=True):
            if key in self.data:
                sorted_entries.append((key, self.data[key]))
        return sorted_entries
    
    def clear(self):
        """Clear all data from the database."""
        self.data = {}
        self.keys = []
        self.accuracy_heap = []
        self._save_data()
        print("Database cleared")


# Example usage and testing
if __name__ == "__main__":
    # Create database instance
    db = LocalDatabase("test_db.json")
    
    # Test the methods
    print(f"Database healthy: {db.is_healthy()}")
    
    # Add some test entries
    test_entries = [
        ("patient_001", {"name": "John Doe", "age": 45, "accuracy": 0.95}),
        ("patient_002", {"name": "Jane Smith", "age": 32, "accuracy": 0.87}),
        ("patient_003", {"name": "Bob Johnson", "age": 58, "accuracy": 0.92}),
    ]
    
    for key, entry in test_entries:
        success = db.set_key(key, entry)
        print(f"Added {key}: {success}")
    
    # Test queries
    print(f"Keys in cache: {db.keys}")
    print(f"Is patient_001 in cache: {db.is_key_in_cache('patient_001')}")
    print(f"Get patient_001: {db.get_key('patient_001')}")
    
    best_entry = db.get_best_entry()
    if best_entry:
        key, entry = best_entry
        print(f"Best entry: {key} with accuracy {entry['accuracy']}")
    
    print(f"All entries sorted by accuracy:")
    for key, entry in db.get_accuracy_sorted_entries():
        print(f"  {key}: {entry['accuracy']}") 