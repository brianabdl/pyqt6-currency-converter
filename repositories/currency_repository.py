"""
Repository pattern for currency and exchange rate data management
"""
from typing import Dict, List, Optional
from models import Currency, ExchangeRate
from services import APIService


class CurrencyRepository:
    """Repository for managing Currency entities"""
    
    def __init__(self, api_service: APIService):
        self._api_service = api_service
        self._currencies: Dict[str, Currency] = {}
    
    def load_all(self) -> bool:
        """Load all currencies from API"""
        data = self._api_service.fetch_currency_list()
        if data:
            self._currencies.clear()
            for code, name in data.items():
                currency = Currency(code, name)
                self._currencies[code] = currency
            return True
        return False
    
    def get_by_code(self, code: str) -> Optional[Currency]:
        """Get currency by code"""
        return self._currencies.get(code)
    
    def get_all_codes(self) -> List[str]:
        """Get all currency codes"""
        return list(self._currencies.keys())
    
    def get_all(self) -> Dict[str, Currency]:
        """Get all currencies"""
        return self._currencies.copy()
    
    def exists(self, code: str) -> bool:
        """Check if currency exists"""
        return code in self._currencies


class ExchangeRateRepository:
    """Repository for managing ExchangeRate entities"""
    
    def __init__(self, api_service: APIService, currency_repo: CurrencyRepository):
        self._api_service = api_service
        self._currency_repo = currency_repo
        self._exchange_rates: Dict[str, ExchangeRate] = {}
    
    def refresh_all(self) -> bool:
        """Refresh all exchange rates from API"""
        data = self._api_service.fetch_latest()
        if data and 'rates' in data:
            self._exchange_rates.clear()
            timestamp = data.get('timestamp', 'Unknown')
            
            for code, rate in data['rates'].items():
                currency = self._currency_repo.get_by_code(code)
                name = currency.get_name() if currency else code
                
                exchange_rate = ExchangeRate(code, name, rate, timestamp)
                self._exchange_rates[code] = exchange_rate
            return True
        return False
    
    def get_by_code(self, code: str) -> Optional[ExchangeRate]:
        """Get exchange rate by code"""
        return self._exchange_rates.get(code)
    
    def get_all(self) -> Dict[str, ExchangeRate]:
        """Get all exchange rates"""
        return self._exchange_rates.copy()
    
    def exists(self, code: str) -> bool:
        """Check if exchange rate exists"""
        return code in self._exchange_rates
