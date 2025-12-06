"""
Main view for the Currency Converter application  
Material Design inspired UI with enhanced UX and Navigation
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QLabel, QApplication)
from PyQt6.QtCore import Qt
from config import Config
from controllers import CurrencyController
from .sidebar import Sidebar
from .converter_view import ConverterView
from .history_view import HistoryView
from .settings_view import SettingsView
from .theme import LIGHT_THEME, DARK_THEME

class MainWindow(QMainWindow):
    """Main application window with Sidebar Navigation"""
    
    def __init__(self, controller: CurrencyController, settings_repo):
        super().__init__()
        self._controller = controller
        self.settings_repo = settings_repo
        self._setup_ui()
        self._init_theme()
    
    def _setup_ui(self):
        """Setup the main window layout with sidebar and content area"""
        self.setWindowTitle(Config.APP_NAME)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout (Horizontal: Sidebar | Content)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 1. Sidebar
        self.sidebar = Sidebar()
        self.sidebar.theme_toggled.connect(self._on_theme_toggled)
        main_layout.addWidget(self.sidebar)
        
        # 2. Content Area (Stacked Widget)
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # -- Page 1: Converter View --
        self.converter_view = ConverterView(self._controller)
        self.content_stack.addWidget(self.converter_view)
        
        # -- Page 2: History View --
        self.history_view = HistoryView(self._controller)
        self.content_stack.addWidget(self.history_view)
        
        # -- Page 3: Settings View --
        self.settings_view = SettingsView(self._controller)
        self.content_stack.addWidget(self.settings_view)
        
        # Connect Sidebar to Stack
        self.sidebar.page_changed.connect(self._on_page_changed)

    def _on_page_changed(self, index: int):
        """Handle page change"""
        self.content_stack.setCurrentIndex(index)
        # Refresh history when switching to it
        if index == 1:
            self.history_view.refresh_data()

    def _create_placeholder_view(self, title: str, subtitle: str) -> QWidget:
        """Create a simple placeholder view for unimplemented pages"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        label = QLabel(f"{title}\n\n{subtitle}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Style will be set by theme
        
        layout.addWidget(label)
        return widget

    def _init_theme(self):
        """Initialize theme based on system settings or default"""
        # Simple detection: check if window text is light (indicating dark background)
        app = QApplication.instance()
        # respect settings theme if available
        if self.settings_repo.get("theme") == "dark":
            is_dark = True
        elif self.settings_repo.get("theme") == "light":
            is_dark = False
        elif app:
            palette = app.palette()
            text_color = palette.color(palette.ColorGroup.Active, palette.ColorRole.WindowText)
            # If text is bright (> 128), it's likely dark mode
            is_dark = text_color.lightness() > 128
        else:
            is_dark = False
        
        if is_dark:
            self.sidebar.theme_btn.setChecked(True)
            self._apply_theme(DARK_THEME)
        else:
            self.sidebar.theme_btn.setChecked(False)
            self._apply_theme(LIGHT_THEME)

    def _on_theme_toggled(self, checked: bool):
        """Handle theme toggle"""
        theme = DARK_THEME if checked else LIGHT_THEME
        self.settings_repo.set("theme", "dark" if checked else "light")
        self._apply_theme(theme)

    def _apply_theme(self, theme):
        """Apply theme to all components"""
        self.setStyleSheet(f"background-color: {theme.background};")
        self.content_stack.setStyleSheet(f"background-color: {theme.background};")
        
        self.sidebar.update_theme(theme)
        self.converter_view.update_theme(theme)
        self.history_view.update_theme(theme)
        self.settings_view.update_theme(theme)
        
        # Update placeholders
        for i in range(self.content_stack.count()):
            widget = self.content_stack.widget(i)
            if widget not in [self.converter_view, self.history_view, self.settings_view]:
                # It's a placeholder
                widget.setStyleSheet(f"background-color: {theme.background};")
                # Find label
                label = widget.findChild(QLabel)
                if label:
                    label.setStyleSheet(f"font-size: 18px; color: {theme.text_secondary};")

