from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QColorDialog, QFileDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QImage
import cv2
import numpy as np
import time

class CurveFillingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Curve Filling App")
        self.setGeometry(100, 100, 800, 600)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.last_point = QPoint()
        self.fill_color = Qt.green  # Default fill color
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Draw a closed curve. Press 'F' to fill. Press 'C' to choose color. Press 'S' to save. Press 'L' to load.")
        layout.addWidget(label)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.image)
            pen = QPen(Qt.black, 3, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F:
            self.fill_curve()
        elif event.key() == Qt.Key_C:
            self.select_color()
        elif event.key() == Qt.Key_S:
            self.save_image()
        elif event.key() == Qt.Key_L:
            self.load_image()

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.fill_color = color

    def fill_curve(self):
        image = self.imageToCv(self.image)
        h, w = image.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        seed_point = (w//2, h//2)
        color = (self.fill_color.red(), self.fill_color.green(), self.fill_color.blue())
        for i in range(100):
            modified_image = image.copy()
            _, _, mask, _ = cv2.floodFill(modified_image, mask, seed_point, color, (5,)*3, (5,)*3, flags=cv2.FLOODFILL_MASK_ONLY | (i << 8))
            self.image = self.cvToQImage(modified_image)
            self.update()
            time.sleep(0.05)

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if file_path:
            self.image.save(file_path)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if file_path:
            self.image.load(file_path)
            self.update()

    def imageToCv(self, image):
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        arr = np.array(ptr).reshape(image.height(), image.width(), 4)
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

    def cvToQImage(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        return QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

if __name__ == "__main__":
    app = QApplication([])
    window = CurveFillingApp()
    window.show()
    app.exec_()
