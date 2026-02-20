import sys
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class ClockCalendarDesklet(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_clock()
        self.update_calendar()
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

        self.calendar_table = QTableWidget(6, 7)
        self.calendar_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.calendar_table.setStyleSheet(
            """
            border: none;
            font-size: 12px;
            background-color: rgba(30, 30, 30, 0.8);
            color: #f0f0f0;
            border-radius: 10px;
            padding: 15px;
        """
        )

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

    def update_calendar(self):
        today = datetime.now()

    def update_clock(self):
        now = datetime.now()
        self.time_label.setText(now.strftime("%H:%M"))
        self.date_label.setText(now.strftime("%Y-%m-%d"))
        self.weekday_label.setText(now.strftime("%A"))

    def update_calendar(self):
        today = datetime.now()
        year, month = today.year, today.month

        # Clear table
        self.calendar_table.clear()

        # Headers
        weekdays = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"]
        for i, day in enumerate(weekdays):
            item = QTableWidgetItem(day)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.calendar_table.setHorizontalHeaderItem(i, item)

        # Fill calendar
        first_day = datetime(year, month, 1)
        start_day = (first_day.weekday() + 1) % 7  # Monday is 0
        days_in_month = (datetime(year, month + 1, 1) - datetime(year, month, 1)).days

        day = 1
        for week in range(6):
            for dow in range(7):
                if week == 0 and dow < start_day:
                    continue
                if day > days_in_month:
                    break

                item = QTableWidgetItem(str(day))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.calendar_table.setItem(week, dow, item)

                # Highlight today
                if day == today.day:
                    item.setBackground(QColor("#007bff"))
                    item.setForeground(QColor("white"))

                day += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    desklet = ClockCalendarDesklet()
    desklet.show()
    sys.exit(app.exec())