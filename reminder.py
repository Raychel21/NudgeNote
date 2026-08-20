import os
from datetime import datetime, timedelta
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False


def _play_sound(sound_path: str):
    """
    Attempts to play a custom .mp3 or .wav file.
    Falls back to Windows default beep if unavailable.
    """
    if sound_path and os.path.isfile(sound_path):
        ext = os.path.splitext(sound_path)[1].lower()
        if ext == ".wav":
            try:
                import winsound
                winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                return
            except Exception as e:
                print(f"[ReminderWatchdog] winsound error: {e}")
        elif ext == ".mp3":
            # Try playsound library first
            try:
                from playsound import playsound
                playsound(sound_path, block=False)
                return
            except Exception:
                pass
            # Fallback: try pygame
            try:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
                return
            except Exception as e:
                print(f"[ReminderWatchdog] mp3 playback error: {e}")

    # Final fallback: Windows default alert beep
    try:
        import winsound
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    except Exception:
        pass


class ReminderWatchdog(QObject):
    """
    Background Watchdog timer that periodically monitors task deadlines.
    Triggers desktop notifications and plays alert audio when a deadline
    is within the user-configured threshold (default: 1 hour).
    """
    reminder_alert = pyqtSignal(str, str)  # title, message

    def __init__(self, task_manager, settings_manager=None,
                 check_interval_ms: int = 30000, parent=None):
        super().__init__(parent)
        self.task_manager = task_manager
        self.settings_manager = settings_manager

        self.timer = QTimer(self)
        self.timer.setInterval(check_interval_ms)  # Default: check every 30 seconds
        self.timer.timeout.connect(self.check_deadlines)

    def _get_alert_seconds(self) -> float:
        """Returns the deadline alert threshold in seconds from settings."""
        if self.settings_manager is not None:
            hours = self.settings_manager.get_deadline_alert_hours()
        else:
            hours = 1
        return hours * 3600.0

    def start(self):
        """Starts the timer and performs an immediate check on startup."""
        self.timer.start()
        self.check_deadlines()

    def stop(self):
        """Stops the timer."""
        self.timer.stop()

    def check_deadlines(self):
        """Iterates over active tasks and checks deadline timestamps against current local time."""
        now = datetime.now()
        alert_window = self._get_alert_seconds()
        tasks = self.task_manager.tasks

        for task in tasks:
            if task.get("is_done", False) or task.get("reminded", False):
                continue

            deadline_str = task.get("deadline", "")
            if not deadline_str:
                continue

            try:
                deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
            except ValueError:
                try:
                    deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue

            # Time remaining until deadline (seconds)
            time_diff = (deadline_dt - now).total_seconds()

            # Trigger if within alert window or overdue (within last 24 hours)
            if -86400 <= time_diff <= alert_window:
                self.trigger_notification(task, time_diff)

    def trigger_notification(self, task: dict, time_diff: float):
        """Fires OS native notification, plays audio, and emits PyQt signal."""
        task_title = task.get("title", "Untitled Task")
        deadline_str = task.get("deadline", "")
        priority = task.get("priority", "Medium")

        if time_diff < 0:
            msg = f"Task '{task_title}' [{priority}] is OVERDUE! (Deadline: {deadline_str})"
        else:
            mins_left = max(1, int(time_diff // 60))
            msg = f"Task '{task_title}' [{priority}] is due in ~{mins_left} minutes! ({deadline_str})"

        # 1. Play custom alert sound (or fallback)
        sound_path = ""
        if self.settings_manager is not None:
            sound_path = self.settings_manager.get_alert_sound()
        _play_sound(sound_path)

        # 2. Fire system notification via Plyer if available
        if PLYER_AVAILABLE:
            try:
                notification.notify(
                    title="⏰ NudgeNote Task Reminder",
                    message=msg,
                    app_name="NudgeNote",
                    timeout=8
                )
            except Exception as e:
                print(f"[ReminderWatchdog] Plyer notification error: {e}")

        # 3. Emit signal for custom in-app popup or UI reaction
        self.reminder_alert.emit("NudgeNote Task Reminder", msg)

        # 4. Flag task as reminded in JSON storage
        self.task_manager.mark_reminded(task["id"])
