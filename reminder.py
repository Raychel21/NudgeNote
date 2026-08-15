from datetime import datetime, timedelta
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

class ReminderWatchdog(QObject):
    """
    Background Watchdog timer that periodically monitors task deadlines.
    Triggers desktop notifications when a deadline is within 1 hour or due.
    """
    reminder_alert = pyqtSignal(str, str) # title, message

    def __init__(self, task_manager, check_interval_ms=30000, parent=None):
        super().__init__(parent)
        self.task_manager = task_manager
        
        self.timer = QTimer(self)
        self.timer.setInterval(check_interval_ms) # Default check every 30 seconds
        self.timer.timeout.connect(self.check_deadlines)

    def start(self):
        """Starts the timer."""
        self.timer.start()
        # Perform an immediate check on startup
        self.check_deadlines()

    def stop(self):
        """Stops the timer."""
        self.timer.stop()

    def check_deadlines(self):
        """Iterates over active tasks and checks deadline timestamps against current local time."""
        now = datetime.now()
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

            # Time remaining until deadline
            time_diff = (deadline_dt - now).total_seconds()

            # Condition: Deadline within 1 hour (3600 seconds) or past due within 24 hours
            if -86400 <= time_diff <= 3600:
                self.trigger_notification(task, time_diff)

    def trigger_notification(self, task: dict, time_diff: float):
        """Fires OS native notification and emits PyQt signal."""
        task_title = task.get("title", "Untitled Task")
        deadline_str = task.get("deadline", "")
        priority = task.get("priority", "Medium")

        if time_diff < 0:
            msg = f"Task '{task_title}' [{priority}] is OVERDUE! (Deadline: {deadline_str})"
        else:
            mins_left = max(1, int(time_diff // 60))
            msg = f"Task '{task_title}' [{priority}] is due in ~{mins_left} minutes! ({deadline_str})"

        # 1. Fire system notification via Plyer if available
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

        # 2. Emit signal for custom in-app popup or UI reaction
        self.reminder_alert.emit("NudgeNote Task Reminder", msg)

        # 3. Flag task as reminded in JSON storage
        self.task_manager.mark_reminded(task["id"])
