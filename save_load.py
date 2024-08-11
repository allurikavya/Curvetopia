from PyQt5.QtWidgets import QFileDialog

def initUI(self):
    central_widget = QWidget()
    layout = QVBoxLayout()
    label = QLabel("Draw a closed curve. Press 'F' to fill. Press 'C' to choose color. Press 'S' to save. Press 'L' to load.")
    layout.addWidget(label)
    central_widget.setLayout(layout)
    self.setCentralWidget(central_widget)

def keyPressEvent(self, event):
    if event.key() == Qt.Key_F:
        self.fill_curve()
    elif event.key() == Qt.Key_C:
        self.select_color()
    elif event.key() == Qt.Key_S:
        self.save_image()
    elif event.key() == Qt.Key_L:
        self.load_image()

def save_image(self):
    file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
    if file_path:
        self.image.save(file_path)

def load_image(self):
    file_path, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
    if file_path:
        self.image.load(file_path)
        self.update()
