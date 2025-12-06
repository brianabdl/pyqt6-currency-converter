"""
Sidebar navigation widget
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QFrame)
from PyQt6.QtCore import pyqtSignal, Qt
from .theme import ThemeColors

class SidebarButton(QPushButton):
    """Custom styled button for sidebar"""
    def __init__(self, text, icon_text, parent=None):
        super().__init__(parent)
        self.setText(f" {icon_text}  {text}")
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setMinimumHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        # Initial style will be set by update_theme

    def update_theme(self, theme: ThemeColors):
        """Update button styles based on theme"""
        self.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding-left: 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                color: {theme.text_secondary};
            }}
            QPushButton:hover {{
                background-color: {theme.hover};
                color: {theme.text_primary};
            }}
            QPushButton:checked {{
                background-color: {theme.selected_bg};
                color: {theme.selected_text};
                font-weight: bold;
            }}
        """)

class Sidebar(QFrame):
    """Sidebar navigation panel"""
    
    # Signal emitted when a navigation item is selected (returns index)
    page_changed = pyqtSignal(int)
    # Signal for theme toggle
    theme_toggled = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFixedWidth(250)
        
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(5)
        
        # App Logo/Title Area
        self.title_label = QLabel("Currency\nConverter")
        # Style will be set in update_theme
        layout.addWidget(self.title_label)
        
        layout.addSpacing(20)
        
        # Navigation Buttons
        self.btn_converter = SidebarButton("Converter", "💱")
        self.btn_history = SidebarButton("History", "🕒")
        self.btn_settings = SidebarButton("Settings", "⚙️")
        
        # Connect buttons
        self.btn_converter.clicked.connect(lambda: self.page_changed.emit(0))
        self.btn_history.clicked.connect(lambda: self.page_changed.emit(1))
        self.btn_settings.clicked.connect(lambda: self.page_changed.emit(2))
        
        layout.addWidget(self.btn_converter)
        layout.addWidget(self.btn_history)
        layout.addWidget(self.btn_settings)
        
        layout.addStretch()

        # Theme Toggle
        self.theme_btn = QPushButton("🌙 Dark Mode")
        self.theme_btn.setCheckable(True)
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self.theme_toggled.emit)
        self.theme_btn.setStyleSheet("border: none; text-align: left; padding: 10px;")
        layout.addWidget(self.theme_btn)
        
        # Version info
        self.version_label = QLabel("v1.0.0")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.version_label)
        
        # Set default selection
        self.btn_converter.setChecked(True)

    def update_theme(self, theme: ThemeColors):
        """Update sidebar styles based on theme"""
        self.setStyleSheet(f"background-color: {theme.surface}; border-right: 1px solid {theme.border};")
        
        self.title_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {theme.text_primary}; padding: 10px;")
        
        self.btn_converter.update_theme(theme)
        self.btn_history.update_theme(theme)
        self.btn_settings.update_theme(theme)
        
        # Update theme button
        self.theme_btn.setStyleSheet(f"color: {theme.text_secondary}; border: none; text-align: left; padding: 10px;")
        if self.theme_btn.isChecked():
            self.theme_btn.setText("☀️ Light Mode")
        else:
            self.theme_btn.setText("🌙 Dark Mode")

        self.version_label.setStyleSheet(f"color: {theme.text_secondary}; font-size: 12px;")
