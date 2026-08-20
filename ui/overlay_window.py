from PyQt6.QtCore import Qt, QPoint, QDate, QEvent
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QDateEdit, QScrollArea, QFrame, QListView
)


class VerticalOnlyScrollArea(QScrollArea):
    """
    QScrollArea that strictly allows only vertical scrolling.
    - Blocks horizontal mouse-wheel / trackpad events.
    - Pins the inner widget width to the viewport on every resize so
      content can never overflow and trigger a horizontal scroll range.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.viewport().installEventFilter(self)

    # Block horizontal wheel/trackpad scroll
    def wheelEvent(self, event):
        delta = event.angleDelta()
        if abs(delta.y()) >= abs(delta.x()):
            super().wheelEvent(event)   # normal vertical scroll
        else:
            event.ignore()              # drop pure-horizontal gesture

    # Pin inner widget width whenever the scroll area is resized
    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.widget()
        if w:
            w.setFixedWidth(self.viewport().width())

    # Also intercept viewport events for completeness
    def eventFilter(self, obj, event):
        if obj is self.viewport() and event.type() == QEvent.Type.Wheel:
            delta = event.angleDelta()
            if abs(delta.x()) > abs(delta.y()):   # horizontal-dominant
                return True                        # consume / block it
        return super().eventFilter(obj, event)

from ui.styles import get_style
from ui.task_widget import TaskItemWidget, set_colorblind_mode
from storage import TaskManager, SettingsManager
from reminder import ReminderWatchdog

TRANSLATIONS = {
    "ID": {
        "title": "📌 NudgeNote",
        "add_placeholder": "Tambah tugas baru...",
        "add_btn": "+ Tambah",
        "lang_tooltip": "Ganti Bahasa (ID / EN)",
        "settings_tooltip": "Buka Pengaturan",
        "priority_tooltip": "Pilih Skala Prioritas (High, Medium, Low)",
        "date_tooltip": "Memilih Tanggal Deadline",
        "time_tooltip": "Memilih Jam Deadline",
        "delete_tooltip": "Hapus Tugas",
        "sort_label": "Urutkan:",
        "sort_options": ["Prioritas", "Deadline"],
        "year_label": "Tahun:",
    },
    "EN": {
        "title": "📌 NudgeNote",
        "add_placeholder": "Add new task...",
        "add_btn": "+ Add",
        "lang_tooltip": "Switch Language (ID / EN)",
        "settings_tooltip": "Open Settings",
        "priority_tooltip": "Select Priority Level (High, Medium, Low)",
        "date_tooltip": "Select Deadline Date",
        "time_tooltip": "Select Deadline Time",
        "delete_tooltip": "Delete Task",
        "sort_label": "Sort by:",
        "sort_options": ["Priority", "Deadline"],
        "year_label": "Year:",
    }
}

class CompactComboBox(QComboBox):
    """
    Custom QComboBox that enforces strict popup height limit (e.g. 5 items)
    with smooth scrolling, avoids infinite vertical popup on Windows,
    and positions the popup directly below the combobox.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setView(QListView(self))
        self.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def showPopup(self):
        super().showPopup()
        popup = self.view().window()
        if popup:
            item_h = 20
            visible_count = min(self.count(), self.maxVisibleItems())
            target_h = item_h * visible_count + 6
            pos = self.mapToGlobal(QPoint(0, self.height() + 2))
            popup.setGeometry(pos.x(), pos.y(), self.width(), target_h)



