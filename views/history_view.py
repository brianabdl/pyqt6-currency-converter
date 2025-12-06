"""
History view for displaying transaction logs
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, 
                              QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt
from controllers import CurrencyController
from .theme import ThemeColors

class HistoryView(QWidget):
    """View for displaying transaction history"""
    
    def __init__(self, controller: CurrencyController):
        super().__init__()
        self._controller = controller
        self._current_theme = None
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Transaction History")
        title.setObjectName("viewTitle")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.refresh_btn = QPushButton("↻ Refresh")
        self.refresh_btn.setObjectName("actionButton")
        self.refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(self.refresh_btn)
        
        self.clear_btn = QPushButton("🗑️ Clear History")
        self.clear_btn.setObjectName("dangerButton")
        self.clear_btn.clicked.connect(self._clear_history)
        header_layout.addWidget(self.clear_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "From", "To", "Rate", "Result"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
        
        # Initial load
        self.refresh_data()
        
    def refresh_data(self):
        """Reload history data from controller"""
        transactions = self._controller.get_history()
        self.table.setRowCount(len(transactions))
        
        for i, t in enumerate(transactions):
            # Date
            date_item = QTableWidgetItem(t.timestamp.strftime("%Y-%m-%d %H:%M"))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, date_item)
            
            # From
            from_item = QTableWidgetItem(f"{t.amount:,.2f} {t.from_currency}")
            from_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 1, from_item)
            
            # To
            to_item = QTableWidgetItem(f"{t.result:,.2f} {t.to_currency}")
            to_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 2, to_item)
            
            # Rate
            rate_item = QTableWidgetItem(f"{t.rate:.4f}")
            rate_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 3, rate_item)
            
            # Result (Summary)
            summary = f"{t.from_currency} → {t.to_currency}"
            summary_item = QTableWidgetItem(summary)
            summary_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 4, summary_item)
            
    def _clear_history(self):
        """Clear all history"""
        self._controller.clear_history()
        self.refresh_data()
        
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
            QPushButton#actionButton {{
                background-color: {theme.surface};
                color: {theme.text_primary};
                border: 1px solid {theme.border};
                padding: 8px 16px;
                border-radius: 4px;
            }}
            QPushButton#actionButton:hover {{
                background-color: {theme.hover};
            }}
            QPushButton#dangerButton {{
                background-color: {theme.surface};
                color: {theme.error};
                border: 1px solid {theme.error};
                padding: 8px 16px;
                border-radius: 4px;
            }}
            QPushButton#dangerButton:hover {{
                background-color: {theme.error};
                color: white;
            }}
            QTableWidget {{
                background-color: {theme.surface};
                gridline-color: {theme.border};
                border: 1px solid {theme.border};
                border-radius: 8px;
            }}
            QHeaderView::section {{
                background-color: {theme.background};
                color: {theme.text_secondary};
                padding: 8px;
                border: none;
                font-weight: bold;
            }}
            QTableWidget::item {{
                padding: 5px;
                border-bottom: 1px solid {theme.border};
            }}
            QTableWidget::item:selected {{
                background-color: {theme.selected_bg};
                color: {theme.selected_text};
            }}
        """)
