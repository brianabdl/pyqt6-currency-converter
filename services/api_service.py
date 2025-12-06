"""
API Service for external data fetching
"""
import requests
from typing import Optional, Dict


class APIService:
    """Service for interacting with OpenExchangeRates API"""
    
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.base_url = "https://openexchangerates.org/api/"
        self.timeout = 10

    def fetch_latest(self) -> Optional[Dict]:
        """Fetch latest exchange rates"""
        url = f"{self.base_url}latest.json?app_id={self.app_id}"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self._handle_error(e)
            return None

    def fetch_currency_list(self) -> Optional[Dict]:
        """Fetch list of available currencies"""
        url = f"{self.base_url}currencies.json"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self._handle_error(e)
            return None

    def fetch_history(self, date: str) -> Optional[Dict]:
        """Fetch historical exchange rates for a specific date"""
        url = f"{self.base_url}historical/{date}.json?app_id={self.app_id}"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self._handle_error(e)
            return None

    def _handle_error(self, error: Exception):
        """Handle API errors"""
        print(f"API Error: {error}")
