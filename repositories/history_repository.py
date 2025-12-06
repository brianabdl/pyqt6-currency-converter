"""
Repository for managing transaction history
"""
import json
import os
from typing import List
from models.transaction import Transaction

class HistoryRepository:
    """Handles storage and retrieval of transaction history"""
    
    def __init__(self, storage_file: str = "history.json"):
        self._storage_file = storage_file
        self._transactions: List[Transaction] = []
        self._load()
    
    def add(self, transaction: Transaction):
        """Add a new transaction and save"""
        self._transactions.insert(0, transaction) # Add to beginning (newest first)
        self._save()
    
    def get_all(self) -> List[Transaction]:
        """Get all transactions"""
        return self._transactions
    
    def clear(self):
        """Clear all history"""
        self._transactions = []
        self._save()
    
    def _save(self):
        """Save transactions to file"""
        try:
            data = [t.to_dict() for t in self._transactions]
            with open(self._storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def _load(self):
        """Load transactions from file"""
        if not os.path.exists(self._storage_file):
            return
            
        try:
            with open(self._storage_file, 'r') as f:
                data = json.load(f)
                self._transactions = [Transaction.from_dict(item) for item in data]
        except Exception as e:
            print(f"Error loading history: {e}")
            self._transactions = []
