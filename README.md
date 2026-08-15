# 📌 NudgeNote

> **"Capture now, we'll remind you later."**  
> *"Catat sekarang, kami ingatkan nanti."*

NudgeNote is a lightweight, always-on-top desktop task manager overlay built with **PyQt6**. It lives on your screen, lets you jot down tasks instantly with priority and deadline, and automatically nudges you before things are due — no browser, no sign-up, no clutter.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📌 **Always-on-Top Overlay** | Frameless, translucent window that floats above all other apps |
| 🌙 ☀️ **Dark / Light Mode** | Toggle themes with a single click, saved automatically |
| 🌐 **Bilingual (ID / EN)** | Full Indonesian and English UI support |
| 🎯 **Priority Levels** | HIGH / MED / LOW badges with vivid color coding |
| 📅 **Deadline Picker** | Date calendar popup + manual time input (HH:MM) |
| 🔔 **Auto Reminder** | Background watchdog fires OS native notifications when deadline is ≤ 1 hour away |
| 📂 **Month & Year Filter** | Quick filter bar for 12 months + year dropdown |
| 🔃 **Smart Sorting** | Sort tasks by Priority or Deadline with persistent preference |
| 💾 **JSON Auto-save** | All tasks and settings saved locally — no database needed |
| 🖱️ **Draggable Window** | Click and drag anywhere on the header to reposition |

---

## 🚀 Getting Started

### Prerequisites

- Python **3.10+**
- pip

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/your-username/nudgenote.git
cd nudgenote

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

---

## 📁 Project Structure

```
NudgeNote/
├── main.py              # Entry point — initializes QApplication & overlay window
├── reminder.py          # Background watchdog timer for deadline notifications
├── storage.py           # TaskManager & SettingsManager (JSON persistence)
├── requirements.txt     # Python dependencies
├── settings.json        # Auto-generated: stores theme, language, sort preference
├── tasks.json           # Auto-generated: persisted task data
├── .gitignore
└── ui/
    ├── overlay_window.py  # Main frameless overlay widget & all UI logic
    ├── styles.py          # Dark & Light mode Qt stylesheets
    └── task_widget.py     # Individual task row widget (checkbox, badge, delete)
```

---

## ⚙️ Tech Stack

| Library | Version | Purpose |
|---|---|---|
| [PyQt6](https://pypi.org/project/PyQt6/) | ≥ 6.5.0 | UI framework & event loop |
| [plyer](https://pypi.org/project/plyer/) | ≥ 2.1.0 | Cross-platform OS desktop notifications |

---

## 🎮 Usage Guide

### Adding a Task
1. Type your task in the text field at the top
2. Select **priority** (High / Med / Low)
3. Pick a **deadline date** and type a **time** (e.g. `14:30`)
4. Press **Enter** or click **+ Tambah / + Add**

### Filtering Tasks
- Click a **month button** (JAN–DES / JAN–DEC) to filter by month
- Use the **Year dropdown** to switch year view
- Click the active month again to deselect and show all

### Sorting
- Use the **Sort** dropdown to switch between **Priority-first** or **Deadline-first** ordering

### Reminders
- NudgeNote silently monitors your deadlines in the background (checks every 30 seconds)
- When a task deadline is **within 1 hour**, an OS notification pops up automatically
- Each task is reminded only once to avoid spam

### Theme & Language
- Click **🌙 / ☀️** to toggle Dark / Light mode
- Click **ID / EN** to switch between Indonesian and English UI

---

## 📝 Local Data Files

NudgeNote stores everything locally — no cloud, no account:

| File | Content |
|---|---|
| `tasks.json` | All tasks with id, title, priority, deadline, status |
| `settings.json` | Theme, language, and sort preference |

> **Tip:** Both files are auto-created on first run. You can safely delete them to reset the app.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ · <strong>NudgeNote</strong> — <em>Capture now, we'll remind you later.</em>
</p>
