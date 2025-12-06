"""
Business logic controller for currency conversion
"""
from typing import Tuple, List
from repositories import CurrencyRepository, ExchangeRateRepository


class CurrencyController:
    """Controller handling currency conversion business logic"""
    
    def __init__(self, currency_repo: CurrencyRepository, rate_repo: ExchangeRateRepository):
        self._currency_repo = currency_repo
        self._rate_repo = rate_repo
    
    def initialize(self) -> Tuple[bool, str]:
        """Initialize data by loading currencies and rates"""
        # Load currencies first
        if not self._currency_repo.load_all():
            return False, "Failed to load currency list"
        
        # Then load exchange rates
        if not self._rate_repo.refresh_all():
            return False, "Failed to load exchange rates"
        
        return True, "Data loaded successfully"
    
    def refresh_rates(self) -> Tuple[bool, str]:
        """Refresh exchange rates"""
        if self._rate_repo.refresh_all():
            return True, "Rates refreshed successfully"
        return False, "Failed to refresh rates"
    
    def get_currency_codes(self) -> List[str]:
        """Get list of all available currency codes"""
        return self._currency_repo.get_all_codes()
    
    def get_currency_name(self, code: str) -> str:
        """Get currency name by code"""
        currency = self._currency_repo.get_by_code(code)
        return currency.get_name() if currency else code
    
    def get_available_currencies(self) -> List[Tuple[str, str]]:
        """Get list of (code, name) tuples for all available currencies"""
        codes = self._currency_repo.get_all_codes()
        return [(code, self.get_currency_name(code)) for code in codes]
    
    def get_default_currencies(self) -> Tuple[str, str]:
        """Get default currency codes (from, to)"""
        return "USD", "EUR"
    
    def convert(self, from_code: str, to_code: str, amount: float) -> Tuple[bool, float, str]:
        """
        Convert amount from one currency to another
        Returns: (success, result, message)
        """
        # Validate inputs
        if not from_code or not to_code:
            return False, 0.0, "Please select both currencies"
        
        if amount <= 0:
            return False, 0.0, "Amount must be positive"
        
        # Check if rates exist
        from_rate = self._rate_repo.get_by_code(from_code)
        to_rate = self._rate_repo.get_by_code(to_code)
        
        if not from_rate:
            return False, 0.0, f"Exchange rate not found for {from_code}"
        
        if not to_rate:
            return False, 0.0, f"Exchange rate not found for {to_code}"
        
        # Perform conversion through USD (base currency)
        try:
            amount_in_usd = amount / from_rate.get_rate()
            result = to_rate.calculate(amount_in_usd)
            
            rate_info = f"1 {from_code} = {result/amount:.4f} {to_code}"
            return True, result, rate_info
        except Exception as e:
            return False, 0.0, f"Conversion error: {str(e)}"
    
    def get_conversion_display(self, from_code: str, to_code: str, 
                               amount: float, result: float) -> str:
        """Format conversion result for display"""
        from_name = self.get_currency_name(from_code)
        to_name = self.get_currency_name(to_code)
        
        return (
            f"{amount:,.2f} {from_code} ({from_name})\n"
            f"=\n"
            f"{result:,.2f} {to_code} ({to_name})"
        )
