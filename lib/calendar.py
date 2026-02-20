from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtWidgets import QTableWidgetItem


class CalendarTableWidget(QTableWidget):
    def __init__(self):
        super().__init__(6, 7)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setStyleSheet(
            """
            border: none;
            font-size: 12px;
            background-color: rgba(30, 30, 30, 0.8);
            color: #f0f0f0;
            border-radius: 10px;
            padding: 15px;
        """
        )
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.update_calendar()

    def update_calendar(self):
        today = datetime.now()
        year, month = today.year, today.month

        self.clear()

        weekdays = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"]
        for i, day in enumerate(weekdays):
            item = QTableWidgetItem(day)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setHorizontalHeaderItem(i, item)

        first_day = datetime(year, month, 1)
        start_day = (first_day.weekday() + 1) % 7
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
                self.setItem(week, dow, item)

                if day == today.day:
                    item.setBackground(QColor("#007bff"))
                    item.setForeground(QColor("white"))

                day += 1