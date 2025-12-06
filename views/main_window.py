"""
Main view for the Currency Converter application  
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QLabel)
from PyQt6.QtCore import Qt
from controllers import CurrencyController
from .sidebar import Sidebar
from .converter_view import ConverterView

class MainWindow(QMainWindow):
    """Main application window with Sidebar Navigation"""
    
    def __init__(self, controller: CurrencyController):
        super().__init__()
        self._controller = controller
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the main window layout with sidebar and content area"""
        self.setWindowTitle("Currency Converter Pro")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(900, 650)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout (Horizontal: Sidebar | Content)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 1. Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        # 2. Content Area (Stacked Widget)
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # -- Page 1: Converter View --
        self.converter_view = ConverterView(self._controller)
        self.content_stack.addWidget(self.converter_view)
        
        # -- Page 2: History View (Placeholder) --
        self.history_view = self._create_placeholder_view("Transaction History", "Coming soon...")
        self.content_stack.addWidget(self.history_view)
        
        # -- Page 3: Settings View (Placeholder) --
        self.settings_view = self._create_placeholder_view("Settings", "App configuration options")
        self.content_stack.addWidget(self.settings_view)
        
        # Connect Sidebar to Stack
        self.sidebar.page_changed.connect(self.content_stack.setCurrentIndex)
        
        # Set background color for content area
        self.content_stack.setStyleSheet("background-color: #f8f9fa;")

    def _create_placeholder_view(self, title: str, subtitle: str) -> QWidget:
        """Create a simple placeholder view for unimplemented pages"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        label = QLabel(f"{title}\n\n{subtitle}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; color: #5f6368;")
        
        layout.addWidget(label)
        return widget