class NudgeNoteOverlay(QWidget):
    """
    Main Frameless Always-on-Top Desktop Overlay Window for NudgeNote.
    Supports smooth dragging, 5 selectable themes, EN/ID Language toggle,
    Sort By (Priority vs Deadline) options, Dot Priority indicators,
    JSON auto-save, and background deadline watchdog popups.
    Settings Panel provides: theme, font, colorblind mode, deadline alert
    hours, custom alert sound, and Windows startup toggle.
    """

    def __init__(self):
        super().__init__()

        # Data, Settings & Background Watchdog Manager
        self.task_manager = TaskManager()
        self.settings_manager = SettingsManager()
        self.current_theme = self.settings_manager.get_theme()
        self.current_font = self.settings_manager.get_font()
        self.current_custom_bg = self.settings_manager.get_custom_bg()
        self.current_colorblind = self.settings_manager.get_colorblind_mode()
        
        # Apply colorblind mode to task widget module
        set_colorblind_mode(self.current_colorblind)
        
        self.current_lang = self.settings_manager.get_lang()
        self.current_sort = self.settings_manager.get_sort_by()
        self.selected_month = None  # None = show all months
        self.selected_year = QDate.currentDate().year()  # default: current year
        self.month_buttons = []

        self.watchdog = ReminderWatchdog(self.task_manager, self.settings_manager)
        self.watchdog.reminder_alert.connect(self.on_reminder_alert)
        self.watchdog.start()

        # Dragging State
        self.drag_position = QPoint()

        # Frameless, Always-on-Top, and Translucent Window Flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.resize(450, 570)
        self.setMinimumSize(420, 440)

        self.init_ui()
        self.apply_current_style()
        self.update_lang_ui()  # also calls refresh_task_list internally

    def init_ui(self):
        # Outer Base Layout
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Main Container Frame
        self.container = QFrame(self)
        self.container.setObjectName("OverlayContainer")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # 1. Custom Frameless Title Bar / Header
        header_frame = QFrame(self.container)
        header_frame.setObjectName("HeaderFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(12, 8, 12, 8)
        header_layout.setSpacing(6)

        # Title Label
        self.title_label = QLabel("📌 NudgeNote", header_frame)
        self.title_label.setObjectName("AppTitle")
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        # Settings Button (⚙️) — opens Settings Dialog
        self.settings_btn = QPushButton("⚙️", header_frame)
        self.settings_btn.setObjectName("SettingsBtn")
        self.settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_btn.clicked.connect(self.open_settings)
        header_layout.addWidget(self.settings_btn)

        # Language Switcher Button (ID / EN)
        self.lang_btn = QPushButton(self.current_lang, header_frame)
        self.lang_btn.setObjectName("LangToggleBtn")
        self.lang_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lang_btn.clicked.connect(self.toggle_language)
        header_layout.addWidget(self.lang_btn)

        # Minimize Button
        min_btn = QPushButton("—", header_frame)
        min_btn.setProperty("class", "WindowBtn")
        min_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        min_btn.clicked.connect(self.showMinimized)
        header_layout.addWidget(min_btn)

        # Close Button
        close_btn = QPushButton("✕", header_frame)
        close_btn.setObjectName("CloseBtn")
        close_btn.setProperty("class", "WindowBtn")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)

        container_layout.addWidget(header_frame)

        # 2. Main Content Area
        content_widget = QWidget(self.container)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(8)

        # Quick Add Task Form
        add_form_layout = QVBoxLayout()
        add_form_layout.setSpacing(8)

        # Task Title Input
        self.title_input = QLineEdit(content_widget)
        self.title_input.returnPressed.connect(self.on_add_task)
        add_form_layout.addWidget(self.title_input)

        # Options Row: Priority + Date + Time + Add Button
        options_layout = QHBoxLayout()
        options_layout.setSpacing(6)

        # Priority Selector (1. High, 2. Med, 3. Low)
        self.priority_combo = CompactComboBox(content_widget)
        self.priority_combo.addItems(["High", "Med", "Low"])
        self.priority_combo.setCurrentText("High")
        options_layout.addWidget(self.priority_combo)

        # Date Picker (Memilih Tanggal)
        self.date_edit = QDateEdit(QDate.currentDate(), content_widget)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setMinimumWidth(108)
        options_layout.addWidget(self.date_edit)

        # Time Input - plain text, user types freely, default 12:00
        self.time_input = QLineEdit("12:00", content_widget)
        self.time_input.setObjectName("TimeInput")
        self.time_input.setPlaceholderText("HH:MM")
        self.time_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_input.setMinimumWidth(68)
        self.time_input.setMaximumWidth(80)
        self.time_input.textChanged.connect(self._auto_format_time)
        options_layout.addWidget(self.time_input)

        # Add Button
        self.add_btn = QPushButton(content_widget)
        self.add_btn.setObjectName("AddTaskBtn")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(self.on_add_task)
        options_layout.addWidget(self.add_btn)

        add_form_layout.addLayout(options_layout)
        content_layout.addLayout(add_form_layout)

        # Sort & Year Row (Left: Urutkan [SortCombo] | Right: Tahun: [YearCombo])
        sort_year_layout = QHBoxLayout()
        sort_year_layout.setContentsMargins(2, 4, 2, 2)
        sort_year_layout.setSpacing(6)

        self.sort_label = QLabel(content_widget)
        self.sort_label.setObjectName("SortLabel")
        sort_year_layout.addWidget(self.sort_label)

        self.sort_combo = CompactComboBox(content_widget)
        self.sort_combo.setObjectName("SortCombo")
        self.sort_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sort_combo.currentIndexChanged.connect(self.on_sort_changed)
        sort_year_layout.addWidget(self.sort_combo)

        sort_year_layout.addStretch()

        self.year_label = QLabel(content_widget)
        self.year_label.setObjectName("YearLabel")
        sort_year_layout.addWidget(self.year_label)

        # Year Dropdown (2026 – 2099)
        self.year_combo = CompactComboBox(content_widget)
        self.year_combo.setObjectName("YearCombo")
        self.year_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.year_combo.setMaxVisibleItems(5)
        self.year_combo.blockSignals(True)
        for y in range(2026, 2100):
            self.year_combo.addItem(str(y))
        current_year = QDate.currentDate().year()
        self.year_combo.setCurrentText(str(max(2026, current_year)))
        self.year_combo.blockSignals(False)
        self.year_combo.currentIndexChanged.connect(self._on_year_filter)
        sort_year_layout.addWidget(self.year_combo)

        content_layout.addLayout(sort_year_layout)

        # Month Filter Bar — wrapped in a dark pill container for wallpaper readability
        month_bar_frame = QFrame(content_widget)
        month_bar_frame.setObjectName("MonthBarRow")
        month_bar_layout = QHBoxLayout(month_bar_frame)
        month_bar_layout.setContentsMargins(4, 3, 4, 3)
        month_bar_layout.setSpacing(3)

        for i in range(1, 13):
            btn = QPushButton()
            btn.setObjectName("MonthFilterBtn")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, m=i: self._on_month_filter(m))
            month_bar_layout.addWidget(btn)
            self.month_buttons.append(btn)

        content_layout.addWidget(month_bar_frame)

        # Task Scroll List — vertical scroll ONLY (custom class blocks all horizontal)
        self.scroll_area = VerticalOnlyScrollArea(content_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.task_list_container = QWidget()
        self.task_list_container.setObjectName("TaskListContainer")

        self.task_list_layout = QVBoxLayout(self.task_list_container)
        self.task_list_layout.setContentsMargins(0, 0, 0, 0)
        self.task_list_layout.setSpacing(6)
        self.task_list_layout.addStretch()

        self.scroll_area.setWidget(self.task_list_container)
        content_layout.addWidget(self.scroll_area, stretch=1)

        container_layout.addWidget(content_widget, stretch=1)
        outer_layout.addWidget(self.container)

    # ── Theme & Style ──────────────────────────────────────────────────────────

    def apply_current_style(self):
        """Applies the current theme/font/colorblind/bg stylesheet to the window."""
        self.setStyleSheet(get_style(
            self.current_theme,
            self.current_font,
            self.current_colorblind,
            self.current_custom_bg
        ))

    # ── Settings Dialog ────────────────────────────────────────────────────────

    def open_settings(self):
        """Opens the Settings Dialog. On save, applies updated settings live."""
        from ui.settings_dialog import SettingsDialog

        dialog = SettingsDialog(self.settings_manager, parent=self)
        # Position dialog near the settings button
        btn_pos = self.settings_btn.mapToGlobal(QPoint(0, self.settings_btn.height() + 4))
        dialog.move(btn_pos.x(), btn_pos.y())
        dialog.settings_saved.connect(self._on_settings_saved)
        dialog.exec()

    def _on_settings_saved(self):
        """Triggered when user clicks Save in SettingsDialog. Applies all new settings live."""
        self.current_theme = self.settings_manager.get_theme()
        self.current_font = self.settings_manager.get_font()
        self.current_custom_bg = self.settings_manager.get_custom_bg()
        
        new_colorblind = self.settings_manager.get_colorblind_mode()
        self.current_colorblind = new_colorblind
        set_colorblind_mode(self.current_colorblind)

        self.apply_current_style()
        self.refresh_task_list()  # Forces a re-render of badges for colorblindness

    # ── Language ───────────────────────────────────────────────────────────────

    def toggle_language(self):
        """Toggles between ID and EN language and persists setting."""
        if self.current_lang == "ID":
            self.current_lang = "EN"
        else:
            self.current_lang = "ID"

        self.settings_manager.set_lang(self.current_lang)
        self.update_lang_ui()

    def update_lang_ui(self):
        """Updates UI texts according to current language (ID or EN)."""
        MONTHS_SHORT_ID = ["JAN","FEB","MAR","APR","MEI","JUN",
                           "JUL","AGU","SEP","OKT","NOV","DES"]
        MONTHS_SHORT_EN = ["JAN","FEB","MAR","APR","MAY","JUN",
                           "JUL","AUG","SEP","OCT","NOV","DEC"]

        self.lang_btn.setText(self.current_lang)
        t = TRANSLATIONS.get(self.current_lang, TRANSLATIONS["ID"])

        self.title_input.setPlaceholderText(t["add_placeholder"])
        self.add_btn.setText(t["add_btn"])

        self.lang_btn.setToolTip(t["lang_tooltip"])
        self.settings_btn.setToolTip(t["settings_tooltip"])
        self.priority_combo.setToolTip(t["priority_tooltip"])
        self.date_edit.setToolTip(t["date_tooltip"])
        self.time_input.setToolTip(t["time_tooltip"])

        # Update sort & year bar UI
        self.sort_label.setText(t["sort_label"])
        self.year_label.setText(t.get("year_label", "Tahun:"))
        self.sort_combo.blockSignals(True)
        self.sort_combo.clear()
        self.sort_combo.addItems(t["sort_options"])
        self.sort_combo.setCurrentIndex(1 if self.current_sort == "deadline" else 0)
        self.sort_combo.blockSignals(False)

        # Update month button labels for current language
        names = MONTHS_SHORT_ID if self.current_lang == "ID" else MONTHS_SHORT_EN
        for i, btn in enumerate(self.month_buttons):
            btn.setText(names[i])

        # Refresh task list so date headers use updated language
        self.refresh_task_list()

    def on_sort_changed(self, index: int):
        """Triggered when user selects a different sorting option."""
        sort_by = "deadline" if index == 1 else "priority"
        self.current_sort = sort_by
        self.settings_manager.set_sort_by(sort_by)
        self.refresh_task_list()

    def on_add_task(self):
        """Handles task creation from UI inputs (Priority, Date, and Time)."""
        title = self.title_input.text().strip()
        if not title:
            return

        priority = self.priority_combo.currentText()
        date_str = self.date_edit.date().toString("yyyy-MM-dd")

        # Sanitize time input: allow empty (no time) or parse HH:MM
        raw_time = self.time_input.text().strip()
        if raw_time:
            # Normalize separator - accept HH.MM or HH:MM
            raw_time = raw_time.replace(".", ":")
            parts = raw_time.split(":")
            try:
                h = int(parts[0]) % 24
                m = int(parts[1]) % 60 if len(parts) > 1 else 0
                time_str = f"{h:02d}:{m:02d}"
            except (ValueError, IndexError):
                time_str = "12:00"
            deadline_str = f"{date_str} {time_str}"
        else:
            deadline_str = date_str

        self.task_manager.add_task(title=title, priority=priority, deadline_str=deadline_str)
        self.title_input.clear()

        # Reset date to today, time back to 12:00
        self.date_edit.setDate(QDate.currentDate())
        self.time_input.setText("12:00")

        self.refresh_task_list()

    def _on_month_filter(self, month_num: int):
        """Toggles the month filter. Clicking the active month deselects it (show all)."""
        if self.selected_month == month_num:
            self.selected_month = None
            for btn in self.month_buttons:
                btn.setChecked(False)
        else:
            self.selected_month = month_num
            for i, btn in enumerate(self.month_buttons):
                btn.setChecked(i + 1 == month_num)
        self.refresh_task_list()

    def _on_year_filter(self, index: int):
        """Updates the active year filter from the year combo selection."""
        self.selected_year = 2026 + index
        self.refresh_task_list()

    def _task_month(self, task: dict) -> int:
        """Returns the month number (1-12) from a task's deadline, or 0 if none."""
        deadline = task.get("deadline", "")
        if not deadline:
            return 0
        try:
            return int(deadline.split("-")[1])
        except (IndexError, ValueError):
            return 0

    def _task_year(self, task: dict) -> int:
        """Returns the year (e.g. 2026) from a task's deadline, or 0 if none."""
        deadline = task.get("deadline", "")
        if not deadline:
            return 0
        try:
            return int(deadline.split("-")[0])
        except (IndexError, ValueError):
            return 0

    def refresh_task_list(self):
        """Clears and re-renders task items grouped by deadline date with date headers."""
        while self.task_list_layout.count() > 0:
            item = self.task_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        from storage import PRIORITY_WEIGHTS
        from collections import OrderedDict

        all_tasks = self.task_manager.tasks

        # Filter by selected year (always active - defaults to current year)
        if self.selected_year is not None:
            all_tasks = [t for t in all_tasks if self._task_year(t) == self.selected_year]

        # Filter by selected month if active
        if self.selected_month is not None:
            all_tasks = [t for t in all_tasks if self._task_month(t) == self.selected_month]

        active_tasks = [t for t in all_tasks if not t.get("is_done", False)]
        done_tasks   = [t for t in all_tasks if t.get("is_done", False)]

        # Sort key respects current_sort: "deadline" sorts by full datetime; "priority" sorts by priority then time
        def sort_key(t):
            deadline = t.get("deadline", "")
            date_part = deadline.split(" ")[0] if deadline else "9999-99-99"
            time_part = deadline.split(" ")[1] if " " in deadline else "99:99"
            pw = PRIORITY_WEIGHTS.get(t.get("priority", "Med"), 4)
            if self.current_sort == "deadline":
                return (date_part, time_part, pw)
            else:
                return (date_part, pw, time_part)

        active_tasks.sort(key=sort_key)
        done_tasks.sort(key=lambda t: t.get("deadline", ""))

        all_sorted = active_tasks + done_tasks

        # Group by deadline date
        date_groups = OrderedDict()
        no_deadline = []

        for task in all_sorted:
            deadline = task.get("deadline", "").strip()
            if deadline:
                date_part = deadline.split(" ")[0]
                if date_part not in date_groups:
                    date_groups[date_part] = []
                date_groups[date_part].append(task)
            else:
                no_deadline.append(task)

        for date_str, tasks in date_groups.items():
            self.task_list_layout.addWidget(self._make_date_header(date_str))
            for task in tasks:
                w = TaskItemWidget(task)
                w.status_changed.connect(self.on_task_status_changed)
                w.delete_requested.connect(self.on_task_delete_requested)
                self.task_list_layout.addWidget(w)

        if no_deadline:
            self.task_list_layout.addWidget(self._make_date_header(None))
            for task in no_deadline:
                w = TaskItemWidget(task)
                w.status_changed.connect(self.on_task_status_changed)
                w.delete_requested.connect(self.on_task_delete_requested)
                self.task_list_layout.addWidget(w)

        self.task_list_layout.addStretch()

    def _make_date_header(self, date_str) -> QLabel:
        """Creates a styled date-separator label for the task list."""
        MONTHS_ID = {
            1:"Januari",2:"Februari",3:"Maret",4:"April",
            5:"Mei",6:"Juni",7:"Juli",8:"Agustus",
            9:"September",10:"Oktober",11:"November",12:"Desember"
        }
        MONTHS_EN = {
            1:"January",2:"February",3:"March",4:"April",
            5:"May",6:"June",7:"July",8:"August",
            9:"September",10:"October",11:"November",12:"December"
        }
        if date_str is None:
            display = "Tanpa Deadline" if self.current_lang == "ID" else "No Deadline"
        else:
            try:
                from datetime import datetime
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                if self.current_lang == "ID":
                    display = f"{dt.day} {MONTHS_ID[dt.month]} {dt.year}"
                else:
                    display = f"{MONTHS_EN[dt.month]} {dt.day}, {dt.year}"
            except ValueError:
                display = date_str
        label = QLabel(display)
        label.setObjectName("DateHeader")
        return label

    def _auto_format_time(self, text: str):
        """Auto-inserts colon after first 2 digits when user types in time input."""
        # Only auto-insert colon when exactly 2 digit chars typed with no colon yet
        if len(text) == 2 and text.isdigit():
            self.time_input.blockSignals(True)
            self.time_input.setText(text + ":")
            self.time_input.setCursorPosition(3)
            self.time_input.blockSignals(False)
        elif len(text) > 5:
            # Clamp to HH:MM (max 5 chars)
            clean = text.replace(":", "")[:4]
            if len(clean) >= 3:
                formatted = f"{clean[:2]}:{clean[2:4]}"
            else:
                formatted = clean
            self.time_input.blockSignals(True)
            self.time_input.setText(formatted)
            self.time_input.setCursorPosition(len(formatted))
            self.time_input.blockSignals(False)

    def on_task_status_changed(self, task_id: str, is_done: bool):
        """Updates task state and triggers list re-sorting."""
        self.task_manager.update_task_status(task_id, is_done)
        self.refresh_task_list()

    def on_task_delete_requested(self, task_id: str):
        """Deletes a task by ID and refreshes list."""
        self.task_manager.delete_task(task_id)
        self.refresh_task_list()

    def on_reminder_alert(self, title: str, message: str):
        """Triggered when background watchdog detects a deadline."""
        print(f"[NudgeNote Watchdog Alert] {title}: {message}")

    # Window Mouse Dragging Logic
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
