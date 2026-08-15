DARK_STYLE = """
/* Main Frameless Overlay Window Styling (Dark Mode) */
#OverlayContainer {
    background-color: #161923;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px;
}

/* Header Title Bar */
#HeaderFrame {
    background-color: #1E2230;
    border-top-left-radius: 16px;
    border-top-right-radius: 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding: 6px 10px;
}

#AppTitle {
    color: #F3F4F6;
    font-size: 14px;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
}

/* Header Buttons (Language & Theme Toggle) */
#LangToggleBtn, #ThemeToggleBtn {
    background-color: rgba(99, 102, 241, 0.2);
    color: #A5B4FC;
    border: 1px solid rgba(99, 102, 241, 0.4);
    border-radius: 6px;
    font-size: 12px;
    font-weight: bold;
    padding: 3px 8px;
    min-height: 22px;
}

#LangToggleBtn:hover, #ThemeToggleBtn:hover {
    background-color: rgba(99, 102, 241, 0.4);
    color: #FFFFFF;
    border-color: #6366F1;
}

/* Window Control Buttons */
.WindowBtn {
    background-color: transparent;
    color: #9CA3AF;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
    min-width: 24px;
    min-height: 24px;
}

.WindowBtn:hover {
    background-color: rgba(255, 255, 255, 0.12);
    color: #FFFFFF;
}

#CloseBtn:hover {
    background-color: #EF4444;
    color: #FFFFFF;
}

/* Input Controls */
QLineEdit, QComboBox, QDateEdit {
    background-color: #232838;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    color: #F9FAFB;
    padding: 5px 8px;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 1px solid #6366F1;
    background-color: #282D41;
}

/* Time plain-text input (no spin arrows) */
#TimeInput {
    background-color: #232838;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    color: #F9FAFB;
    padding: 5px 4px;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
    text-align: center;
    min-width: 60px;
    max-width: 80px;
}

#TimeInput:focus {
    border: 1px solid #6366F1;
    background-color: #282D41;
}

/* Dropdown QComboBox Popup */
QComboBox QAbstractItemView {
    background-color: #1E2230;
    border: 1px solid rgba(255, 255, 255, 0.15);
    selection-background-color: #4F46E5;
    color: #F9FAFB;
    border-radius: 6px;
}

/* Add Task Button */
#AddTaskBtn {
    background-color: #6366F1;
    color: #FFFFFF;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
}

#AddTaskBtn:hover {
    background-color: #4F46E5;
}

#AddTaskBtn:pressed {
    background-color: #4338CA;
}

/* Sort & Year Controls */
#SortLabel, #YearLabel {
    color: #9CA3AF;
    font-size: 11px;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
}

#SortCombo, #YearCombo {
    background-color: #232838;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    color: #F9FAFB;
    padding: 2px 6px;
    font-size: 11px;
    font-family: 'Segoe UI', sans-serif;
}

/* Task Item Container */
#TaskItemWidget {
    background-color: #202534;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
}

#TaskItemWidget:hover {
    background-color: #282E40;
    border: 1px solid rgba(99, 102, 241, 0.4);
}

/* Checkbox */
QCheckBox {
    color: #F3F4F6;
    font-size: 13px;
    font-family: 'Segoe UI', sans-serif;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 2px solid #6B7280;
    background-color: transparent;
}

QCheckBox::indicator:hover {
    border-color: #6366F1;
}

QCheckBox::indicator:checked {
    background-color: #10B981;
    border-color: #10B981;
}

/* Priority Badges with Solid Background & Soft Rounded Curves */
#BadgeHigh {
    background-color: #EF4444;
    color: #FFFFFF;
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 10px;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
}

#BadgeMed {
    background-color: #F59E0B;
    color: #FFFFFF;
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 10px;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
}

#BadgeLow {
    background-color: #10B981;
    color: #FFFFFF;
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 10px;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
}

/* Deadline Button & Label */
#DeadlineBtn {
    background-color: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 5px;
    font-size: 12px;
    padding: 2px 6px;
    min-width: 22px;
    min-height: 20px;
}

#DeadlineBtn:hover {
    background-color: rgba(99, 102, 241, 0.25);
    border-color: #6366F1;
}

#DeadlineLabel {
    color: #9CA3AF;
    font-size: 11px;
    font-family: 'Segoe UI', sans-serif;
    background-color: rgba(0, 0, 0, 0.2);
    padding: 2px 6px;
    border-radius: 4px;
}

/* Delete Button */
#DeleteBtn {
    background-color: transparent;
    color: #6B7280;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    font-size: 14px;
    min-width: 24px;
    min-height: 24px;
}

#DeleteBtn:hover {
    background-color: rgba(239, 68, 68, 0.2);
    color: #EF4444;
}

/* Date Header Separator — slim and understated */
#DateHeader {
    color: #6B7DBF;
    font-size: 9px;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    padding: 3px 2px 1px 2px;
    border-bottom: 1px solid rgba(99, 102, 241, 0.15);
    background: transparent;
}

/* Month Filter Buttons */
#MonthFilterBtn {
    background: rgba(255, 255, 255, 0.05);
    color: #6B7280;
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 4px;
    font-size: 9px;
    font-weight: 700;
    font-family: 'Segoe UI', sans-serif;
    padding: 2px 1px;
    min-width: 30px;
    max-width: 36px;
}

#MonthFilterBtn:hover {
    background: rgba(99, 102, 241, 0.18);
    color: #A5B4FC;
    border-color: rgba(99, 102, 241, 0.35);
}

#MonthFilterBtn:checked {
    background: #6366F1;
    color: #FFFFFF;
    border-color: #6366F1;
}
#TimeLabel {
    color: #8B9CC8;
    font-size: 11px;
    font-family: 'Segoe UI', sans-serif;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 5px;
    padding: 2px 6px;
    min-width: 46px;
}

/* ScrollArea & Scroll List Background Fix */
QScrollArea {
    background: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}

#TaskListContainer {
    background: transparent;
}

QScrollBar:vertical {
    background: transparent;
    width: 6px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(255, 255, 255, 0.4);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Calendar Widget Dark Popup Styling */
QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #1E2230;
}
QCalendarWidget QAbstractItemView:enabled {
    background-color: #161923;
    color: #F9FAFB;
    selection-background-color: #6366F1;
    selection-color: #FFFFFF;
}
"""

