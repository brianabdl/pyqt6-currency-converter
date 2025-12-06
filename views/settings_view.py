"""
Settings view for application configuration
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                              QGroupBox, QFormLayout, QPushButton)
from PyQt6.QtCore import Qt
from controllers import CurrencyController
from .theme import ThemeColors

class SettingsView(QWidget):
    """View for configuring application settings"""
    
    def __init__(self, controller: CurrencyController):
        super().__init__()
        self._controller = controller
        self._current_theme = None
        self._setup_ui()
        self._load_settings()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        title = QLabel("Settings")
        title.setObjectName("viewTitle")
        layout.addWidget(title)
        
        # Default Currencies Group
        self.defaults_group = QGroupBox("Default Currencies")
        self.defaults_group.setObjectName("settingsGroup")
        defaults_layout = QFormLayout(self.defaults_group)
        defaults_layout.setSpacing(15)
        
        self.default_from = QComboBox()
        self.default_from.setObjectName("settingsCombo")
        defaults_layout.addRow("Default From:", self.default_from)
        
        self.default_to = QComboBox()
        self.default_to.setObjectName("settingsCombo")
        defaults_layout.addRow("Default To:", self.default_to)
        
        layout.addWidget(self.defaults_group)
        
        # Save Button
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.setMinimumHeight(45)
        self.save_btn.clicked.connect(self._save_settings)
        layout.addWidget(self.save_btn)
        
        # Status Label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
    def _load_settings(self):
        """Load current settings into UI"""
        # Populate currency combos
        currencies = self._controller.get_available_currencies()
        self.default_from.clear()
        self.default_to.clear()
        
        for code, name in currencies:
            display = f"{code} - {name}"
            self.default_from.addItem(display, code)
            self.default_to.addItem(display, code)
            
        # Set current defaults
        from_code, to_code = self._controller.get_default_currencies()
        self._set_combo_value(self.default_from, from_code)
        self._set_combo_value(self.default_to, to_code)
        
    def _set_combo_value(self, combo: QComboBox, value: str):
        """Set combo box selection by data value"""
        for i in range(combo.count()):
            if combo.itemData(i) == value:
                combo.setCurrentIndex(i)
                break
                
    def _save_settings(self):
        """Save settings via controller"""
        from_code = self.default_from.currentData()
        to_code = self.default_to.currentData()
        
        if from_code and to_code:
            self._controller.set_default_currencies(from_code, to_code)
            self.status_label.setText("✓ Settings saved successfully")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        else:
            self.status_label.setText("✗ Error saving settings")
            self.status_label.setStyleSheet("color: #F44336; font-weight: bold;")
            
    def update_theme(self, theme: ThemeColors):
        """Update view styles based on theme"""
        self._current_theme = theme
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.background};
                color: {theme.text_primary};
            }}
            QLabel#viewTitle {{
                font-size: 24px;
                font-weight: bold;
                color: {theme.text_primary};
            }}
            QGroupBox#settingsGroup {{
                border: 1px solid {theme.border};
                border-radius: 8px;
                margin-top: 1em;
                padding-top: 10px;
                font-weight: bold;
                color: {theme.text_primary};
            }}
            QGroupBox#settingsGroup::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }}
            QComboBox#settingsCombo {{
                padding: 8px;
                border: 1px solid {theme.input_border};
                border-radius: 4px;
                background-color: {theme.input_bg};
                color: {theme.text_primary};
            }}
            QPushButton#primaryButton {{
                background-color: {theme.primary};
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton#primaryButton:hover {{
                background-color: {theme.selected_text};
            }}
        """)
