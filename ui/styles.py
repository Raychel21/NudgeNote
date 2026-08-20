# ─────────────────────────────────────────────────────────────────────────────
# NudgeNote — Themes & Style System
# 5 themes: midnight, aurora, crimson, parchment, arctic
# + Colorblind filter overlay (deuteranopia / protanopia)
# ─────────────────────────────────────────────────────────────────────────────

# ── Shared structural CSS (injected per-theme via format) ─────────────────────
_BASE_TEMPLATE = """
/* ═══════════════════════════════════════════════════════════
   NudgeNote — Theme: {theme_name}
   ═══════════════════════════════════════════════════════════ */

/* Main Frameless Overlay Container */
#OverlayContainer {{
    {bg_property}
    border: 1px solid {border_main};
    border-radius: 16px;
}}

/* Header Title Bar */
#HeaderFrame {{
    background-color: {bg_header};
    border-top-left-radius: 16px;
    border-top-right-radius: 16px;
    border-bottom: 1px solid {border_header};
    padding: 6px 10px;
}}

#AppTitle {{
    color: {text_primary};
    font-size: 14px;
    font-weight: bold;
    font-family: '{font}', 'Segoe UI', sans-serif;
}}

/* Header Buttons (Language & Settings) */
#LangToggleBtn, #SettingsBtn {{
    background-color: {btn_bg};
    color: {btn_fg};
    border: 1px solid {btn_border};
    border-radius: 6px;
    font-size: 12px;
    font-weight: bold;
    padding: 3px 8px;
    min-height: 22px;
}}

#LangToggleBtn:hover, #SettingsBtn:hover {{
    background-color: {btn_bg_hover};
    color: {btn_fg_hover};
    border-color: {accent};
}}

/* Window Control Buttons */
.WindowBtn {{
    background-color: transparent;
    color: {text_muted};
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
    min-width: 24px;
    min-height: 24px;
}}

.WindowBtn:hover {{
    background-color: {wbtn_hover};
    color: {text_primary};
}}

#CloseBtn:hover {{
    background-color: #EF4444;
    color: #FFFFFF;
}}

/* Input Controls */
QLineEdit, QComboBox, QDateEdit {{
    background-color: {input_bg};
    border: 1px solid {input_border};
    border-radius: 8px;
    color: {text_primary};
    padding: 5px 8px;
    font-size: 12px;
    font-family: '{font}', 'Segoe UI', sans-serif;
}}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus {{
    border: 1px solid {accent};
    background-color: {input_bg_focus};
}}

/* Time plain-text input */
#TimeInput {{
    background-color: {input_bg};
    border: 1px solid {input_border};
    border-radius: 8px;
    color: {text_primary};
    padding: 5px 4px;
    font-size: 12px;
    font-family: '{font}', 'Segoe UI', sans-serif;
    text-align: center;
    min-width: 60px;
    max-width: 80px;
}}

#TimeInput:focus {{
    border: 1px solid {accent};
    background-color: {input_bg_focus};
}}

/* Dropdown Popup */
QComboBox QAbstractItemView {{
    background-color: {popup_bg};
    border: 1px solid {border_main};
    selection-background-color: {accent};
    color: {text_primary};
    border-radius: 6px;
}}

/* Add Task Button */
#AddTaskBtn {{
    background-color: {accent};
    color: #FFFFFF;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
    font-family: '{font}', 'Segoe UI', sans-serif;
}}

#AddTaskBtn:hover {{
    background-color: {accent_hover};
}}

#AddTaskBtn:pressed {{
    background-color: {accent_press};
}}

/* Sort & Year Controls */
#SortLabel, #YearLabel {{
    color: {text_muted};
    font-size: 11px;
    font-weight: 600;
    font-family: '{font}', 'Segoe UI', sans-serif;
}}

#SortCombo, #YearCombo {{
    background-color: {input_bg};
    border: 1px solid {input_border};
    border-radius: 6px;
    color: {text_primary};
    padding: 2px 6px;
    font-size: 11px;
    font-family: '{font}', 'Segoe UI', sans-serif;
}}

/* Task Item Container */
#TaskItemWidget {{
    background-color: {card_bg};
    border: 1px solid {card_border};
    border-radius: 10px;
}}

#TaskItemWidget:hover {{
    background-color: {card_bg_hover};
    border: 1px solid {accent_soft};
}}

/* Checkbox */
QCheckBox {{
    color: {text_primary};
    font-size: 13px;
    font-family: '{font}', 'Segoe UI', sans-serif;
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 2px solid {check_border};
    background-color: {check_bg};
}}

QCheckBox::indicator:hover {{
    border-color: {accent};
}}

QCheckBox::indicator:checked {{
    background-color: {check_done};
    border-color: {check_done};
}}

/* Priority Badges */
#BadgeHigh {{
    background-color: {badge_high};
    color: #FFFFFF;
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 10px;
    font-weight: bold;
    font-family: '{font}', 'Segoe UI', sans-serif;
}}

#BadgeMed {{
    background-color: {badge_med};
    color: #FFFFFF;
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 10px;
    font-weight: bold;
    font-family: '{font}', 'Segoe UI', sans-serif;
}}

#BadgeLow {{
    background-color: {badge_low};
    color: #FFFFFF;
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 10px;
    font-weight: bold;
    font-family: '{font}', 'Segoe UI', sans-serif;
}}

/* Deadline Button & Label */
#DeadlineBtn {{
    background-color: {deadline_btn_bg};
    border: 1px solid {input_border};
    border-radius: 5px;
    font-size: 12px;
    padding: 2px 6px;
    min-width: 22px;
    min-height: 20px;
}}

#DeadlineBtn:hover {{
    background-color: {accent_soft};
    border-color: {accent};
}}

#DeadlineLabel {{
    color: {text_muted};
    font-size: 11px;
    font-family: '{font}', 'Segoe UI', sans-serif;
    background-color: {deadline_label_bg};
    padding: 2px 6px;
    border-radius: 4px;
}}

/* Delete Button */
#DeleteBtn {{
    background-color: transparent;
    color: {text_muted};
    border: none;
    border-radius: 6px;
    font-weight: bold;
    font-size: 14px;
    min-width: 24px;
    min-height: 24px;
}}

#DeleteBtn:hover {{
    background-color: {delete_hover_bg};
    color: #EF4444;
}}

/* Date Header Separator — pill badge always readable over wallpaper */
#DateHeader {{
    color: {date_header_color};
    font-size: 9px;
    font-weight: 700;
    font-family: '{font}', 'Segoe UI', sans-serif;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 3px 10px 3px 8px;
    background: rgba(0, 0, 0, 0.52);
    border: 1px solid {date_header_border};
    border-radius: 6px;
    margin: 2px 0px 1px 0px;
}}

/* Month Filter Bar — dark strip so labels are always legible over wallpaper */
#MonthBarRow {{
    background: rgba(0, 0, 0, 0.48);
    border-radius: 8px;
    padding: 3px 4px;
}}

/* Month Filter Buttons */
#MonthFilterBtn {{
    background: rgba(255, 255, 255, 0.10);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 4px;
    font-size: 9px;
    font-weight: 700;
    font-family: '{font}', 'Segoe UI', sans-serif;
    padding: 2px 1px;
    min-width: 30px;
    max-width: 36px;
}}

#MonthFilterBtn:hover {{
    background: {month_btn_hover};
    color: {accent_text};
    border-color: {accent_soft};
}}

#MonthFilterBtn:checked {{
    background: {accent};
    color: #FFFFFF;
    border-color: {accent};
}}

/* Time Label */
#TimeLabel {{
    color: {time_label_fg};
    font-size: 11px;
    font-family: '{font}', 'Segoe UI', sans-serif;
    background: {time_label_bg};
    border: 1px solid {time_label_border};
    border-radius: 5px;
    padding: 2px 6px;
    min-width: 46px;
}}

/* ScrollArea */
QScrollArea {{
    background: transparent;
    border: none;
}}

QScrollArea > QWidget > QWidget {{
    background: transparent;
    max-width: 9999px;
}}

#TaskListContainer {{
    background: transparent;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: {scrollbar_handle};
    border-radius: 3px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: {scrollbar_handle_hover};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* Hide horizontal scrollbar entirely */
QScrollBar:horizontal {{
    height: 0px;
    background: transparent;
}}


/* Calendar Widget */
QCalendarWidget QWidget#qt_calendar_navigationbar {{
    background-color: {bg_header};
}}

QCalendarWidget QAbstractItemView:enabled {{
    background-color: {bg_base};
    color: {text_primary};
    selection-background-color: {accent};
    selection-color: #FFFFFF;
}}
"""

