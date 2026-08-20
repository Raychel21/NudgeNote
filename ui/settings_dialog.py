"""
NudgeNote — Settings Dialog
A polished, scrollable settings panel opened from the main header.
Sections:
  1. Appearance  — Theme (5 cards) + Font picker
  2. Accessibility — Colorblind mode (3 radio buttons)
  3. Notifications — Deadline alert hours (spin box)
  4. Alert Sound   — File browser for .mp3 / .wav
  5. System        — Run at Windows startup (checkbox)
"""

import os
from PyQt6.QtCore import Qt, pyqtSignal, QEvent, QPoint
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame, QSpinBox, QCheckBox,
    QComboBox, QButtonGroup, QRadioButton, QFileDialog,
    QLineEdit, QSizePolicy, QMessageBox
)

class NoScrollComboBox(QComboBox):
    """Combobox that ignores scroll wheel events unless the dropdown popup is open.
    
    The key fix: check view().isVisible() instead of hasFocus().
    hasFocus() is True whenever the widget has keyboard focus (e.g. after clicking
    it once), which means scrolling the settings body would still spin the combo.
    view().isVisible() is only True when the popup is actively open.
    """
    def wheelEvent(self, event):
        if self.view().isVisible():
            # Popup is open — allow scrolling through options
            super().wheelEvent(event)
        else:
            # Popup is closed — forward scroll to parent (settings scroll area)
            event.ignore()

from ui.styles import (
    THEME_DISPLAY_NAMES, AVAILABLE_FONTS, COLORBLIND_DISPLAY_NAMES,
    AVAILABLE_THEMES, get_style
)

# ─── Bilingual translations for all Settings dialog text ─────────────────────
SETTINGS_TRANSLATIONS = {
    "EN": {
        "title":              "  ⚙️  Settings",
        "drag_hint":          "Drag to move",
        # Section headers
        "s_appearance":       "APPEARANCE",
        "s_custom_bg":        "Custom Background Image",
        "s_font":             "FONT",
        "s_accessibility":    "ACCESSIBILITY — COLOR VISION",
        "s_notifications":    "NOTIFICATIONS",
        "s_sound":            "ALERT SOUND",
        "s_system":           "SYSTEM",
        # Font section
        "font_label":         "Font Family:",
        # Custom BG section
        "bg_placeholder":     "No custom background selected",
        "bg_upload_btn":      "📂  Upload && Crop",
        "bg_clear_btn":       "✕  Clear",
        "bg_hint":            "Upload an image and crop it to fit the NudgeNote window (450 × 570).",
        "bg_dialog_title":    "Select Background Image",
        # Colorblind section
        "cb_hint":            "Changes badge and accent colors to be accessible for color vision differences.",
        "cb_normal":          "Normal",
        "cb_deuteranopia":    "Deuteranopia (Red-Green)",
        "cb_protanopia":      "Protanopia (Red Weak)",
        # Notifications section
        "notif_hint":         "Show a popup reminder this many hours before the deadline.",
        "notif_suffix":       "hours before deadline  (max 48 hrs)",
        # Alert sound section
        "sound_hint":         "Play a custom sound when a reminder popup appears. Supported: .mp3, .wav",
        "sound_no_file":      "No file selected",
        "sound_browse_btn":   "Browse",
        "sound_clear_btn":    "Clear",
        "sound_dialog_title": "Select Alert Sound",
        # System section
        "startup_check":      "Launch NudgeNote automatically when Windows starts",
        "startup_hint":       "Adds NudgeNote to the Windows startup registry (HKCU Run). No admin rights needed.",
        # Footer
        "cancel_btn":         "Cancel",
        "save_btn":           "Save Settings",
    },
    "ID": {
        "title":              "  ⚙️  Pengaturan",
        "drag_hint":          "Seret untuk memindahkan",
        # Section headers
        "s_appearance":       "TAMPILAN",
        "s_custom_bg":        "Gambar Latar Belakang Kustom",
        "s_font":             "FONT",
        "s_accessibility":    "AKSESIBILITAS — PENGLIHATAN WARNA",
        "s_notifications":    "NOTIFIKASI",
        "s_sound":            "SUARA PERINGATAN",
        "s_system":           "SISTEM",
        # Font section
        "font_label":         "Keluarga Font:",
        # Custom BG section
        "bg_placeholder":     "Belum ada latar belakang dipilih",
        "bg_upload_btn":      "📂  Unggah && Pangkas",
        "bg_clear_btn":       "✕  Hapus",
        "bg_hint":            "Unggah gambar dan pangkas sesuai ukuran jendela NudgeNote (450 × 570).",
        "bg_dialog_title":    "Pilih Gambar Latar Belakang",
        # Colorblind section
        "cb_hint":            "Mengubah warna lencana dan aksen agar ramah bagi pengguna dengan perbedaan penglihatan warna.",
        "cb_normal":          "Normal",
        "cb_deuteranopia":    "Deuteranopia (Merah-Hijau)",
        "cb_protanopia":      "Protanopia (Lemah Merah)",
        # Notifications section
        "notif_hint":         "Tampilkan pengingat popup sejumlah jam ini sebelum batas waktu deadline.",
        "notif_suffix":       "jam sebelum deadline  (maks 48 jam)",
        # Alert sound section
        "sound_hint":         "Putar suara kustom saat popup pengingat muncul. Didukung: .mp3, .wav",
        "sound_no_file":      "Belum ada file dipilih",
        "sound_browse_btn":   "Cari File",
        "sound_clear_btn":    "Hapus",
        "sound_dialog_title": "Pilih Suara Peringatan",
        # System section
        "startup_check":      "Jalankan NudgeNote otomatis saat Windows dimulai",
        "startup_hint":       "Menambahkan NudgeNote ke registry startup Windows (HKCU Run). Tidak perlu hak administrator.",
        # Footer
        "cancel_btn":         "Batal",
        "save_btn":           "Simpan Pengaturan",
    },
}


