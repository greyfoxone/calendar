from datetime import datetime

from lib.indent_logger import class_debug_log
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


@class_debug_log
class StopwatchWidget(QWidget):
    STOPPED = 0
    RUNNING = 1
    FINISHED = 2

    def __init__(self, minutes: int, label: str = ""):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.start_time = datetime.now().strftime("%H:%M")
        self.state = StopwatchWidget.RUNNING
        self.remaining = minutes * 60
        self.init_ui(label)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    #        self.setStyleSheet("border: 1px solid;")

    def init_ui(self, label: str):
        self.create_ui(label)
        self.layout_ui()

    def create_ui(self, label: str):
        if label:
            title = QLabel(label)
            title.setStyleSheet("font-size: 20px")
            self.title_label = title

        self.time_label = QLabel()
        self.time_label.setContentsMargins(0, 0, 0, 0)
        self.time_label.setStyleSheet(
            "font-size: 80px; font-weight: bold; background-color: transparent;"
        )

        self.start_time_label = QLabel()
        self.start_time_label.setStyleSheet("font-size: 16px; color: gray;")

        self.state_label = QLabel()
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state_label.setStyleSheet(
            """
            font-size: 40px;
            font-weight: bold;
            color: rgba(255,255,255,150);
            background-color: rgba(0,0,0,50);
            border-radius: 20px;
            padding: 15px;
            border: 1px solid #101010;
            """
        )

    def layout_ui(self):
        overlay_layout = QVBoxLayout(self.time_label)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overlay_layout.addWidget(self.state_label)

        layout = QVBoxLayout()
        layout.addWidget(self.start_time_label)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.time_label)
        if hasattr(self, "title_label"):
            h_layout.addWidget(self.title_label)
        h_layout.addStretch(1)
        
        layout.addLayout(h_layout)
        self.setLayout(layout)
        self.update_label()
        self.update_state_label()

    def update_time(self):
        if self.remaining > 0:
            self.remaining -= 1
            self.update_label()
            return

        self.timer.stop()
        self.state = StopwatchWidget.FINISHED
        self.activateWindow()
        self.raise_()
        self.time_label.setText("00:00")
        self.update_state_label()

    def update_state_label(self):
        if self.state == StopwatchWidget.RUNNING:
            self.state_label.setText("⏸")
        elif self.state == StopwatchWidget.STOPPED:
            self.state_label.setText("▶")
        elif self.state == StopwatchWidget.FINISHED:
            self.state_label.setText("⏹")

    def update_label(self):
        mins = self.remaining // 60
        secs = self.remaining % 60
        self.time_label.setText(f"{mins:02d}:{secs:02d}")
        self.start_time_label.setText(f"Start: {self.start_time}")
        self.update_state_label()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton and self.state in [
            StopwatchWidget.FINISHED,
            StopwatchWidget.STOPPED,
        ]:
            self.setParent(None)
            self.deleteLater()
            return

        if event.button() == Qt.MouseButton.LeftButton:
            if self.state == StopwatchWidget.FINISHED:
                self.setParent(None)
                self.deleteLater()
                return
            elif self.state == StopwatchWidget.RUNNING:
                self.timer.stop()
                self.state = StopwatchWidget.STOPPED
            else:
                self.timer.start()
                self.state = StopwatchWidget.RUNNING
        self.update_state_label()
        super().mousePressEvent(event)