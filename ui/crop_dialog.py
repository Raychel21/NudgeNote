import os
from PyQt6.QtCore import Qt, QRect, QPoint, QSize
from PyQt6.QtGui import QPixmap, QMouseEvent, QPainter, QColor, QPen
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox
)

class CropDialog(QDialog):
    """
    Dialog to let the user crop an image for the custom background.
    Forces a fixed aspect ratio (e.g. 450 / 570) to match the main NudgeNote window.
    """
    TARGET_RATIO = 450.0 / 570.0

    def __init__(self, image_path: str, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.cropped_pixmap = None
        
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.resize(800, 600)
        
        self._drag_pos = QPoint()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.container = QFrame(self)
        self.container.setObjectName("CropContainer")
        self.container.setStyleSheet("""
            #CropContainer {
                background-color: #1A1F2E;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 14px;
            }
        """)
        container_layout = QVBoxLayout(self.container)
        
        # Header
        hdr = QHBoxLayout()
        hdr.setContentsMargins(16, 12, 12, 12)
        title = QLabel("Crop Background Image")
        title.setStyleSheet("color: #F3F4F6; font-size: 14px; font-weight: bold; font-family: 'Segoe UI';")
        hdr.addWidget(title)
        hdr.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("background: transparent; color: #9CA3AF; border: none; font-size: 14px; font-weight: bold;")
        close_btn.clicked.connect(self.reject)
        hdr.addWidget(close_btn)
        container_layout.addLayout(hdr)
        
        # Image view
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_pixmap = QPixmap(self.image_path)
        
        # Scale pixmap down to fit max 700x450 while preserving aspect ratio
        self.scaled_pixmap = self.original_pixmap.scaled(
            700, 450, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(self.scaled_pixmap)
        container_layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Crop variables
        self.rubber_band = None
        self.origin = QPoint()
        
        # Footer
        footer = QHBoxLayout()
        footer.setContentsMargins(16, 12, 16, 12)
        
        hint = QLabel("Drag to select the crop area. Aspect ratio is locked to NudgeNote window size.")
        hint.setStyleSheet("color: #9CA3AF; font-size: 11px; font-family: 'Segoe UI';")
        footer.addWidget(hint)
        footer.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(99,102,241,0.15); color: #A5B4FC; 
                border: 1px solid rgba(99,102,241,0.3); border-radius: 8px; padding: 8px 20px; font-weight: bold; font-family: 'Segoe UI';
            }
            QPushButton:hover { background-color: rgba(99,102,241,0.3); color: #FFFFFF; }
        """)
        cancel_btn.clicked.connect(self.reject)
        footer.addWidget(cancel_btn)
        
        crop_btn = QPushButton("Crop & Save")
        crop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        crop_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366F1; color: #FFFFFF; border: none; border-radius: 8px; padding: 8px 24px; font-weight: bold; font-family: 'Segoe UI';
            }
            QPushButton:hover { background-color: #4F46E5; }
        """)
        crop_btn.clicked.connect(self.do_crop)
        footer.addWidget(crop_btn)
        
        container_layout.addLayout(footer)
        layout.addWidget(self.container)

    def mousePressEvent(self, event: QMouseEvent):
        # Window Dragging if clicked outside image
        if not self.image_label.geometry().contains(self.image_label.mapFrom(self, event.pos())):
            if event.button() == Qt.MouseButton.LeftButton:
                self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()
            return

        # Start rubber band on the image label
        img_pos = self.image_label.mapFrom(self, event.pos())
        self.origin = img_pos
        if not self.rubber_band:
            from PyQt6.QtWidgets import QRubberBand
            self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self.image_label)
            # Custom style for rubber band using QPalette could be added, but default is fine
        self.rubber_band.setGeometry(QRect(self.origin, QSize()))
        self.rubber_band.show()
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        # Window Dragging
        if not self.rubber_band or not self.rubber_band.isVisible():
            if event.buttons() & Qt.MouseButton.LeftButton and not self._drag_pos.isNull():
                self.move(event.globalPosition().toPoint() - self._drag_pos)
                event.accept()
            return

        # Update rubber band with fixed aspect ratio
        img_pos = self.image_label.mapFrom(self, event.pos())
        
        # Clamp to image bounds
        img_rect = self.image_label.rect()
        img_pos.setX(max(0, min(img_pos.x(), img_rect.width())))
        img_pos.setY(max(0, min(img_pos.y(), img_rect.height())))
        
        width = abs(img_pos.x() - self.origin.x())
        height = abs(img_pos.y() - self.origin.y())
        
        # Enforce aspect ratio
        if width > 0 and height > 0:
            if width / height > self.TARGET_RATIO:
                # Too wide, adjust width
                width = int(height * self.TARGET_RATIO)
            else:
                # Too tall, adjust height
                height = int(width / self.TARGET_RATIO)
        
        rect_x = self.origin.x() if img_pos.x() >= self.origin.x() else self.origin.x() - width
        rect_y = self.origin.y() if img_pos.y() >= self.origin.y() else self.origin.y() - height
        
        self.rubber_band.setGeometry(QRect(rect_x, rect_y, width, height))
        event.accept()
        
    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_pos = QPoint()

    def do_crop(self):
        if not self.rubber_band or not self.rubber_band.isVisible():
            QMessageBox.warning(self, "No Selection", "Please drag over the image to select the crop area.")
            return
            
        rect = self.rubber_band.geometry()
        
        # We need to map the rubber band rect (which is relative to scaled_pixmap) back to the original pixmap.
        # However, the image_label might have margins or the pixmap is centered. 
        # Since image_label.alignment is AlignCenter, the pixmap is drawn centered in the label.
        
        label_size = self.image_label.size()
        pixmap_size = self.scaled_pixmap.size()
        
        offset_x = (label_size.width() - pixmap_size.width()) // 2
        offset_y = (label_size.height() - pixmap_size.height()) // 2
        
        # Adjust rect to be relative to the scaled pixmap's top-left
        pixmap_rect = QRect(rect.x() - offset_x, rect.y() - offset_y, rect.width(), rect.height())
        
        # Map to original image size
        scale_x = self.original_pixmap.width() / pixmap_size.width()
        scale_y = self.original_pixmap.height() / pixmap_size.height()
        
        orig_rect = QRect(
            int(pixmap_rect.x() * scale_x),
            int(pixmap_rect.y() * scale_y),
            int(pixmap_rect.width() * scale_x),
            int(pixmap_rect.height() * scale_y)
        )
        
        # Crop the original image
        self.cropped_pixmap = self.original_pixmap.copy(orig_rect)
        self.accept()
