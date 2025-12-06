"""
Currency domain models
"""

class Currency:
    """Represents a currency with code and name"""
    
    def __init__(self, code, name):
        self.__code = code
        self.__name = name

    def get_code(self):
        return self.__code

    def get_name(self):
        return self.__name
    
    def __str__(self):
        return f"{self.__code} - {self.__name}"
    
    def __repr__(self):
        return f"Currency(code='{self.__code}', name='{self.__name}')"


class ExchangeRate(Currency):
    """Represents an exchange rate for a currency"""
    
    def __init__(self, code, name, rate, last_update):
        super().__init__(code, name)
        self.__rate = rate
        self.__last_update = last_update

    def get_rate(self):
        return self.__rate
    
    def get_last_update(self):
        return self.__last_update

    def calculate(self, amount):
        """Calculate converted amount using this rate"""
        return amount * self.__rate

    def to_string(self):
        return f"{self.get_code()}: {self.__rate}"
    
    def __str__(self):
        return f"{self.get_code()} - Rate: {self.__rate}"
    
    def __repr__(self):
        return f"ExchangeRate(code='{self.get_code()}', rate={self.__rate})"