# ─── Per-theme preview swatch colors (bg, accent) ────────────────────────────
THEME_SWATCHES = {
    "midnight":  ("#161923", "#6366F1", "#F3F4F6"),
    "aurora":    ("#0D1F1A", "#10B981", "#ECFDF5"),
    "crimson":   ("#1A0D10", "#E11D48", "#FFF1F2"),
    "parchment": ("#FAF7F2", "#B45309", "#2D1F0E"),
    "arctic":    ("#F0F5FB", "#0284C7", "#0F2D4A"),
}

_DIALOG_STYLE = """
QDialog {{
    background-color: {bg};
    border: 1px solid {border};
    border-radius: 14px;
}}

/* Scrollable content area */
QScrollArea {{
    background: transparent;
    border: none;
}}
QScrollArea > QWidget > QWidget {{
    background: transparent;
}}

/* Section header labels */
#SectionHeader {{
    color: {accent};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    font-family: '{font}', 'Segoe UI', sans-serif;
    padding: 2px 0 4px 0;
}}

/* Divider */
#Divider {{
    background: {divider};
    min-height: 1px;
    max-height: 1px;
    border: none;
}}

/* Theme card buttons */
#ThemeCard {{
    border-radius: 10px;
    border: 2px solid transparent;
    padding: 0px;
    font-size: 11px;
    font-weight: 600;
    font-family: '{font}', 'Segoe UI', sans-serif;
}}
#ThemeCard:checked {{
    border: 2px solid {accent};
}}

/* Font/colorblind combos & spin boxes */
QComboBox, QSpinBox {{
    background-color: {input_bg};
    border: 1px solid {input_border};
    border-radius: 7px;
    color: {text};
    padding: 5px 8px;
    font-size: 12px;
    font-family: '{font}', 'Segoe UI', sans-serif;
    min-height: 28px;
}}

QComboBox:focus, QSpinBox:focus {{
    border: 1px solid {accent};
}}

QComboBox QAbstractItemView {{
    background-color: {popup_bg};
    border: 1px solid {input_border};
    selection-background-color: {accent};
    color: {text};
    border-radius: 6px;
}}

QSpinBox::up-button, QSpinBox::down-button {{
    width: 18px;
    border: none;
    background: {input_bg};
}}

/* Checkbox */
QCheckBox {{
    color: {text};
    font-size: 12px;
    font-family: '{font}', 'Segoe UI', sans-serif;
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 2px solid {check_border};
    background-color: transparent;
}}
QCheckBox::indicator:checked {{
    background-color: {accent};
    border-color: {accent};
}}

/* Radio buttons */
QRadioButton {{
    color: {text};
    font-size: 12px;
    font-family: '{font}', 'Segoe UI', sans-serif;
    spacing: 8px;
}}
QRadioButton::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid {check_border};
    background-color: transparent;
}}
QRadioButton::indicator:checked {{
    background-color: {accent};
    border-color: {accent};
}}

/* Sound path display */
#SoundPathEdit {{
    background-color: {input_bg};
    border: 1px solid {input_border};
    border-radius: 7px;
    color: {text_muted};
    padding: 4px 8px;
    font-size: 11px;
    font-family: '{font}', 'Segoe UI', sans-serif;
}}

/* Browse / Clear buttons */
#BrowseBtn, #ClearBtn {{
    background-color: {btn_bg};
    color: {btn_fg};
    border: 1px solid {btn_border};
    border-radius: 7px;
    font-size: 11px;
    font-weight: 600;
    font-family: '{font}', 'Segoe UI', sans-serif;
    padding: 4px 10px;
    min-height: 26px;
}}
#BrowseBtn:hover, #ClearBtn:hover {{
    background-color: {btn_bg_hover};
    color: {btn_fg_hover};
    border-color: {accent};
}}

/* Save / Cancel */
#SaveBtn {{
    background-color: {accent};
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    font-size: 13px;
    font-weight: bold;
    font-family: '{font}', 'Segoe UI', sans-serif;
    padding: 8px 24px;
    min-height: 34px;
}}
#SaveBtn:hover {{
    background-color: {accent_hover};
}}
#CancelBtn {{
    background-color: {btn_bg};
    color: {btn_fg};
    border: 1px solid {btn_border};
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    font-family: '{font}', 'Segoe UI', sans-serif;
    padding: 8px 20px;
    min-height: 34px;
}}
#CancelBtn:hover {{
    background-color: {btn_bg_hover};
    border-color: {accent};
    color: {btn_fg_hover};
}}

/* Description / hint text */
#HintLabel {{
    color: {text_muted};
    font-size: 10px;
    font-family: '{font}', 'Segoe UI', sans-serif;
}}

/* Font section live preview */
#FontPreviewLabel {{
    color: {text};
    font-size: 12px;
    background-color: {input_bg};
    border: 1px solid {input_border};
    border-radius: 7px;
    padding: 6px 10px;
    min-height: 28px;
}}

/* Sub-section label (e.g. "Custom Background Image") */
#SubSectionLabel {{
    color: {text};
    font-size: 11px;
    font-weight: 600;
    font-family: '{font}', 'Segoe UI', sans-serif;
    opacity: 0.8;
}}

/* Drag handle icon in header */
#DragIcon {{
    color: {text_muted};
    font-size: 14px;
    padding: 0 4px 0 0;
}}

/* Value labels next to spinbox */
#SpinSuffix {{
    color: {text_muted};
    font-size: 11px;
    font-family: '{font}', 'Segoe UI', sans-serif;
}}
"""

