import sys
from datetime import datetime

from lib.calendar import MonthTableWidget
from lib.event_handler import EventHandler
from lib.header import HeaderWidget
from lib.indent_logger import class_debug_log
from lib.stopwatch import StopwatchWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtWidgets import QMenu
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


@class_debug_log
class ClockCalendarDesklet(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.event_handler = EventHandler()

    def init_ui(self):
        self.create_ui()
        self.layout_ui()
        self.connect_signals()
        self.header_widget.customContextMenuRequested.connect(self.show_context_menu)
        today = datetime.now()
        self.calendar_table.mark_day(today.day, QColor(255, 0, 0))
        self.update_app()
    
    def update_app(self):
        self.adjustSize()
        self.place_app()
        
    def place_app(self):
        app = QApplication.instance() 
        screen = app.screens()[1]  # Secondary screen
        geom = screen.geometry()
        self.move(geom.right() - self.width(), geom.top())

    def create_ui(self):
        self.header_widget = HeaderWidget()
        self.calendar_table = MonthTableWidget(datetime.now().year, datetime.now().month)
        self.calendar_table.setVisible(False)

    def layout_ui(self):
        self.countdown_area = QVBoxLayout()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.calendar_table)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def connect_signals(self):
        self.header_widget.clicked.connect(self.toggle_calendar)

    def toggle_calendar(self, status):
        self.calendar_table.setVisible(not self.calendar_table.isVisible())
        self.update_app()

    def show_context_menu(self, pos):
        menu = QMenu(self)
        sw_menu = menu.addMenu("Stopwatch")
        for m in [1, 3, 5, 10, 15, 30, 60]:
            act = sw_menu.addAction(f"{m} min")
            act.triggered.connect(lambda _, mins=m: self.start_stopwatch(mins))

        load_action = menu.addAction("Load Events")
        load_action.triggered.connect(self.event_handler.load_events_dialog)

        save_action = menu.addAction("Save Events")
        save_action.triggered.connect(self.event_handler.save_events_dialog)
        self.event_handler.event_loaded.connect(self.mark_events)
        menu.exec(self.mapToGlobal(pos))

    def start_stopwatch(self, mins):
        text, ok = QInputDialog.getText(self, "Label", "Enter label (optional):")
        if not ok:
            return
        sw = StopwatchWidget(mins, text.strip())
        self.layout.addWidget(sw)
        sw.show()
        sw.destroyed.connect(self.adjustSize)

    def mark_events(self):
        today = datetime.now()
        current_month = today.month
        current_year = today.year

        for event in self.event_handler.events:
            start_date = event.start
            if start_date.month == current_month and start_date.year == current_year:
                self.calendar_table.mark_day(start_date.day, QColor(0, 255, 0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    desklet = ClockCalendarDesklet()
    desklet.show()
    sys.exit(app.exec())