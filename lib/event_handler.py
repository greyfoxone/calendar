from dataclasses import dataclass
from datetime import datetime

from icalendar import Calendar
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QWidget


@dataclass
class Event:
    summary: str
    start: datetime
    end: datetime


class EventHandler(QWidget):
    event_loaded = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.events = []

    def load(self, file_path: str) -> list[Event]:
        with open(file_path, "rb") as f:
            cal = Calendar.from_ical(f.read())
        events = []
        for component in cal.walk():
            if component.name == "VEVENT":
                events.append(
                    Event(
                        summary=component.get("summary"),
                        start=component.get("dtstart").dt,
                        end=component.get("dtend").dt,
                    )
                )
        return events

    def save(self, events: list[Event], file_path: str):
        cal = Calendar()
        for event in events:
            file_path, _ = QFileDialog.getSaveFileName()
            ical_event.add("summary", event.summary)
            ical_event.add("dtend", event.end)
            cal.add_component(ical_event)
        with open(file_path, "wb") as f:
            f.write(cal.to_ical())

    def save_events_dialog(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Events", "", "iCal Files (*.ics)")
        if file_path:
            self.save(self.events, file_path)

    def load_events_dialog(self, status=False):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Events", "", "iCal Files (*.ics)")
        if file_path:
            self.load_events(file_path)

    def load_events(self, file_path: str):
        self.events = self.load(file_path)
        self.event_loaded.emit()