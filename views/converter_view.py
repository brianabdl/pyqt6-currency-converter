"""
Converter view for the Currency Converter application
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QComboBox, QFrame, 
                              QCompleter, QStatusBar)
from PyQt6.QtCore import Qt, QTimer
from controllers import CurrencyController

class MaterialCard(QFrame):
    """Material Design card widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.Box)
        self.setObjectName("materialCard")

class ConverterView(QWidget):
    """
    The main conversion interface, extracted from MainWindow
    to allow for a multi-page navigation structure.
    """
    
    def __init__(self, controller: CurrencyController):
        super().__init__()
        self._controller = controller
        self._setup_ui()
        self._connect_signals()
        self._load_data()
    
    def _setup_ui(self):
        """Setup the Material Design user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header section
        header_section = self._create_header_section()
        main_layout.addWidget(header_section)
        
        # Input card
        input_card = self._create_input_card()
        main_layout.addWidget(input_card)
        
        # Exchange rate info
        self.rate_info_label = QLabel("")
        self.rate_info_label.setObjectName("rateInfo")
        self.rate_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rate_info_label.setWordWrap(True)
        main_layout.addWidget(self.rate_info_label)
        
        # Result card
        result_card = self._create_result_card()
        main_layout.addWidget(result_card)
        
        # Action buttons
        actions_layout = self._create_action_buttons()
        main_layout.addLayout(actions_layout)
        
        main_layout.addStretch()
        
        # Status label (replacing StatusBar since this is a widget now)
        self.status_label = QLabel("Ready to convert")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

    def _create_header_section(self) -> QWidget:
        """Create header with app title and info"""
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(5)
        
        # App title
        title = QLabel("💱 Currency Converter")
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Real-time exchange rates from OpenExchangeRates")
        subtitle.setObjectName("appSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        
        return header
    
    def _create_input_card(self) -> MaterialCard:
        """Create input section with Material Design"""
        card = MaterialCard()
        layout = QVBoxLayout(card)
        layout.setSpacing(20)
        
        # Amount section
        amount_label = QLabel("Amount")
        amount_label.setObjectName("fieldLabel")
        layout.addWidget(amount_label)
        
        self.amount_input = QLineEdit("1.00")
        self.amount_input.setObjectName("materialInput")
        self.amount_input.setPlaceholderText("Enter amount...")
        layout.addWidget(self.amount_input)
        
        # Currency selection section
        currency_container = QWidget()
        currency_layout = QHBoxLayout(currency_container)
        currency_layout.setSpacing(15)
        currency_layout.setContentsMargins(0, 0, 0, 0)
        
        # From currency
        from_container = QWidget()
        from_layout = QVBoxLayout(from_container)
        from_layout.setSpacing(8)
        from_layout.setContentsMargins(0, 0, 0, 0)
        
        from_label = QLabel("From")
        from_label.setObjectName("fieldLabel")
        from_layout.addWidget(from_label)
        
        self.from_combo = QComboBox()
        self.from_combo.setObjectName("materialCombo")
        self.from_combo.setEditable(True)
        self.from_combo.setPlaceholderText("Select currency...")
        from_layout.addWidget(self.from_combo)
        
        currency_layout.addWidget(from_container, 1)
        
        # Swap button in the middle
        swap_container = QWidget()
        swap_layout = QVBoxLayout(swap_container)
        swap_layout.setContentsMargins(0, 0, 0, 0)
        swap_layout.addStretch()
        
        self.swap_btn = QPushButton("⇄")
        self.swap_btn.setObjectName("swapButton")
        self.swap_btn.setFixedSize(56, 56)
        self.swap_btn.setToolTip("Swap currencies")
        swap_layout.addWidget(self.swap_btn)
        
        currency_layout.addWidget(swap_container, 0)
        
        # To currency
        to_container = QWidget()
        to_layout = QVBoxLayout(to_container)
        to_layout.setSpacing(8)
        to_layout.setContentsMargins(0, 0, 0, 0)
        
        to_label = QLabel("To")
        to_label.setObjectName("fieldLabel")
        to_layout.addWidget(to_label)
        
        self.to_combo = QComboBox()
        self.to_combo.setObjectName("materialCombo")
        self.to_combo.setEditable(True)
        self.to_combo.setPlaceholderText("Select currency...")
        to_layout.addWidget(self.to_combo)
        
        currency_layout.addWidget(to_container, 1)
        
        layout.addWidget(currency_container)
        
        # Convert button
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.setObjectName("primaryButton")
        self.convert_btn.setMinimumHeight(50)
        layout.addWidget(self.convert_btn)
        
        return card
    
    def _create_result_card(self) -> MaterialCard:
        """Create result display card"""
        card = MaterialCard()
        card.setObjectName("resultCard")
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        # Result header
        result_header = QLabel("Conversion Result")
        result_header.setObjectName("cardTitle")
        layout.addWidget(result_header)
        
        # From amount display
        self.from_amount_label = QLabel("--")
        self.from_amount_label.setObjectName("fromAmount")
        self.from_amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.from_amount_label)
        
        # Arrow separator
        arrow_label = QLabel("↓")
        arrow_label.setObjectName("arrowSeparator")
        arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(arrow_label)
        
        # To amount display
        self.to_amount_label = QLabel("--")
        self.to_amount_label.setObjectName("toAmount")
        self.to_amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.to_amount_label)
        
        # Additional info
        self.result_info_label = QLabel("Enter amount and currencies to convert")
        self.result_info_label.setObjectName("resultInfo")
        self.result_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_info_label.setWordWrap(True)
        layout.addWidget(self.result_info_label)
        
        return card
    
    def _create_action_buttons(self) -> QHBoxLayout:
        """Create action buttons layout"""
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # Refresh button
        self.refresh_btn = QPushButton("↻ Refresh Rates")
        self.refresh_btn.setObjectName("secondaryButton")
        self.refresh_btn.setMinimumHeight(45)
        layout.addWidget(self.refresh_btn)
        
        # Clear button
        self.clear_btn = QPushButton("✕ Clear")
        self.clear_btn.setObjectName("secondaryButton")
        self.clear_btn.setMinimumHeight(45)
        layout.addWidget(self.clear_btn)
        
        return layout
    
    def _connect_signals(self):
        """Connect UI signals to handlers"""
        self.convert_btn.clicked.connect(self._perform_conversion)
        self.refresh_btn.clicked.connect(self._refresh_rates)
        self.clear_btn.clicked.connect(self._clear_fields)
        self.swap_btn.clicked.connect(self._swap_currencies)
        
        # Auto-convert when currency selection changes
        self.from_combo.currentTextChanged.connect(self._on_currency_changed)
        self.to_combo.currentTextChanged.connect(self._on_currency_changed)
        
        # Enter key support
        self.amount_input.returnPressed.connect(self._perform_conversion)
    
    def _load_data(self):
        """Load initial data"""
        self._update_status("⟳ Initializing application...", "info")
        success, message = self._controller.initialize()
        
        if not success:
            self._update_status(f"✗ Initialization failed: {message}", "error")
            return
        
        # Get available currencies
        currencies = self._controller.get_available_currencies()
        
        if not currencies:
            self._update_status("✗ No currencies loaded", "error")
            return
        
        # Populate combo boxes
        self.from_combo.clear()
        self.to_combo.clear()
        
        for code, name in currencies:
            display_text = f"{self._get_flag(code)} {code} - {name}"
            self.from_combo.addItem(display_text, code)
            self.to_combo.addItem(display_text, code)
        
        # Setup autocomplete
        currency_list = [f"{self._get_flag(code)} {code} - {name}" 
                        for code, name in currencies]
        
        from_completer = QCompleter(currency_list, self)
        from_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.from_combo.setCompleter(from_completer)
        
        to_completer = QCompleter(currency_list, self)
        to_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.to_combo.setCompleter(to_completer)
        
        # Set defaults
        default_from, default_to = self._controller.get_default_currencies()
        self._set_currency_selection(self.from_combo, default_from)
        self._set_currency_selection(self.to_combo, default_to)
        
        self._update_status(f"✓ Ready • {len(currencies)} currencies loaded", "success")
    
    def _set_currency_selection(self, combo: QComboBox, code: str):
        """Set currency selection by code"""
        for i in range(combo.count()):
            if combo.itemData(i) == code:
                combo.setCurrentIndex(i)
                break
    
    def _get_selected_currency(self, combo: QComboBox) -> str:
        """Get selected currency code from combo box"""
        return combo.currentData() or ""
    
    def _get_flag(self, currency_code: str) -> str:
        """Get flag emoji for currency code"""
        flags = {
            'USD': '🇺🇸', 'EUR': '🇪🇺', 'GBP': '🇬', 'JPY': '🇯🇵',
            'AUD': '🇦🇺', 'CAD': '🇨🇦', 'CHF': '🇨🇭', 'CNY': '🇨🇳',
            'SEK': '🇸🇪', 'NZD': '🇳🇿', 'MXN': '🇲🇽', 'SGD': '🇸🇬',
            'HKD': '🇭🇰', 'NOK': '🇳🇴', 'KRW': '🇰🇷', 'TRY': '🇹🇷',
            'RUB': '🇷🇺', 'INR': '🇮🇳', 'BRL': '🇧🇷', 'ZAR': '🇿🇦',
            'IDR': '🇮🇩', 'MYR': '🇲🇾', 'PHP': '🇵🇭', 'THB': '🇹🇭',
            'DKK': '🇰', 'PLN': '🇵🇱', 'TWD': '🇹🇼', 'ARS': '🇦🇷',
            'CLP': '🇨🇱', 'COP': '🇨🇴', 'PEN': '🇵🇪', 'CZK': '🇨🇿',
            'HUF': '🇭🇺', 'ILS': '🇮🇱', 'AED': '🇦🇪', 'SAR': '🇸🇦',
            'EGP': '🇪🇬', 'VND': '🇻🇳', 'PKR': '🇵🇰', 'BDT': '🇧🇩',
            'NGN': '🇳🇬', 'UAH': '🇺🇦', 'RON': '🇷🇴', 'BGN': '🇧🇬',
        }
        return flags.get(currency_code, '💱')
    
    def _perform_conversion(self):
        """Handle currency conversion"""
        from_code = self._get_selected_currency(self.from_combo)
        to_code = self._get_selected_currency(self.to_combo)
        amount_str = self.amount_input.text().strip()
        
        if not all([from_code, to_code, amount_str]):
            self._update_status("ℹ Please fill in all fields", "warning")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                self._update_status("✗ Amount must be positive", "error")
                return
        except ValueError:
            self._update_status("✗ Invalid amount format", "error")
            return
        
        self._update_status("⟳ Converting...", "info")
        
        success, result, message = self._controller.convert(from_code, to_code, amount)
        
        if not success:
            self._update_status(f"✗ Conversion failed: {message}", "error")
            self.result_info_label.setText(f"Error: {message}")
            return
        
        # Display results with flags
        from_flag = self._get_flag(from_code)
        to_flag = self._get_flag(to_code)
        
        self.from_amount_label.setText(f"{from_flag} {amount:,.2f} {from_code}")
        self.to_amount_label.setText(f"{to_flag} {result:,.2f} {to_code}")
        
        # Calculate and display rate
        rate = result / amount if amount > 0 else 0
        self.rate_info_label.setText(
            f"Exchange Rate: 1 {from_code} = {rate:.6f} {to_code}"
        )
        
        # Additional info
        self.result_info_label.setText(message)
        
        self._update_status(f"✓ Conversion completed successfully", "success")
    
    def _refresh_rates(self):
        """Refresh exchange rates"""
        self._update_status("⟳ Refreshing exchange rates...", "info")
        self.refresh_btn.setEnabled(False)
        
        success, message = self._controller.refresh_rates()
        
        if success:
            self._update_status(f"✓ {message}", "success")
            # Re-perform conversion if we have values
            if self.from_amount_label.text() != "--":
                QTimer.singleShot(500, self._perform_conversion)
        else:
            self._update_status(f"✗ {message}", "error")
        
        self.refresh_btn.setEnabled(True)
    
    def _clear_fields(self):
        """Clear all input and result fields"""
        self.amount_input.setText("1.00")
        self.from_amount_label.setText("--")
        self.to_amount_label.setText("--")
        self.rate_info_label.setText("")
        self.result_info_label.setText("Enter amount and currencies to convert")
        
        # Reset to defaults
        default_from, default_to = self._controller.get_default_currencies()
        self._set_currency_selection(self.from_combo, default_from)
        self._set_currency_selection(self.to_combo, default_to)
        
        self._update_status("ℹ Fields cleared", "info")
        self.amount_input.setFocus()
    
    def _swap_currencies(self):
        """Swap from and to currencies"""
        from_index = self.from_combo.currentIndex()
        to_index = self.to_combo.currentIndex()
        
        self.from_combo.setCurrentIndex(to_index)
        self.to_combo.setCurrentIndex(from_index)
        
        self._update_status("⇄ Currencies swapped", "info")
        
        # Auto-convert after swap if we have an amount
        if self.amount_input.text().strip():
            QTimer.singleShot(300, self._perform_conversion)
    
    def _on_currency_changed(self):
        """Handle currency selection change - auto convert if data exists"""
        # Only auto-convert if we have both currencies selected and an amount
        from_code = self._get_selected_currency(self.from_combo)
        to_code = self._get_selected_currency(self.to_combo)
        amount_str = self.amount_input.text().strip()
        
        if all([from_code, to_code, amount_str]):
            try:
                amount = float(amount_str)
                if amount > 0:
                    # Small delay for better UX
                    QTimer.singleShot(300, self._perform_conversion)
            except ValueError:
                pass
    
    def _update_status(self, message: str, status_type: str = "info"):
        """Update status label with styled message"""
        # In the main window this was a status bar, here we just update the label
        self.status_label.setText(message)
        
        colors = {
            "info": "#2196F3",
            "success": "#4CAF50",
            "error": "#F44336",
            "warning": "#FF9800"
        }
        
        color = colors.get(status_type, "#2196F3")
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