# Per-theme dialog style tokens
_DIALOG_TOKENS = {
    "midnight":  {
        "bg": "#1A1F2E", "border": "rgba(255,255,255,0.15)",
        "accent": "#6366F1", "accent_hover": "#4F46E5",
        "text": "#F3F4F6", "text_muted": "#9CA3AF",
        "divider": "rgba(255,255,255,0.08)",
        "input_bg": "#232838", "input_border": "rgba(255,255,255,0.12)",
        "popup_bg": "#1E2230",
        "check_border": "#6B7280",
        "btn_bg": "rgba(99,102,241,0.15)", "btn_fg": "#A5B4FC",
        "btn_border": "rgba(99,102,241,0.3)",
        "btn_bg_hover": "rgba(99,102,241,0.3)", "btn_fg_hover": "#FFFFFF",
    },
    "aurora": {
        "bg": "#112920", "border": "rgba(16,185,129,0.2)",
        "accent": "#10B981", "accent_hover": "#059669",
        "text": "#ECFDF5", "text_muted": "#6EE7B7",
        "divider": "rgba(16,185,129,0.1)",
        "input_bg": "#1A2E27", "input_border": "rgba(16,185,129,0.2)",
        "popup_bg": "#132920",
        "check_border": "#4B9E82",
        "btn_bg": "rgba(16,185,129,0.12)", "btn_fg": "#6EE7B7",
        "btn_border": "rgba(16,185,129,0.3)",
        "btn_bg_hover": "rgba(16,185,129,0.25)", "btn_fg_hover": "#FFFFFF",
    },
    "crimson": {
        "bg": "#1F1018", "border": "rgba(225,29,72,0.2)",
        "accent": "#E11D48", "accent_hover": "#BE123C",
        "text": "#FFF1F2", "text_muted": "#FCA5A5",
        "divider": "rgba(225,29,72,0.1)",
        "input_bg": "#271318", "input_border": "rgba(225,29,72,0.18)",
        "popup_bg": "#221218",
        "check_border": "#9B4258",
        "btn_bg": "rgba(225,29,72,0.12)", "btn_fg": "#FCA5A5",
        "btn_border": "rgba(225,29,72,0.3)",
        "btn_bg_hover": "rgba(225,29,72,0.25)", "btn_fg_hover": "#FFFFFF",
    },
    "parchment": {
        "bg": "#FFFBF5", "border": "#E8DFD0",
        "accent": "#B45309", "accent_hover": "#92400E",
        "text": "#2D1F0E", "text_muted": "#8B6F4E",
        "divider": "#EDE4D6",
        "input_bg": "#FFFFFF", "input_border": "#D4B896",
        "popup_bg": "#FFFFFF",
        "check_border": "#C4A882",
        "btn_bg": "#F0E8DC", "btn_fg": "#7C4A1E",
        "btn_border": "#D4B896",
        "btn_bg_hover": "#E4D5C0", "btn_fg_hover": "#2D1F0E",
    },
    "arctic": {
        "bg": "#F5F9FD", "border": "#C9DAEA",
        "accent": "#0284C7", "accent_hover": "#0369A1",
        "text": "#0F2D4A", "text_muted": "#4A7499",
        "divider": "#DCE8F5",
        "input_bg": "#FFFFFF", "input_border": "#BAD7ED",
        "popup_bg": "#FFFFFF",
        "check_border": "#7BB3D0",
        "btn_bg": "#E0EEF8", "btn_fg": "#0C4A6E",
        "btn_border": "#BAD7ED",
        "btn_bg_hover": "#CFE4F5", "btn_fg_hover": "#0F2D4A",
    },
}


