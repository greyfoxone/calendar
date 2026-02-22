from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class StopwatchWidget(QWidget):
    STOPPED = 0
    RUNNING = 1
    FINISHED = 2

    def __init__(self, minutes: int, label: str = ""):
        super().__init__()
        self.state = StopwatchWidget.RUNNING
        self.remaining = minutes * 60
        self.init_ui(label)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def init_ui(self, label: str):
        self.create_ui(label)
        self.layout_ui()

    def create_ui(self, label: str):
        if label:
            title = QLabel(label)
            title.setStyleSheet("font-size: 20px;")
            self.title_label = title

        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 80px; font-weight: bold;")

        self.state_label = QLabel()
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state_label.setStyleSheet(
            """
            font-size: 40px;
            font-weight: bold;
            color: white;
            background-color: rgba(0,0,0,50);
            border-radius: 20px;
            padding: 15px;
            """
        )

    def layout_ui(self):
        layout = QVBoxLayout()
        if hasattr(self, "title_label"):
            layout.addWidget(self.title_label)

        container = QWidget()
        container_layout = QHBoxLayout()
        container.setLayout(container_layout)
        container_layout.addWidget(self.time_label)
        container_layout.addWidget(self.state_label)

        layout.addWidget(container)
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
        self.update_state_label()

    def mousePressEvent(self, event):
        if self.state == StopwatchWidget.FINISHED:
            self.close()
        elif self.state == StopwatchWidget.RUNNING:
            self.timer.stop()
            self.state = StopwatchWidget.STOPPED
        else:
            self.timer.start()
            self.state = StopwatchWidget.RUNNING
        self.update_state_label()
        super().mousePressEvent(event)