import sys
import io
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QMainWindow, QTabWidget


class MyGeomHelper(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)
        self.launch()
        self.user_name = None
        self.test_theme = None
        self.learn_btn.clicked.connect(self.move_to_another)
        self.test_btn.clicked.connect(self.move_to_another)
        self.learning_back_btn.clicked.connect(self.move_to_another)
        self.testing_back_btn.clicked.connect(self.move_to_another)
        self.learning_start_btn.clicked.connect(self.move_to_another)
        self.testing_start_btn.clicked.connect(self.move_to_another)
        self.l_back_btn.clicked.connect(self.move_to_another)
        self.t_back_btn.clicked.connect(self.move_to_another)

    def launch(self):
        self.set_background()
        self.fill_comboBox()

    def set_background(self):
        name = 'load_files/back.png'
        self.curr_image = QImage(name)
        self.patimg = QImage(name)
        self.pixmap = QPixmap(f'{name}')
        self.label.setPixmap(self.pixmap)

    def move_to_another(self):
        if self.sender().text() == "Учить!":
            self.stackedWidget.setCurrentIndex(1)
        if self.sender().text() == "Тестироваться!":
            self.stackedWidget.setCurrentIndex(3)
        if self.sender().text() == "НАЗАД НА ГЛАВНУЮ":
            self.stackedWidget.setCurrentIndex(0)
        if self.sender().text() == "НАЧАТЬ ТЕСТИРОВАНИЕ":
            self.test_prepearing()
            self.stackedWidget.setCurrentIndex(4)
        if self.sender().text() == "НАЧАТЬ ОБУЧЕНИЕ":
            self.stackedWidget.setCurrentIndex(2)

    def fill_combobox(self):
        with open('load_files/shapes.txt', 'r', encoding='utf-8') as f:
            for shape in f.readlines():
                self.comboBox.addItem(shape)
        with open('load_files/test_themes.txt', 'r', encoding='utf-8') as f:
            for theme in f.readlines():
                self.comboBox_theme.addItem(theme)

    def test_preparing(self):
        self.user_name = self.get_name.text()
        self.get_name.clear()
        self.test_theme = self.comboBox_theme.currentText()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyGeomHelper()
    ex.show()
    sys.exit(app.exec())
