import sys
from PyQt6.QtWidgets import QApplication

from config import Config
from services import APIService
from repositories import CurrencyRepository, ExchangeRateRepository
from controllers import CurrencyController
from views import MainWindow


def main():
    """Main application entry point"""
    # Validate configuration
    if not Config.validate():
        sys.exit(1)
    
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName(Config.APP_NAME)
    
    # Initialize services (Dependency Injection)
    api_service = APIService(Config.API_ID)
    
    # Initialize repositories
    currency_repo = CurrencyRepository(api_service)
    rate_repo = ExchangeRateRepository(api_service, currency_repo)
    
    # Initialize controller
    controller = CurrencyController(currency_repo, rate_repo)
    
    # Create and show main window
    window = MainWindow(controller)
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()