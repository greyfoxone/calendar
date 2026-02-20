import sys
from datetime import datetime

from lib.calendar import MonthTableWidget
from lib.indent_logger import class_debug_log
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QSizePolicy
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
        layout.addWidget(self.date_label, 0)
        layout.addWidget(self.weekday_label, 0)
        layout.addStretch(1)
        self.setLayout(layout)

    def update(self):
        super().update()
        now = datetime.now()
        self.date_label.setText(now.strftime("%Y-%m-%d"))
        self.weekday_label.setText(now.strftime("%A"))


class TimeClock(QLabel):
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
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.update()

    def update(self):
        super().update()
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
        today = datetime.now()
        self.calendar_table.mark_day(today.day)
        self.adjustSize()

    def create_ui(self):
        self.time_label = TimeClock()
        self.current_day = CurrentDay()
        self.calendar_table = MonthTableWidget(datetime.now().year, datetime.now().month)

    def layout_ui(self):
        layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.time_label,0)
        header_layout.addWidget(self.current_day,0)
        header_layout.addStretch(1)
        layout.addLayout(header_layout)

        layout.addWidget(self.calendar_table)
        layout.addStretch(1)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    desklet = ClockCalendarDesklet()
    desklet.show()
    sys.exit(app.exec())