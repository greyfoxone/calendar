import calendar
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QAbstractScrollArea
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtWidgets import QTableWidgetItem


class MonthTableWidget(QTableWidget):
    def __init__(self, year: int, month: int):
        super().__init__(6, 7)
        self.year = year
        self.month = month
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.update_calendar(year, month)

    def mark_day(self, day: int, color: QColor):
        if not 1 <= day <= 31:
            return
        first_weekday = calendar.monthrange(self.year, self.month)[0]
        week = (first_weekday + day - 1) // 7 + 1
        dow = (first_weekday + day - 1) % 7
        if 0 <= week < 6 and 0 <= dow < 7:
            item = self.item(week, dow)
            if item:
                item.setBackground(color)

    def mark_events(self, events, color):
        today = datetime.now()
        current_month = today.month
        current_year = today.year

        for event in events:
            start_date = event.start
            if start_date.month == current_month and start_date.year == current_year:
                self.mark_day(start_date.day, color)

    def update_calendar(self, year: int, month: int):
        self.clear()
        self._setup_header()
        self._render_month_days(year, month)
        self.adjustSize()

    def _setup_header(self):
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(weekdays):
            item = QTableWidgetItem(day)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setHorizontalHeaderItem(i, item)

    def _render_month_days(self, year: int, month: int):
        _, days_in_month = calendar.monthrange(year, month)
        first_weekday = calendar.monthrange(year, month)[0]
        day = 1
        for week in range(6):
            for dow in range(7):
                if week == 0 and dow < first_weekday:
                    continue
                if day > days_in_month:
                    break
                item = QTableWidgetItem(str(day))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(week + 1, dow, item)
                day += 1