# ─────────────────────────────────────────────────────────────────────────────
# Theme Token Definitions
# ─────────────────────────────────────────────────────────────────────────────

THEMES = {

    # ── 1. MIDNIGHT — Deep navy/indigo dark ──────────────────────────────────
    "midnight": {
        "theme_name": "Midnight",
        "font": "{font}",
        "bg_base":           "#161923",
        "bg_header":         "#1E2230",
        "border_main":       "rgba(255,255,255,0.15)",
        "border_header":     "rgba(255,255,255,0.08)",
        "text_primary":      "#F3F4F6",
        "text_muted":        "#9CA3AF",
        "accent":            "#6366F1",
        "accent_hover":      "#4F46E5",
        "accent_press":      "#4338CA",
        "accent_soft":       "rgba(99,102,241,0.4)",
        "accent_text":       "#A5B4FC",
        "btn_bg":            "rgba(99,102,241,0.2)",
        "btn_fg":            "#A5B4FC",
        "btn_border":        "rgba(99,102,241,0.4)",
        "btn_bg_hover":      "rgba(99,102,241,0.4)",
        "btn_fg_hover":      "#FFFFFF",
        "wbtn_hover":        "rgba(255,255,255,0.12)",
        "input_bg":          "#232838",
        "input_bg_focus":    "#282D41",
        "input_border":      "rgba(255,255,255,0.12)",
        "popup_bg":          "#1E2230",
        "card_bg":           "#202534",
        "card_border":       "rgba(255,255,255,0.08)",
        "card_bg_hover":     "#282E40",
        "check_border":      "#6B7280",
        "check_bg":          "transparent",
        "check_done":        "#10B981",
        "badge_high":        "#EF4444",
        "badge_med":         "#F59E0B",
        "badge_low":         "#10B981",
        "deadline_btn_bg":   "rgba(255,255,255,0.06)",
        "deadline_label_bg": "rgba(0,0,0,0.2)",
        "delete_hover_bg":   "rgba(239,68,68,0.2)",
        "date_header_color": "#6B7DBF",
        "date_header_border":"rgba(99,102,241,0.15)",
        "month_btn_bg":      "rgba(255,255,255,0.05)",
        "month_btn_border":  "rgba(255,255,255,0.07)",
        "month_btn_hover":   "rgba(99,102,241,0.18)",
        "time_label_fg":     "#8B9CC8",
        "time_label_bg":     "rgba(99,102,241,0.1)",
        "time_label_border": "rgba(99,102,241,0.25)",
        "scrollbar_handle":  "rgba(255,255,255,0.2)",
        "scrollbar_handle_hover": "rgba(255,255,255,0.4)",
    },

    # ── 2. AURORA — Dark teal/emerald neon ──────────────────────────────────
    "aurora": {
        "theme_name": "Aurora",
        "font": "{font}",
        "bg_base":           "#0D1F1A",
        "bg_header":         "#132920",
        "border_main":       "rgba(16,185,129,0.2)",
        "border_header":     "rgba(16,185,129,0.1)",
        "text_primary":      "#ECFDF5",
        "text_muted":        "#6EE7B7",
        "accent":            "#10B981",
        "accent_hover":      "#059669",
        "accent_press":      "#047857",
        "accent_soft":       "rgba(16,185,129,0.35)",
        "accent_text":       "#6EE7B7",
        "btn_bg":            "rgba(16,185,129,0.15)",
        "btn_fg":            "#6EE7B7",
        "btn_border":        "rgba(16,185,129,0.35)",
        "btn_bg_hover":      "rgba(16,185,129,0.3)",
        "btn_fg_hover":      "#FFFFFF",
        "wbtn_hover":        "rgba(255,255,255,0.1)",
        "input_bg":          "#1A2E27",
        "input_bg_focus":    "#1F3830",
        "input_border":      "rgba(16,185,129,0.18)",
        "popup_bg":          "#132920",
        "card_bg":           "#172820",
        "card_border":       "rgba(16,185,129,0.1)",
        "card_bg_hover":     "#1E3429",
        "check_border":      "#4B9E82",
        "check_bg":          "transparent",
        "check_done":        "#10B981",
        "badge_high":        "#EF4444",
        "badge_med":         "#F59E0B",
        "badge_low":         "#10B981",
        "deadline_btn_bg":   "rgba(16,185,129,0.08)",
        "deadline_label_bg": "rgba(0,0,0,0.25)",
        "delete_hover_bg":   "rgba(239,68,68,0.18)",
        "date_header_color": "#34D399",
        "date_header_border":"rgba(16,185,129,0.2)",
        "month_btn_bg":      "rgba(16,185,129,0.06)",
        "month_btn_border":  "rgba(16,185,129,0.1)",
        "month_btn_hover":   "rgba(16,185,129,0.2)",
        "time_label_fg":     "#6EE7B7",
        "time_label_bg":     "rgba(16,185,129,0.1)",
        "time_label_border": "rgba(16,185,129,0.3)",
        "scrollbar_handle":  "rgba(16,185,129,0.25)",
        "scrollbar_handle_hover": "rgba(16,185,129,0.5)",
    },

    # ── 3. CRIMSON — Dark rose/red deep ─────────────────────────────────────
    "crimson": {
        "theme_name": "Crimson",
        "font": "{font}",
        "bg_base":           "#1A0D10",
        "bg_header":         "#221218",
        "border_main":       "rgba(239,68,68,0.2)",
        "border_header":     "rgba(239,68,68,0.1)",
        "text_primary":      "#FFF1F2",
        "text_muted":        "#FCA5A5",
        "accent":            "#E11D48",
        "accent_hover":      "#BE123C",
        "accent_press":      "#9F1239",
        "accent_soft":       "rgba(225,29,72,0.35)",
        "accent_text":       "#FCA5A5",
        "btn_bg":            "rgba(225,29,72,0.15)",
        "btn_fg":            "#FCA5A5",
        "btn_border":        "rgba(225,29,72,0.35)",
        "btn_bg_hover":      "rgba(225,29,72,0.3)",
        "btn_fg_hover":      "#FFFFFF",
        "wbtn_hover":        "rgba(255,255,255,0.1)",
        "input_bg":          "#271318",
        "input_bg_focus":    "#301620",
        "input_border":      "rgba(225,29,72,0.18)",
        "popup_bg":          "#221218",
        "card_bg":           "#211016",
        "card_border":       "rgba(225,29,72,0.1)",
        "card_bg_hover":     "#2A141C",
        "check_border":      "#9B4258",
        "check_bg":          "transparent",
        "check_done":        "#10B981",
        "badge_high":        "#EF4444",
        "badge_med":         "#F59E0B",
        "badge_low":         "#10B981",
        "deadline_btn_bg":   "rgba(225,29,72,0.08)",
        "deadline_label_bg": "rgba(0,0,0,0.25)",
        "delete_hover_bg":   "rgba(239,68,68,0.2)",
        "date_header_color": "#FB7185",
        "date_header_border":"rgba(225,29,72,0.2)",
        "month_btn_bg":      "rgba(225,29,72,0.06)",
        "month_btn_border":  "rgba(225,29,72,0.1)",
        "month_btn_hover":   "rgba(225,29,72,0.2)",
        "time_label_fg":     "#FCA5A5",
        "time_label_bg":     "rgba(225,29,72,0.1)",
        "time_label_border": "rgba(225,29,72,0.3)",
        "scrollbar_handle":  "rgba(225,29,72,0.25)",
        "scrollbar_handle_hover": "rgba(225,29,72,0.5)",
    },

    # ── 4. PARCHMENT — Warm cream light ─────────────────────────────────────
    "parchment": {
        "theme_name": "Parchment",
        "font": "{font}",
        "bg_base":           "#FAF7F2",
        "bg_header":         "#FFFFFF",
        "border_main":       "#E8DFD0",
        "border_header":     "#EDE4D6",
        "text_primary":      "#2D1F0E",
        "text_muted":        "#8B6F4E",
        "accent":            "#B45309",
        "accent_hover":      "#92400E",
        "accent_press":      "#78350F",
        "accent_soft":       "rgba(180,83,9,0.2)",
        "accent_text":       "#B45309",
        "btn_bg":            "#F0E8DC",
        "btn_fg":            "#7C4A1E",
        "btn_border":        "#D4B896",
        "btn_bg_hover":      "#E4D5C0",
        "btn_fg_hover":      "#2D1F0E",
        "wbtn_hover":        "#EDE4D6",
        "input_bg":          "#FFFFFF",
        "input_bg_focus":    "#FFFCF8",
        "input_border":      "#D4B896",
        "popup_bg":          "#FFFFFF",
        "card_bg":           "#FFFFFF",
        "card_border":       "#E8DFD0",
        "card_bg_hover":     "#FDF5EB",
        "check_border":      "#C4A882",
        "check_bg":          "#FFFFFF",
        "check_done":        "#10B981",
        "badge_high":        "#DC2626",
        "badge_med":         "#D97706",
        "badge_low":         "#059669",
        "deadline_btn_bg":   "#F0E8DC",
        "deadline_label_bg": "#F5EDE0",
        "delete_hover_bg":   "#FEE2E2",
        "date_header_color": "#B45309",
        "date_header_border":"rgba(180,83,9,0.2)",
        "month_btn_bg":      "#F0E8DC",
        "month_btn_border":  "#DDD0BE",
        "month_btn_hover":   "#FDEBD0",
        "time_label_fg":     "#8B6F4E",
        "time_label_bg":     "#FDE8C8",
        "time_label_border": "#D4B896",
        "scrollbar_handle":  "#C4A882",
        "scrollbar_handle_hover": "#A0856A",
    },

    # ── 5. ARCTIC — Cool slate/blue light ───────────────────────────────────
    "arctic": {
        "theme_name": "Arctic",
        "font": "{font}",
        "bg_base":           "#F0F5FB",
        "bg_header":         "#FFFFFF",
        "border_main":       "#C9DAEA",
        "border_header":     "#DCE8F5",
        "text_primary":      "#0F2D4A",
        "text_muted":        "#4A7499",
        "accent":            "#0284C7",
        "accent_hover":      "#0369A1",
        "accent_press":      "#075985",
        "accent_soft":       "rgba(2,132,199,0.2)",
        "accent_text":       "#0284C7",
        "btn_bg":            "#E0EEF8",
        "btn_fg":            "#0C4A6E",
        "btn_border":        "#BAD7ED",
        "btn_bg_hover":      "#CFE4F5",
        "btn_fg_hover":      "#0F2D4A",
        "wbtn_hover":        "#DCE8F5",
        "input_bg":          "#FFFFFF",
        "input_bg_focus":    "#F8FBFF",
        "input_border":      "#BAD7ED",
        "popup_bg":          "#FFFFFF",
        "card_bg":           "#FFFFFF",
        "card_border":       "#D0E5F5",
        "card_bg_hover":     "#EAF4FC",
        "check_border":      "#7BB3D0",
        "check_bg":          "#FFFFFF",
        "check_done":        "#0D9488",
        "badge_high":        "#DC2626",
        "badge_med":         "#D97706",
        "badge_low":         "#0D9488",
        "deadline_btn_bg":   "#E0EEF8",
        "deadline_label_bg": "#EAF4FC",
        "delete_hover_bg":   "#FEE2E2",
        "date_header_color": "#0284C7",
        "date_header_border":"rgba(2,132,199,0.2)",
        "month_btn_bg":      "#E0EEF8",
        "month_btn_border":  "#BAD7ED",
        "month_btn_hover":   "#D0E8F8",
        "time_label_fg":     "#4A7499",
        "time_label_bg":     "#DBEEFF",
        "time_label_border": "#BAD7ED",
        "scrollbar_handle":  "#7BB3D0",
        "scrollbar_handle_hover": "#4A7499",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Colorblind filter — overrides specific color tokens
# Applied on top of the theme, not replacing it wholesale
# ─────────────────────────────────────────────────────────────────────────────

# Deuteranopia: red-green deficiency (most common) — shift red→orange, green→blue-ish
_DEUTERANOPIA_OVERRIDES = {
    "badge_high":  "#D97706",   # orange instead of red
    "badge_low":   "#0284C7",   # blue instead of green
    "check_done":  "#0284C7",   # blue checkmark
    "accent":      "#7C3AED",   # violet accent (safe for D)
    "accent_hover":"#6D28D9",
    "accent_press":"#5B21B6",
}

# Protanopia: red weakness (red appears very dark) — replace reds with amber/blue
_PROTANOPIA_OVERRIDES = {
    "badge_high":  "#B45309",   # amber-brown instead of red
    "badge_low":   "#0369A1",   # deep blue instead of green
    "check_done":  "#0369A1",   # blue checkmark
    "accent":      "#7C3AED",   # violet accent (safe for P)
    "accent_hover":"#6D28D9",
    "accent_press":"#5B21B6",
}

COLORBLIND_OVERRIDES = {
    "normal":       {},
    "deuteranopia": _DEUTERANOPIA_OVERRIDES,
    "protanopia":   _PROTANOPIA_OVERRIDES,
}

AVAILABLE_THEMES = list(THEMES.keys())

AVAILABLE_FONTS = [
    "Segoe UI",
    "Comic Sans MS",
    "Trebuchet MS",
    "Consolas",
    "Georgia",
]

THEME_DISPLAY_NAMES = {
    "midnight":  "🌌 Midnight",
    "aurora":    "🌿 Aurora",
    "crimson":   "🌹 Crimson",
    "parchment": "📜 Parchment",
    "arctic":    "❄️ Arctic",
}

COLORBLIND_DISPLAY_NAMES = {
    "normal":       "Normal",
    "deuteranopia": "Deuteranopia (Red-Green)",
    "protanopia":   "Protanopia (Red Weak)",
}


def get_style(theme: str, font: str = "Segoe UI", colorblind_mode: str = "normal", custom_bg: str = "") -> str:
    """
    Returns the complete stylesheet for the given theme, font, and colorblind mode.

    Args:
        theme: One of 'midnight', 'aurora', 'crimson', 'parchment', 'arctic'.
               Legacy 'dark'/'light' values are auto-migrated.
        font: Font family name from AVAILABLE_FONTS.
        colorblind_mode: 'normal', 'deuteranopia', or 'protanopia'.
        custom_bg: Path to a background image, or empty string.
    """
    # Migrate legacy theme names
    if theme == "dark":
        theme = "midnight"
    elif theme == "light":
        theme = "parchment"

    tokens = THEMES.get(theme, THEMES["midnight"]).copy()

    # Apply colorblind overrides on top of base tokens
    overrides = COLORBLIND_OVERRIDES.get(colorblind_mode, {})
    tokens.update(overrides)

    # Inject font everywhere the template uses {font}
    # (token "font" itself contains {font} as a placeholder — replace with actual font)
    tokens["font"] = font

    if custom_bg:
        bg_url = custom_bg.replace('\\', '/')
        tokens["bg_property"] = f"border-image: url('{bg_url}') 0 0 0 0 stretch stretch;"
    else:
        tokens["bg_property"] = f"background-color: {tokens['bg_base']};"

    return _BASE_TEMPLATE.format(**tokens)


# Legacy alias kept for any imports that reference MAIN_STYLE directly
MAIN_STYLE = get_style("midnight")
