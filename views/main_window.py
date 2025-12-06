"""
Main view for the Currency Converter application
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QLineEdit, QPushButton, QComboBox, 
                              QGroupBox, QStatusBar, QCompleter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from controllers import CurrencyController


class MainWindow(QMainWindow):
    """Main application window (View in MVC)"""
    
    def __init__(self, controller: CurrencyController):
        super().__init__()
        self._controller = controller
        self._setup_ui()
        self._connect_signals()
        self._load_data()
    
    def _setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Currency Exchange Converter")
        self.setGeometry(100, 100, 650, 600)
        self._apply_styles()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Currency Exchange Converter")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Input section
        input_group = self._create_input_section()
        main_layout.addWidget(input_group)
        
        # Convert button
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.setObjectName("convertBtn")
        self.convert_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        main_layout.addWidget(self.convert_btn)
        
        # Result section
        result_group = self._create_result_section()
        main_layout.addWidget(result_group)
        
        # Refresh button
        refresh_layout = QHBoxLayout()
        refresh_layout.addStretch()
        self.refresh_btn = QPushButton("↻ Refresh Rates")
        self.refresh_btn.setObjectName("refreshBtn")
        self.refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_layout.addWidget(self.refresh_btn)
        main_layout.addLayout(refresh_layout)
        
        main_layout.addStretch()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _create_input_section(self) -> QGroupBox:
        """Create the input section"""
        input_group = QGroupBox("Conversion Details")
        input_layout = QVBoxLayout()
        
        # Amount
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Amount:")
        amount_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.amount_input = QLineEdit("1.00")
        amount_layout.addWidget(amount_label, 1)
        amount_layout.addWidget(self.amount_input, 3)
        input_layout.addLayout(amount_layout)
        
        # Currency selection with swap button
        currency_layout = QHBoxLayout()
        
        # From currency
        from_layout = QVBoxLayout()
        from_label = QLabel("From:")
        from_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.from_combo = QComboBox()
        self.from_combo.setEditable(True)
        from_layout.addWidget(from_label)
        from_layout.addWidget(self.from_combo)
        currency_layout.addLayout(from_layout, 2)
        
        # Swap button
        swap_layout = QVBoxLayout()
        swap_layout.addStretch()
        self.swap_btn = QPushButton("⇄")
        self.swap_btn.setObjectName("swapBtn")
        self.swap_btn.setFixedSize(50, 50)
        self.swap_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        swap_layout.addWidget(self.swap_btn)
        swap_layout.addStretch()
        currency_layout.addLayout(swap_layout, 0)
        
        # To currency
        to_layout = QVBoxLayout()
        to_label = QLabel("To:")
        to_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.to_combo = QComboBox()
        self.to_combo.setEditable(True)
        to_layout.addWidget(to_label)
        to_layout.addWidget(self.to_combo)
        currency_layout.addLayout(to_layout, 2)
        
        input_layout.addLayout(currency_layout)
        input_group.setLayout(input_layout)
        
        return input_group
    
    def _create_result_section(self) -> QGroupBox:
        """Create the result section"""
        result_group = QGroupBox("Result")
        result_layout = QVBoxLayout()
        self.result_label = QLabel("Enter amount and select currencies")
        self.result_label.setObjectName("resultLabel")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setWordWrap(True)
        result_layout.addWidget(self.result_label)
        result_group.setLayout(result_layout)
        
        return result_group
    
    def _apply_styles(self):
        """Apply CSS-like styles to the window"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                font-size: 12pt;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton#convertBtn {
                background-color: #3498db;
                color: white;
            }
            QPushButton#convertBtn:hover {
                background-color: #2980b9;
            }
            QPushButton#swapBtn {
                background-color: #95a5a6;
                color: white;
                font-size: 16pt;
                padding: 5px 15px;
            }
            QPushButton#swapBtn:hover {
                background-color: #7f8c8d;
            }
            QPushButton#refreshBtn {
                background-color: #27ae60;
                color: white;
                font-size: 10pt;
                padding: 5px 10px;
            }
            QPushButton#refreshBtn:hover {
                background-color: #229954;
            }
            QLabel#titleLabel {
                font-size: 20pt;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
            QLabel#resultLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #27ae60;
                padding: 20px;
                background-color: #f8f9fa;
                border-radius: 5px;
                min-height: 80px;
            }
            QStatusBar {
                background-color: #34495e;
                color: white;
                font-size: 9pt;
            }
        """)
    
    def _connect_signals(self):
        """Connect button signals to handlers"""
        self.convert_btn.clicked.connect(self._on_convert)
        self.swap_btn.clicked.connect(self._on_swap)
        self.refresh_btn.clicked.connect(self._on_refresh)
    
    def _load_data(self):
        """Load initial data from controller"""
        success, message = self._controller.initialize()
        
        if success:
            currency_codes = sorted(self._controller.get_currency_codes())
            
            self.from_combo.addItems(currency_codes)
            self.to_combo.addItems(currency_codes)
            
            # Setup autocomplete
            self._setup_autocomplete(self.from_combo, currency_codes)
            self._setup_autocomplete(self.to_combo, currency_codes)
            
            # Set defaults
            self.from_combo.setCurrentText("USD")
            self.to_combo.setCurrentText("IDR")
            
            self.status_bar.showMessage(message)
        else:
            self.result_label.setText(f"⚠ {message}")
            self.status_bar.showMessage(f"Error: {message}")
    
    def _setup_autocomplete(self, combobox: QComboBox, items: list):
        """Setup autocomplete for combobox"""
        completer = QCompleter(items)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchStartsWith)
        combobox.setCompleter(completer)
    
    def _on_convert(self):
        """Handle convert button click"""
        try:
            # Get input values
            amount_str = self.amount_input.text().strip()
            if not amount_str:
                self._show_error("Please enter an amount")
                return
            
            amount = float(amount_str)
            from_code = self.from_combo.currentText()
            to_code = self.to_combo.currentText()
            
            # Perform conversion through controller
            success, result, message = self._controller.convert(from_code, to_code, amount)
            
            if success:
                # Display result
                display_text = self._controller.get_conversion_display(
                    from_code, to_code, amount, result
                )
                self.result_label.setText(display_text)
                self.status_bar.showMessage(f"Conversion successful • Rate: {message}")
            else:
                self._show_error(message)
                
        except ValueError:
            self._show_error("Invalid amount format. Please enter a valid number.")
        except Exception as e:
            self._show_error(f"Conversion failed: {str(e)}")
    
    def _on_swap(self):
        """Handle swap button click"""
        from_text = self.from_combo.currentText()
        to_text = self.to_combo.currentText()
        
        self.from_combo.setCurrentText(to_text)
        self.to_combo.setCurrentText(from_text)
        
        self.status_bar.showMessage("Currencies swapped", 2000)
    
    def _on_refresh(self):
        """Handle refresh button click"""
        self.status_bar.showMessage("Refreshing rates...")
        self.repaint()  # Force UI update
        
        success, message = self._controller.refresh_rates()
        
        if success:
            self.status_bar.showMessage(message, 3000)
        else:
            self._show_error(message)
    
    def _show_error(self, message: str):
        """Display error message"""
        self.result_label.setText(f"⚠ {message}")
        self.status_bar.showMessage(f"Error: {message}")