class SettingsDialog(QDialog):
    """
    Settings dialog for NudgeNote.
    Emits settings_saved(theme, font, colorblind_mode) when the user saves.
    """
    settings_saved = pyqtSignal()

    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager

        # Load current values
        self._theme     = settings_manager.get_theme()
        self._font      = settings_manager.get_font()
        self._custom_bg = settings_manager.get_custom_bg()
        self._alert_hours = settings_manager.get_deadline_alert_hours()
        self._startup   = settings_manager.get_startup_from_registry()
        self._sound_path = settings_manager.get_alert_sound()
        self._colorblind = settings_manager.get_colorblind_mode()

        # Language — read from settings so dialog matches the main app language
        self._lang = settings_manager.get_lang()          # "ID" or "EN"
        self._t    = SETTINGS_TRANSLATIONS.get(self._lang, SETTINGS_TRANSLATIONS["EN"])

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Dialog |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedWidth(480)

        # Drag state — only active when dragging from header
        self._drag_pos: QPoint | None = None
        self._drag_header = None  # set in _init_ui

        self._theme_btns: dict[str, QPushButton] = {}
        self._colorblind_radios: dict[str, QRadioButton] = {}

        self._init_ui()
        self._apply_dialog_style(self._theme, self._font)

    # ─── Build UI ─────────────────────────────────────────────────────────────

    def _init_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.container = QFrame(self)
        self.container.setObjectName("SettingsContainer")
        outer.addWidget(self.container)

        root = QVBoxLayout(self.container)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Dialog header (drag zone) ──
        hdr = QFrame(self.container)
        hdr.setObjectName("SettingsHeader")
        hdr.setCursor(Qt.CursorShape.SizeAllCursor)  # visual hint: draggable
        hdr_layout = QHBoxLayout(hdr)
        hdr_layout.setContentsMargins(16, 13, 12, 13)

        drag_icon = QLabel("⠿")
        drag_icon.setObjectName("DragIcon")
        drag_icon.setToolTip(self._t["drag_hint"])
        hdr_layout.addWidget(drag_icon)

        self.hdr_title = QLabel(self._t["title"], hdr)
        self.hdr_title.setObjectName("SettingsTitle")
        hdr_layout.addWidget(self.hdr_title)
        hdr_layout.addStretch()

        close_x = QPushButton("✕", hdr)
        close_x.setObjectName("SettingsCloseBtn")
        close_x.setCursor(Qt.CursorShape.PointingHandCursor)
        close_x.clicked.connect(self.reject)
        hdr_layout.addWidget(close_x)

        # Store ref & install event filter for header-only drag
        self._drag_header = hdr
        hdr.installEventFilter(self)
        root.addWidget(hdr)

        # ── Scrollable body ──
        scroll = QScrollArea(self.container)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        body_widget = QWidget()
        body_widget.setObjectName("SettingsBody")
        body_layout = QVBoxLayout(body_widget)
        body_layout.setContentsMargins(20, 18, 20, 24)
        body_layout.setSpacing(0)

        def _add_section(header_text, content_fn):
            """Helper: adds section header + content + bottom margin."""
            body_layout.addWidget(self._section_header(header_text))
            body_layout.addSpacing(8)
            result = content_fn()
            if isinstance(result, QWidget):
                body_layout.addWidget(result)
            elif result is not None:
                body_layout.addLayout(result)
            body_layout.addSpacing(16)
            body_layout.addWidget(self._divider())
            body_layout.addSpacing(16)

        # 1. Appearance — Theme
        body_layout.addWidget(self._section_header(self._t["s_appearance"]))
        body_layout.addSpacing(8)
        body_layout.addWidget(self._theme_grid())
        body_layout.addSpacing(10)

        # Custom Background (sub-section under Appearance)
        custom_bg_lbl = QLabel(self._t["s_custom_bg"])
        custom_bg_lbl.setObjectName("SubSectionLabel")
        body_layout.addWidget(custom_bg_lbl)
        body_layout.addSpacing(6)
        body_layout.addLayout(self._custom_bg_row())
        body_layout.addSpacing(16)
        body_layout.addWidget(self._divider())
        body_layout.addSpacing(16)

        # 2. Font
        _add_section(self._t["s_font"], self._font_row)

        # 3. Accessibility — Colorblind mode
        _add_section(self._t["s_accessibility"], self._colorblind_row)

        # 4. Notifications
        _add_section(self._t["s_notifications"], self._alert_hours_row)

        # 5. Alert Sound
        _add_section(self._t["s_sound"], self._sound_row)

        # 6. System — Startup (last section, no trailing divider)
        body_layout.addWidget(self._section_header(self._t["s_system"]))
        body_layout.addSpacing(8)
        body_layout.addLayout(self._startup_row())

        body_layout.addStretch()

        scroll.setWidget(body_widget)
        root.addWidget(scroll, stretch=1)

        # ── Footer buttons ──
        footer = QFrame(self.container)
        footer.setObjectName("SettingsFooter")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(16, 10, 16, 14)
        footer_layout.setSpacing(8)

        footer_layout.addStretch()

        cancel_btn = QPushButton(self._t["cancel_btn"], footer)
        cancel_btn.setObjectName("CancelBtn")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        footer_layout.addWidget(cancel_btn)

        save_btn = QPushButton(self._t["save_btn"], footer)
        save_btn.setObjectName("SaveBtn")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._on_save)
        footer_layout.addWidget(save_btn)

        root.addWidget(footer)

    # ─── Section widgets ──────────────────────────────────────────────────────

    def _section_header(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("SectionHeader")
        return lbl

    def _divider(self) -> QFrame:
        d = QFrame()
        d.setObjectName("Divider")
        d.setFrameShape(QFrame.Shape.HLine)
        return d

    def _theme_grid(self) -> QWidget:
        """Theme card grid — symmetric 2 × 2 + 1 full-width layout:
        Row 1: Midnight | Aurora
        Row 2: Crimson  | Parchment
        Row 3: Arctic  (full-width, slightly shorter — acts as a footer accent)

        Card font is hard-coded to Segoe UI so it's immune to the user's
        font selection changing the card proportions.
        """
        wrap = QWidget()
        wrap_layout = QVBoxLayout(wrap)
        wrap_layout.setContentsMargins(0, 0, 0, 0)
        wrap_layout.setSpacing(8)

        themes = list(AVAILABLE_THEMES)  # ['midnight', 'aurora', 'crimson', 'parchment', 'arctic']

        def _make_card(theme_key: str, height: int = 60) -> QPushButton:
            btn = QPushButton()
            btn.setObjectName("ThemeCard")
            btn.setCheckable(True)
            btn.setChecked(theme_key == self._theme)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(height)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            bg, accent, text_c = THEME_SWATCHES.get(theme_key, ("#161923", "#6366F1", "#F3F4F6"))
            display = THEME_DISPLAY_NAMES.get(theme_key, theme_key.capitalize())

            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg};
                    color: {text_c};
                    border: 2px solid transparent;
                    border-radius: 10px;
                    font-size: 12px;
                    font-weight: 700;
                    font-family: 'Segoe UI', sans-serif;
                    padding: 6px 8px;
                    text-align: center;
                }}
                QPushButton:hover {{
                    border: 2px solid {accent};
                }}
                QPushButton:checked {{
                    border: 2px solid {accent};
                    box-shadow: 0 0 0 3px {accent}40;
                }}
            """)
            btn.setText(display)
            btn.clicked.connect(lambda _checked, k=theme_key: self._select_theme(k))
            self._theme_btns[theme_key] = btn
            return btn

        # Row 1 — Midnight | Aurora
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        row1.addWidget(_make_card(themes[0]))  # midnight
        row1.addWidget(_make_card(themes[1]))  # aurora
        wrap_layout.addLayout(row1)

        # Row 2 — Crimson | Parchment
        row2 = QHBoxLayout()
        row2.setSpacing(8)
        row2.addWidget(_make_card(themes[2]))  # crimson
        row2.addWidget(_make_card(themes[3]))  # parchment
        wrap_layout.addLayout(row2)

        # Row 3 — Arctic full-width (shorter, acts as a wide accent strip)
        wrap_layout.addWidget(_make_card(themes[4], height=46))  # arctic

        return wrap


    def _select_theme(self, key: str):
        self._theme = key
        for k, btn in self._theme_btns.items():
            btn.setChecked(k == key)
        # Live-preview the dialog style
        self._apply_dialog_style(key, self._font)

    def _font_row(self) -> QVBoxLayout:
        outer = QVBoxLayout()
        outer.setSpacing(6)

        top = QHBoxLayout()
        top.setSpacing(10)

        lbl = QLabel(self._t["font_label"])
        lbl.setObjectName("HintLabel")
        lbl.setFixedWidth(100)
        top.addWidget(lbl)

        self.font_combo = NoScrollComboBox()
        self.font_combo.addItems(AVAILABLE_FONTS)
        if self._font in AVAILABLE_FONTS:
            self.font_combo.setCurrentText(self._font)
        self.font_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.font_combo.currentTextChanged.connect(self._on_font_changed)
        top.addWidget(self.font_combo, stretch=1)
        outer.addLayout(top)

        # Live preview box — font is applied to sample text only
        self.font_preview = QLabel("AaBbCc  Gg Qq  0123  Hello, World!")
        self.font_preview.setObjectName("FontPreviewLabel")
        self.font_preview.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        outer.addWidget(self.font_preview)
        self._update_font_preview(self._font)

        return outer

    def _on_font_changed(self, font_name: str):
        self._font = font_name
        self._update_font_preview(font_name)
        self._apply_dialog_style(self._theme, font_name)

    def _update_font_preview(self, font_name: str):
        f = QFont(font_name, 12)
        self.font_preview.setFont(f)
        # Only show sample glyphs — name is already visible in the combo
        self.font_preview.setText("AaBbCc  Gg Qq  0123  Hello, World!")

    def _custom_bg_row(self) -> QVBoxLayout:
        outer = QVBoxLayout()
        outer.setSpacing(6)

        path_row = QHBoxLayout()
        path_row.setSpacing(6)

        self.bg_path_edit = QLineEdit()
        self.bg_path_edit.setObjectName("SoundPathEdit")
        self.bg_path_edit.setReadOnly(True)
        self.bg_path_edit.setPlaceholderText(self._t["bg_placeholder"])
        if self._custom_bg:
            import os as _os
            self.bg_path_edit.setText(_os.path.basename(self._custom_bg))
        path_row.addWidget(self.bg_path_edit, stretch=1)

        btn = QPushButton(self._t["bg_upload_btn"])
        btn.setObjectName("BrowseBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._upload_custom_bg)
        path_row.addWidget(btn)

        clear_btn = QPushButton(self._t["bg_clear_btn"])
        clear_btn.setObjectName("ClearBtn")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self._clear_custom_bg)
        path_row.addWidget(clear_btn)

        outer.addLayout(path_row)

        hint = QLabel(self._t["bg_hint"])
        hint.setObjectName("HintLabel")
        hint.setWordWrap(True)
        outer.addWidget(hint)

        return outer

    def _upload_custom_bg(self):
        path, _ = QFileDialog.getOpenFileName(
            self, self._t["bg_dialog_title"],
            os.path.expanduser("~"),
            "Images (*.png *.jpg *.jpeg)"
        )
        if path:
            from ui.crop_dialog import CropDialog
            dialog = CropDialog(path, parent=self)
            if dialog.exec():
                app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                save_path = os.path.join(app_dir, "custom_bg.png")
                dialog.cropped_pixmap.save(save_path)
                self._custom_bg = save_path
                self.bg_path_edit.setText(os.path.basename(save_path))
                self._apply_dialog_style(self._theme, self._font)

    def _clear_custom_bg(self):
        self._custom_bg = ""
        self.bg_path_edit.clear()
        self.bg_path_edit.setPlaceholderText(self._t["bg_placeholder"])

    def _colorblind_row(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(6)

        hint = QLabel(self._t["cb_hint"])
        hint.setObjectName("HintLabel")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        radio_layout = QHBoxLayout()
        radio_layout.setSpacing(14)
        group = QButtonGroup(self)

        # Map mode keys to localized display names from self._t
        cb_labels = {
            "normal":       self._t["cb_normal"],
            "deuteranopia": self._t["cb_deuteranopia"],
            "protanopia":   self._t["cb_protanopia"],
        }
        for mode, display in cb_labels.items():
            rb = QRadioButton(display)
            rb.setCursor(Qt.CursorShape.PointingHandCursor)
            rb.setChecked(mode == self._colorblind)
            rb.toggled.connect(lambda checked, m=mode: self._on_colorblind(m, checked))
            group.addButton(rb)
            radio_layout.addWidget(rb)
            self._colorblind_radios[mode] = rb

        radio_layout.addStretch()
        layout.addLayout(radio_layout)
        return layout

    def _on_colorblind(self, mode: str, checked: bool):
        if checked:
            self._colorblind = mode

    def _alert_hours_row(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(6)

        hint = QLabel(self._t["notif_hint"])
        hint.setObjectName("HintLabel")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        row = QHBoxLayout()
        row.setSpacing(8)

        self.alert_spin = QSpinBox()
        self.alert_spin.setMinimum(1)
        self.alert_spin.setMaximum(48)
        self.alert_spin.setValue(self._alert_hours)
        self.alert_spin.setFixedWidth(80)
        row.addWidget(self.alert_spin)

        suffix = QLabel(self._t["notif_suffix"])
        suffix.setObjectName("SpinSuffix")
        row.addWidget(suffix)
        row.addStretch()

        layout.addLayout(row)
        return layout

    def _sound_row(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(6)

        hint = QLabel(self._t["sound_hint"])
        hint.setObjectName("HintLabel")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        row = QHBoxLayout()
        row.setSpacing(6)

        self.sound_path_edit = QLineEdit()
        self.sound_path_edit.setObjectName("SoundPathEdit")
        self.sound_path_edit.setReadOnly(True)
        if self._sound_path:
            self.sound_path_edit.setText(self._sound_path)
        else:
            self.sound_path_edit.setPlaceholderText(self._t["sound_no_file"])
        row.addWidget(self.sound_path_edit, stretch=1)

        browse_btn = QPushButton(self._t["sound_browse_btn"])
        browse_btn.setObjectName("BrowseBtn")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.clicked.connect(self._browse_sound)
        row.addWidget(browse_btn)

        clear_btn = QPushButton(self._t["sound_clear_btn"])
        clear_btn.setObjectName("ClearBtn")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self._clear_sound)
        row.addWidget(clear_btn)

        layout.addLayout(row)
        return layout

    def _browse_sound(self):
        path, _ = QFileDialog.getOpenFileName(
            self, self._t["sound_dialog_title"],
            os.path.expanduser("~"),
            "Audio Files (*.mp3 *.wav)"
        )
        if path:
            self._sound_path = path
            self.sound_path_edit.setText(path)

    def _clear_sound(self):
        self._sound_path = ""
        self.sound_path_edit.clear()
        self.sound_path_edit.setPlaceholderText(self._t["sound_no_file"])

    def _startup_row(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(4)

        self.startup_check = QCheckBox(self._t["startup_check"])
        self.startup_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.startup_check.setChecked(self._startup)
        layout.addWidget(self.startup_check)

        hint = QLabel(self._t["startup_hint"])
        hint.setObjectName("HintLabel")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        return layout

    # ─── Drag via Header Event Filter ────────────────────────────────────────

    def eventFilter(self, obj, event):
        """Intercepts mouse events on the header frame to enable drag-to-move."""
        if obj is self._drag_header:
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                    event.accept()
                    return True
            elif event.type() == QEvent.Type.MouseMove:
                if event.buttons() & Qt.MouseButton.LeftButton and self._drag_pos is not None:
                    self.move(event.globalPosition().toPoint() - self._drag_pos)
                    event.accept()
                    return True
            elif event.type() == QEvent.Type.MouseButtonRelease:
                self._drag_pos = None
                event.accept()
                return True
        return super().eventFilter(obj, event)

    def _on_save(self):
        """Persists all settings and emits settings_saved signal."""
        sm = self.settings_manager
        sm.set_theme(self._theme)
        sm.set_font(self._font)
        sm.set_custom_bg(self._custom_bg)
        sm.set_deadline_alert_hours(self.alert_spin.value())
        sm.set_startup(self.startup_check.isChecked())
        sm.set_alert_sound(self._sound_path)
        sm.set_colorblind_mode(self._colorblind)
        self.settings_saved.emit()
        self.accept()

    # ─── Style ────────────────────────────────────────────────────────────────

    def _apply_dialog_style(self, theme: str, font: str):
        """Rebuilds dialog stylesheet for the selected theme and font."""
        tokens = _DIALOG_TOKENS.get(theme, _DIALOG_TOKENS["midnight"]).copy()
        tokens["font"] = font

        # Container background
        css = _DIALOG_STYLE.format(**tokens)

        # Extra styles for header elements (can't use named objects in template easily)
        extra = f"""
        #SettingsContainer {{
            background-color: {tokens['bg']};
            border: 1px solid {tokens['border']};
            border-radius: 14px;
        }}
        #SettingsHeader {{
            background-color: {tokens['bg']};
            border-top-left-radius: 14px;
            border-top-right-radius: 14px;
            border-bottom: 1px solid {tokens['divider']};
        }}
        #SettingsTitle {{
            color: {tokens['text']};
            font-size: 14px;
            font-weight: bold;
            font-family: '{font}', 'Segoe UI', sans-serif;
        }}
        #SettingsCloseBtn {{
            background-color: transparent;
            color: {tokens['text_muted']};
            border: none;
            border-radius: 6px;
            font-size: 13px;
            font-weight: bold;
            min-width: 24px;
            min-height: 24px;
            padding: 2px 6px;
        }}
        #SettingsCloseBtn:hover {{
            background-color: #EF4444;
            color: #FFFFFF;
        }}
        #SettingsFooter {{
            background-color: {tokens['bg']};
            border-top: 1px solid {tokens['divider']};
            border-bottom-left-radius: 14px;
            border-bottom-right-radius: 14px;
        }}
        #SettingsBody {{
            background: transparent;
        }}
        QScrollBar:vertical {{
            background: transparent;
            width: 6px;
        }}
        QScrollBar::handle:vertical {{
            background: {tokens['check_border']};
            border-radius: 3px;
            min-height: 20px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        """
        self.setStyleSheet(css + extra)
