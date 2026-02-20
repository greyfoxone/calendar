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


@class_debug_log
class ClockCalendarDesklet(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_clock()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(60000)  # Update every minute

    def init_ui(self):
        self.create_ui()
        self.layout_ui()
        self.adjustSize()

    def create_ui(self):
        self.time_label = QLabel()
        self.time_label.setStyleSheet(
            """
            font-size: 80px;
            font-weight: bold;
        """
        )

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

        self.calendar_table = CalendarTableWidget()

    def layout_ui(self):
        layout = QVBoxLayout()

        clock_layout = QHBoxLayout()
        date_layout = QVBoxLayout()

        date_layout.addWidget(self.date_label)
        date_layout.addWidget(self.weekday_label)

        clock_layout.addWidget(self.time_label)
        clock_layout.addLayout(date_layout)
        layout.addLayout(clock_layout)

        layout.addWidget(self.calendar_table)
        self.setLayout(layout)

    def update_clock(self):
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M"))
        self.date_label.setText(now.strftime("%Y-%m-%d"))
        self.weekday_label.setText(now.strftime("%A"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    desklet = ClockCalendarDesklet()
    desklet.show()
    sys.exit(app.exec())