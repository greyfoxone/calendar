from dataclasses import dataclass
from datetime import datetime

from icalendar import Calendar
from icalendar import Event as ICalEvent

from .event import Event


@dataclass
class Event:
    summary: str
    start: datetime
    end: datetime


class CalendarHandler:
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
            ical_event = ICalEvent()
            ical_event.add("summary", event.summary)
            ical_event.add("dtstart", event.start)
            ical_event.add("dtend", event.end)
            cal.add_component(ical_event)
        with open(file_path, "wb") as f:
            f.write(cal.to_ical())