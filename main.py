import sys
from datetime import datetime

from lib.calendar import MonthTableWidget
from lib.header import HeaderWidget
from lib.indent_logger import class_debug_log
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


@class_debug_log
class ClockCalendarDesklet(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self._calendar_visible = True

    def init_ui(self):
        self.create_ui()
        self.layout_ui()
        self.connect_signals()
        today = datetime.now()
        self.calendar_table.mark_day(today.day)
        

        self.adjustSize()

    def create_ui(self):
        self.header_widget = HeaderWidget()
        self.calendar_table = MonthTableWidget(datetime.now().year, datetime.now().month)

    def layout_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.header_widget)
        layout.addWidget(self.calendar_table)
        layout.addStretch(1)
        self.setLayout(layout)
        
    def connect_signals(self):
        self.header_widget.clicked.connect(self.toggle_calendar)
        
    def toggle_calendar(self,status):
        self._calendar_visible = not self._calendar_visible
        self.calendar_table.setVisible(self._calendar_visible)
        self.adjustSize()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    desklet = ClockCalendarDesklet()
    desklet.show()
    sys.exit(app.exec())
    