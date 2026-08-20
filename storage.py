import json
import os
import uuid
import winreg
from datetime import datetime

PRIORITY_WEIGHTS = {
    "High": 1,
    "Medium": 2,
    "Med": 2,
    "Low": 3
}

APP_NAME = "NudgeNote"

class SettingsManager:
    """Manages application settings like theme preferences in settings.json."""
    def __init__(self, filepath="settings.json"):
        self.filepath = os.path.abspath(filepath)
        self.settings = {
            "theme": "midnight",
            "font": "Segoe UI",
            "lang": "ID",
            "sort_by": "priority",
            "deadline_alert_hours": 1,
            "startup": False,
            "alert_sound": "",
            "colorblind_mode": "normal",
            "custom_bg": ""
        }
        self.load_settings()

    def load_settings(self):
        if not os.path.exists(self.filepath):
            self.save_settings()
            return
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.settings.update(data)
        except Exception as e:
            print(f"[SettingsManager] Error loading settings: {e}")

    def save_settings(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"[SettingsManager] Error saving settings: {e}")

    # ── Theme ──────────────────────────────────────────────────────────────
    def get_theme(self) -> str:
        theme = self.settings.get("theme", "midnight")
        # Migrate old "dark"/"light" values to new theme names
        if theme == "dark":
            return "midnight"
        if theme == "light":
            return "parchment"
        return theme

    def set_theme(self, theme: str):
        self.settings["theme"] = theme
        self.save_settings()

    # ── Font ───────────────────────────────────────────────────────────────
    def get_font(self) -> str:
        return self.settings.get("font", "Segoe UI")

    def set_font(self, font: str):
        self.settings["font"] = font
        self.save_settings()

    # ── Language ───────────────────────────────────────────────────────────
    def get_lang(self) -> str:
        return self.settings.get("lang", "ID")

    def set_lang(self, lang: str):
        self.settings["lang"] = lang
        self.save_settings()

    # ── Sort ───────────────────────────────────────────────────────────────
    def get_sort_by(self) -> str:
        return self.settings.get("sort_by", "priority")

    def set_sort_by(self, sort_by: str):
        self.settings["sort_by"] = sort_by
        self.save_settings()

    # ── Deadline Alert Hours ───────────────────────────────────────────────
    def get_deadline_alert_hours(self) -> int:
        """Returns deadline alert threshold in hours (1–48). Default: 1."""
        val = self.settings.get("deadline_alert_hours", 1)
        try:
            return max(1, min(48, int(val)))
        except (TypeError, ValueError):
            return 1

    def set_deadline_alert_hours(self, hours: int):
        self.settings["deadline_alert_hours"] = max(1, min(48, int(hours)))
        self.save_settings()

    # ── Startup ────────────────────────────────────────────────────────────
    def get_startup(self) -> bool:
        return bool(self.settings.get("startup", False))

    def set_startup(self, enabled: bool):
        self.settings["startup"] = enabled
        self.save_settings()
        self._apply_startup_registry(enabled)

    def _apply_startup_registry(self, enabled: bool):
        """Adds or removes NudgeNote from Windows startup registry key."""
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, reg_path,
                0, winreg.KEY_SET_VALUE
            )
            if enabled:
                # Use pythonw.exe so no console window appears on startup
                python_exe = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "pythonw_launcher.bat"
                )
                # Fallback: just point to main.py with python
                main_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "main.py")
                )
                import sys
                exe = sys.executable.replace("python.exe", "pythonw.exe")
                if not os.path.exists(exe):
                    exe = sys.executable
                cmd = f'"{exe}" "{main_path}"'
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            print(f"[SettingsManager] Registry startup error: {e}")

    def get_startup_from_registry(self) -> bool:
        """Checks if NudgeNote is actually in startup registry (source of truth)."""
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, reg_path,
                0, winreg.KEY_READ
            )
            winreg.QueryValueEx(key, APP_NAME)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False

    # ── Alert Sound ────────────────────────────────────────────────────────
    def get_alert_sound(self) -> str:
        return self.settings.get("alert_sound", "")

    def set_alert_sound(self, path: str):
        self.settings["alert_sound"] = path
        self.save_settings()

    # ── Colorblind Mode ────────────────────────────────────────────────────
    def get_colorblind_mode(self) -> str:
        """Returns colorblind mode: 'normal', 'deuteranopia', or 'protanopia'."""
        return self.settings.get("colorblind_mode", "normal")

    def set_colorblind_mode(self, mode: str):
        valid = {"normal", "deuteranopia", "protanopia"}
        self.settings["colorblind_mode"] = mode if mode in valid else "normal"
        self.save_settings()


    # ── Custom Background ──────────────────────────────────────────────────
    def get_custom_bg(self) -> str:
        return self.settings.get("custom_bg", "")

    def set_custom_bg(self, path: str):
        self.settings["custom_bg"] = path
        self.save_settings()


class TaskManager:
    """Manages local JSON storage, CRUD operations, and task sorting logic."""
    
    def __init__(self, filepath="tasks.json"):
        self.filepath = os.path.abspath(filepath)
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Loads tasks from the local JSON file safely."""
        if not os.path.exists(self.filepath):
            self.tasks = []
            self.save_tasks()
            return
        
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        except Exception as e:
            print(f"[TaskManager] Error loading {self.filepath}: {e}")
            self.tasks = []

    def save_tasks(self):
        """Saves current tasks to the local JSON file."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[TaskManager] Error saving tasks: {e}")

    def add_task(self, title: str, priority: str = "Medium", deadline_str: str = "") -> dict:
        """Adds a new task and returns it."""
        new_task = {
            "id": str(uuid.uuid4()),
            "title": title.strip(),
            "priority": priority if priority in PRIORITY_WEIGHTS else "Med",
            "deadline": deadline_str.strip(),
            "is_done": False,
            "reminded": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def update_task_status(self, task_id: str, is_done: bool):
        """Updates is_done status for a given task id."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["is_done"] = is_done
                break
        self.save_tasks()

    def mark_reminded(self, task_id: str):
        """Flags task as reminded to avoid repetitive popups."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["reminded"] = True
                break
        self.save_tasks()

    def delete_task(self, task_id: str):
        """Deletes a task by id."""
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save_tasks()

    def get_sorted_tasks(self, sort_by: str = "priority") -> list:
        """
        Sorts tasks:
        - Unfinished tasks (is_done == False) come first.
          - If sort_by == 'priority': Sorted by Priority ('High' > 'Medium' > 'Low'), then Deadline.
          - If sort_by == 'deadline': Sorted by earliest Deadline timestamp, then Priority.
        - Finished tasks (is_done == True) are pushed to the bottom.
        """
        def parse_deadline(d_str):
            if not d_str:
                return datetime.max
            try:
                return datetime.strptime(d_str, "%Y-%m-%d %H:%M")
            except ValueError:
                try:
                    return datetime.strptime(d_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    return datetime.max

        active_tasks = [t for t in self.tasks if not t.get("is_done", False)]
        completed_tasks = [t for t in self.tasks if t.get("is_done", False)]

        if sort_by == "deadline":
            active_tasks.sort(key=lambda t: (
                parse_deadline(t.get("deadline", "")),
                PRIORITY_WEIGHTS.get(t.get("priority", "Medium"), 4)
            ))
        else:
            active_tasks.sort(key=lambda t: (
                PRIORITY_WEIGHTS.get(t.get("priority", "Medium"), 4),
                parse_deadline(t.get("deadline", ""))
            ))

        completed_tasks.sort(key=lambda t: parse_deadline(t.get("deadline", "")))

        return active_tasks + completed_tasks
