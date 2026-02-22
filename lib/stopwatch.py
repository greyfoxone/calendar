from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

class StopwatchWidget(QWidget):
    def __init__(self, minutes: int, label: str = ""):
        super().__init__()
        self.remaining = minutes * 60
        self.finished = False
        self.init_ui(label)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def init_ui(self, label: str):
        layout = QVBoxLayout()
        if label:
            title = QLabel(label)
            title.setStyleSheet("font-size: 20px;")
            layout.addWidget(title)
        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 80px; font-weight: bold;")
        layout.addWidget(self.time_label)
        self.setLayout(layout)
        self.update_label()

    def update_time(self):
        if self.remaining > 0:
            self.remaining -= 1
            self.update_label()
        else:
            self.timer.stop()
            self.finished = True
            self.activateWindow()
            self.raise_()
            self.time_label.setText("00:00")

    def update_label(self):
        mins = self.remaining // 60
        secs = self.remaining % 60
        self.time_label.setText(f"{mins:02d}:{secs:02d}")

    def mousePressEvent(self, event):
        if self.finished:
            self.close()
        super().mousePressEvent(event)