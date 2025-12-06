"""
Application configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # API Configuration
    API_ID = os.getenv('APP_ID')
    API_BASE_URL = "https://openexchangerates.org/api/"
    API_TIMEOUT = 10
    
    # Application Configuration
    APP_NAME = "Currency Exchange Converter"
    APP_VERSION = "2.0.0"
    
    # UI Configuration
    WINDOW_WIDTH = 650
    WINDOW_HEIGHT = 600
    DEFAULT_FROM_CURRENCY = "USD"
    DEFAULT_TO_CURRENCY = "IDR"
    DEFAULT_AMOUNT = "1.00"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.API_ID:
            print("Error: APP_ID not found in environment variables")
            return False
        return True
