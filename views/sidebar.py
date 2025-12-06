"""
Sidebar navigation widget
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QFrame)
from PyQt6.QtCore import pyqtSignal, Qt

class SidebarButton(QPushButton):
    """Custom styled button for sidebar"""
    def __init__(self, text, icon_text, parent=None):
        super().__init__(parent)
        self.setText(f" {icon_text}  {text}")
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setMinimumHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                color: #5f6368;
            }
            QPushButton:hover {
                background-color: #f1f3f4;
                color: #202124;
            }
            QPushButton:checked {
                background-color: #e8f0fe;
                color: #1967d2;
                font-weight: bold;
            }
        """)

class Sidebar(QFrame):
    """Sidebar navigation panel"""
    
    # Signal emitted when a navigation item is selected (returns index)
    page_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFixedWidth(250)
        self.setStyleSheet("background-color: #ffffff; border-right: 1px solid #dadce0;")
        
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(5)
        
        # App Logo/Title Area
        title_label = QLabel("Currency\nConverter")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #202124; padding: 10px;")
        layout.addWidget(title_label)
        
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
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: #9aa0a6; font-size: 12px;")
        layout.addWidget(version_label)
        
        # Set default selection
        self.btn_converter.setChecked(True)
