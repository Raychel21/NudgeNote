import sys
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
