import sys
import io
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QMainWindow, QTabWidget


class GeomHelper(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)
        self.set_background()
        self.learn_btn.clicked.connect(self.move_to_another)
        self.test_btn.clicked.connect(self.move_to_another)
        self.learning_back_btn.clicked.connect(self.move_to_another)
        self.testing_back_btn.clicked.connect(self.move_to_another)

    def set_background(self):
        name = 'back.png'
        self.curr_image = QImage(name)
        self.patimg = QImage(name)
        self.pixmap = QPixmap(f'{name}')
        self.label.setPixmap(self.pixmap)

    def move_to_another(self):
        if self.sender().text() == "Учить!":
            self.stackedWidget.setCurrentIndex(1)
        if self.sender().text() == "Тестироваться!":
            self.stackedWidget.setCurrentIndex(2)
        if self.sender().text() == "НАЗАД":
            self.stackedWidget.setCurrentIndex(0)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GeomHelper()
    ex.show()
    sys.exit(app.exec_())
