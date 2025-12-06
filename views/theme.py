"""
Theme management for the application
"""
from dataclasses import dataclass
from PyQt6.QtGui import QColor

@dataclass
class ThemeColors:
    background: str
    surface: str
    text_primary: str
    text_secondary: str
    border: str
    hover: str
    selected_bg: str
    selected_text: str
    primary: str
    secondary_btn_bg: str
    secondary_btn_text: str
    input_bg: str
    input_border: str
    success: str
    error: str
    warning: str
    info: str

LIGHT_THEME = ThemeColors(
    background="#f8f9fa",
    surface="#ffffff",
    text_primary="#202124",
    text_secondary="#5f6368",
    border="#dadce0",
    hover="#f1f3f4",
    selected_bg="#e8f0fe",
    selected_text="#1967d2",
    primary="#1967d2",
    secondary_btn_bg="#f1f3f4",
    secondary_btn_text="#3c4043",
    input_bg="#ffffff",
    input_border="#dadce0",
    success="#4CAF50",
    error="#F44336",
    warning="#FF9800",
    info="#2196F3"
)

DARK_THEME = ThemeColors(
    background="#202124",
    surface="#2d2e31",
    text_primary="#e8eaed",
    text_secondary="#9aa0a6",
    border="#3c4043",
    hover="#3c4043",
    selected_bg="#3c4043", # Darker selection
    selected_text="#8ab4f8",
    primary="#8ab4f8",
    secondary_btn_bg="#3c4043",
    secondary_btn_text="#e8eaed",
    input_bg="#202124",
    input_border="#5f6368",
    success="#81c995",
    error="#f28b82",
    warning="#fdd663",
    info="#8ab4f8"
)
