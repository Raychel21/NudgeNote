import sys
import os

# Ensure the project root is always in sys.path and the working directory,
# regardless of how/where the IDE launcher invokes this script.
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
os.chdir(_PROJECT_ROOT)

from PyQt6.QtWidgets import QApplication
from ui.overlay_window import NudgeNoteOverlay

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("NudgeNote")
    app.setStyle("Fusion")

    overlay = NudgeNoteOverlay()
    overlay.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
