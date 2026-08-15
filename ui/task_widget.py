from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QCheckBox, QLabel, QPushButton
)

class TaskItemWidget(QFrame):
    """
    Custom widget row displaying an individual task with checkbox,
    strikethrough effect, solid rounded priority pill badge,
    clickable time label (toggles priority badge), and delete action.
    """
    status_changed = pyqtSignal(str, bool)  # task_id, is_done
    delete_requested = pyqtSignal(str)       # task_id

    def __init__(self, task: dict, parent=None):
        super().__init__(parent)
        self.task_id = task["id"]
        self.task_data = task
        self._priority = task.get("priority", "Med")
        self._priority_visible = True

        self.setObjectName("TaskItemWidget")
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 6, 10, 6)
        main_layout.setSpacing(8)

        # Checkbox & Task Title
        self.checkbox = QCheckBox(self.task_data["title"])
        self.checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.checkbox.setChecked(self.task_data.get("is_done", False))
        self.checkbox.stateChanged.connect(self.on_checkbox_toggled)
        self.update_title_style(self.task_data.get("is_done", False))

        main_layout.addWidget(self.checkbox, stretch=1)

        # Right Meta Container: [PRIORITY_BADGE][TIME_LABEL][DELETE]
        right_meta_layout = QHBoxLayout()
        right_meta_layout.setSpacing(6)

        # Priority / Done Badge
        self.priority_badge = QLabel()
        self.priority_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.priority_badge.setMinimumWidth(44)
        self._apply_badge(self.task_data.get("is_done", False))
        right_meta_layout.addWidget(self.priority_badge, alignment=Qt.AlignmentFlag.AlignCenter)

        # Clickable Time Label — clicking it hides/shows priority badge
        deadline_str = self.task_data.get("deadline", "")
        time_str = self._extract_time(deadline_str)
        self.time_label = None
        if time_str and not self.task_data.get("is_done", False):
            self.time_label = QLabel(time_str)
            self.time_label.setObjectName("TimeLabel")
            self.time_label.setMinimumWidth(46)
            self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.time_label.setCursor(Qt.CursorShape.PointingHandCursor)
            self.time_label.setToolTip("Klik untuk sembunyikan/tampilkan prioritas")
            self.time_label.mousePressEvent = lambda e: self.toggle_priority_badge()
            right_meta_layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(right_meta_layout)

    def _extract_time(self, deadline_str: str) -> str:
        """Extracts HH:MM from deadline string like '2026-08-17 14:01'."""
        if not deadline_str:
            return ""
        parts = deadline_str.strip().split(" ")
        if len(parts) >= 2:
            time_parts = parts[1].split(":")
            if len(time_parts) >= 2:
                return f"{time_parts[0]}:{time_parts[1]}"
        return ""

    def toggle_priority_badge(self):
        """Toggles priority badge visibility when time label is clicked."""
        self._priority_visible = not self._priority_visible
        self.priority_badge.setVisible(self._priority_visible)

    def _apply_badge(self, is_done: bool):
        """Sets badge text and inline stylesheet based on done state or priority."""
        if is_done:
            self.priority_badge.setText("DONE")
            self.priority_badge.setStyleSheet(
                "background-color: #2563EB; color: #FFFFFF; border-radius: 6px; "
                "padding: 2px 8px; font-size: 10px; font-weight: bold; "
                "font-family: 'Segoe UI', sans-serif; letter-spacing: 0.3px;"
            )
            self.priority_badge.setToolTip("Status: Selesai / Done")
        else:
            priority = self._priority
            if priority == "High":
                text, bg = "HIGH", "#E60000"   # vivid red
                tooltip = "Prioritas: High (Tinggi)"
            elif priority == "Low":
                text, bg = "LOW", "#00A550"    # vivid green
                tooltip = "Prioritas: Low (Rendah)"
            else:
                text, bg = "MED", "#E8A000"    # vivid amber-yellow
                tooltip = "Prioritas: Med (Sedang)"
            self.priority_badge.setText(text)
            self.priority_badge.setStyleSheet(
                f"background-color: {bg}; color: #FFFFFF; border-radius: 6px; "
                f"padding: 2px 8px; font-size: 10px; font-weight: bold; "
                f"font-family: 'Segoe UI', sans-serif; letter-spacing: 0.3px;"
            )
            self.priority_badge.setToolTip(tooltip)

    def on_checkbox_toggled(self, state):
        is_done = (state == Qt.CheckState.Checked.value or state == 2 or state is True)
        self.update_title_style(is_done)
        self._apply_badge(is_done)
        # Hide time label when task is done (DONE badge takes its place)
        if self.time_label is not None:
            self.time_label.setVisible(not is_done)
        # Restore priority badge visibility when state changes
        self._priority_visible = True
        self.priority_badge.setVisible(True)
        self.status_changed.emit(self.task_id, is_done)

    def update_title_style(self, is_done: bool):
        """Applies strikethrough styling when task is checked."""
        font = self.checkbox.font()
        font.setStrikeOut(is_done)
        self.checkbox.setFont(font)
        if is_done:
            self.checkbox.setStyleSheet("color: #9CA3AF; text-decoration: line-through;")
        else:
            self.checkbox.setStyleSheet("text-decoration: none;")
