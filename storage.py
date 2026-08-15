import json
import os
import uuid
from datetime import datetime

PRIORITY_WEIGHTS = {
    "High": 1,
    "Medium": 2,
    "Med": 2,
    "Low": 3
}

class SettingsManager:
    """Manages application settings like theme preferences in settings.json."""
    def __init__(self, filepath="settings.json"):
        self.filepath = os.path.abspath(filepath)
        self.settings = {"theme": "dark", "lang": "ID", "sort_by": "priority"}
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

    def get_theme(self) -> str:
        return self.settings.get("theme", "dark")

    def set_theme(self, theme: str):
        self.settings["theme"] = theme
        self.save_settings()

    def get_lang(self) -> str:
        return self.settings.get("lang", "ID")

    def set_lang(self, lang: str):
        self.settings["lang"] = lang
        self.save_settings()

    def get_sort_by(self) -> str:
        return self.settings.get("sort_by", "priority")

    def set_sort_by(self, sort_by: str):
        self.settings["sort_by"] = sort_by
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
