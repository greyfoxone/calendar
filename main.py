import sys
from datetime import datetime

from lib.calendar import CalendarTableWidget
from lib.indent_logger import class_debug_log
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class CurrentDay(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(60000)
        self.update()

    def init_ui(self):
        layout = QVBoxLayout()
        self.date_label = QLabel()
        self.date_label.setStyleSheet(
            """
            margin-top: 11px;
            font-size: 60%;
        """
        )
        self.weekday_label = QLabel()
        self.weekday_label.setStyleSheet(
            """
            color: #cc6666;
            font-size: 40%;
        """
        )
        layout.addWidget(self.date_label)
        layout.addWidget(self.weekday_label)
        self.setLayout(layout)

    def update(self):
        now = datetime.now()
        self.date_label.setText(now.strftime("%Y-%m-%d"))
        self.weekday_label.setText(now.strftime("%A"))


class TimeLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            font-size: 80px;
            font-weight: bold;
        """
        )
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(60000)
        self.update()

    def update(self):
        now = datetime.now()
        self.setText(now.strftime("%H:%M"))


@class_debug_log
class ClockCalendarDesklet(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.create_ui()
        self.layout_ui()
        self.adjustSize()

    def create_ui(self):
        self.time_label = TimeLabel()
        self.current_day = CurrentDay()
        self.calendar_table = CalendarTableWidget()

    def layout_ui(self):
        layout = QVBoxLayout()

        clock_layout = QHBoxLayout()
        clock_layout.addWidget(self.time_label)
        clock_layout.addWidget(self.current_day)
        layout.addLayout(clock_layout)

        layout.addWidget(self.calendar_table)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    desklet = ClockCalendarDesklet()
    desklet.show()
    sys.exit(app.exec())