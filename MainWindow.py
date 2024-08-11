from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QColorDialog, QFileDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QImage, QColor
import cv2
import numpy as np

class CurveFillingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Curve Filling App")
        self.setGeometry(100, 100, 800, 600)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.last_point = QPoint()
        self.points = []  # Store points of the curve
        self.fill_color = QColor(Qt.green)  # Default fill color as QColor
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
            self.points = [self.last_point]  # Start a new curve

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.image)
            pen = QPen(Qt.black, 3, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.points.append(self.last_point)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            # Connect last point to the first point to close the curve
            painter = QPainter(self.image)
            pen = QPen(Qt.black, 3, Qt.SolidLine)
            painter.setPen(pen)
            if len(self.points) > 1:
                painter.drawLine(self.points[-1], self.points[0])  # Close the curve
            self.update()

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

        # Create a binary mask of the curve
        curve_mask = np.zeros((h, w), np.uint8)
        if len(self.points) > 2:
            points_np = np.array([(p.x(), p.y()) for p in self.points], np.int32)
            cv2.fillPoly(curve_mask, [points_np], 255)

            # Create an RGB image for filling
            fill_image = np.zeros((h, w, 3), np.uint8)
            fill_image[curve_mask == 255] = [self.fill_color.red(), self.fill_color.green(), self.fill_color.blue()]

            # Combine the filled area with the original image
            image[curve_mask == 255] = fill_image[curve_mask == 255]

        # Update the QImage from the modified OpenCV image
        self.image = self.cvToQImage(image)
        self.update()

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