LIGHT_STYLE = """
/* Main Frameless Overlay Window Styling (Light Mode - Polished) */
#OverlayContainer {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
}

/* Header Title Bar */
#HeaderFrame {
    background-color: #FFFFFF;
    border-top-left-radius: 16px;
    border-top-right-radius: 16px;
    border-bottom: 1px solid #E2E8F0;
    padding: 6px 10px;
}

#AppTitle {
    color: #0F172A;
    font-size: 14px;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
}

/* Header Buttons (Language & Theme Toggle) */
#LangToggleBtn, #ThemeToggleBtn {
    background-color: #F1F5F9;
    color: #475569;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    font-size: 12px;
    font-weight: bold;
    padding: 3px 8px;
    min-height: 22px;
}

#LangToggleBtn:hover, #ThemeToggleBtn:hover {
    background-color: #E2E8F0;
    color: #0F172A;
    border-color: #94A3B8;
}

/* Window Control Buttons */
.WindowBtn {
    background-color: transparent;
    color: #64748B;
    border: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
    min-width: 24px;
    min-height: 24px;
}

.WindowBtn:hover {
    background-color: #E2E8F0;
    color: #0F172A;
}

#CloseBtn:hover {
    background-color: #EF4444;
    color: #FFFFFF;
}

/* Input Controls */
QLineEdit, QComboBox, QDateEdit {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    color: #0F172A;
    padding: 5px 8px;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 1px solid #6366F1;
    background-color: #FFFFFF;
}

/* Time plain-text input (no spin arrows) */
#TimeInput {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    color: #0F172A;
    padding: 5px 4px;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
    text-align: center;
    min-width: 60px;
    max-width: 80px;
}

#TimeInput:focus {
    border: 1px solid #6366F1;
    background-color: #FFFFFF;
}

/* Dropdown QComboBox Popup */
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    selection-background-color: #6366F1;
    color: #0F172A;
    border-radius: 6px;
}

/* Add Task Button */
#AddTaskBtn {
    background-color: #4F46E5;
    color: #FFFFFF;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
}

#AddTaskBtn:hover {
    background-color: #4338CA;
}

#AddTaskBtn:pressed {
    background-color: #3730A3;
}

/* Sort & Year Controls */
#SortLabel, #YearLabel {
    color: #64748B;
    font-size: 11px;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
}

#SortCombo, #YearCombo {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    color: #0F172A;
    padding: 2px 6px;
    font-size: 11px;
    font-family: 'Segoe UI', sans-serif;
}

/* Task Item Container */
#TaskItemWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
}

#TaskItemWidget:hover {
    background-color: #F1F5F9;
    border: 1px solid #A5B4FC;
}

/* Checkbox */
QCheckBox {
    color: #0F172A;
    font-size: 13px;
    font-family: 'Segoe UI', sans-serif;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 2px solid #94A3B8;
    background-color: #FFFFFF;
}

QCheckBox::indicator:hover {
    border-color: #6366F1;
}

QCheckBox::indicator:checked {
    background-color: #10B981;
    border-color: #10B981;
}

/* Priority Badges with Solid Background & Soft Rounded Curves */
#BadgeHigh {
    background-color: #EF4444;
    color: #FFFFFF;
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 10px;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
}

#BadgeMed {
    background-color: #F59E0B;
    color: #FFFFFF;
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 10px;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
}

#BadgeLow {
    background-color: #10B981;
    color: #FFFFFF;
    border-radius: 6px;
    padding: 2px 7px;
    font-size: 10px;
    font-weight: bold;
    font-family: 'Segoe UI', sans-serif;
}

/* Deadline Button & Label */
#DeadlineBtn {
    background-color: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-radius: 5px;
    font-size: 12px;
    padding: 2px 6px;
    min-width: 22px;
    min-height: 20px;
}

#DeadlineBtn:hover {
    background-color: #E0E7FF;
    border-color: #6366F1;
}

#DeadlineLabel {
    color: #475569;
    font-size: 11px;
    font-family: 'Segoe UI', sans-serif;
    background-color: #F1F5F9;
    padding: 2px 6px;
    border-radius: 4px;
}

/* Delete Button */
#DeleteBtn {
    background-color: transparent;
    color: #94A3B8;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    font-size: 14px;
    min-width: 24px;
    min-height: 24px;
}

#DeleteBtn:hover {
    background-color: #FEE2E2;
    color: #EF4444;
}

/* Date Header Separator — slim and understated */
#DateHeader {
    color: #6366F1;
    font-size: 9px;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    padding: 3px 2px 1px 2px;
    border-bottom: 1px solid rgba(99, 102, 241, 0.25);
    background: transparent;
}

/* Month Filter Buttons */
#MonthFilterBtn {
    background: #F1F5F9;
    color: #94A3B8;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    font-size: 9px;
    font-weight: 700;
    font-family: 'Segoe UI', sans-serif;
    padding: 2px 1px;
    min-width: 30px;
    max-width: 36px;
}

#MonthFilterBtn:hover {
    background: #E0E7FF;
    color: #6366F1;
    border-color: #A5B4FC;
}

#MonthFilterBtn:checked {
    background: #6366F1;
    color: #FFFFFF;
    border-color: #6366F1;
}
#TimeLabel {
    color: #475569;
    font-size: 11px;
    font-family: 'Segoe UI', sans-serif;
    background: #EDE9FE;
    border: 1px solid #C4B5FD;
    border-radius: 5px;
    padding: 2px 6px;
    min-width: 46px;
}

/* ScrollArea & Scroll List Background Fix */
QScrollArea {
    background: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}

#TaskListContainer {
    background: transparent;
}

QScrollBar:vertical {
    background: transparent;
    width: 6px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #CBD5E1;
    border-radius: 3px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #94A3B8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Calendar Widget Light Popup Styling */
QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #F1F5F9;
}
QCalendarWidget QAbstractItemView:enabled {
    background-color: #FFFFFF;
    color: #0F172A;
    selection-background-color: #6366F1;
    selection-color: #FFFFFF;
}
"""

MAIN_STYLE = DARK_STYLE

def get_style(theme: str) -> str:
    """Returns the corresponding stylesheet string for theme ('dark' or 'light')."""
    if theme == "light":
        return LIGHT_STYLE
    return DARK_STYLE
