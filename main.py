import sys
import io
from PyQt5 import uic
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from testing import generate_questions


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
        self.pushButton_learn.clicked.connect(self.show_picture)

    def launch(self):
        self.set_background()
        self.fill_combobox()

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
            self.comboBox_learn.clear()
            name = f'load_files/clear.png'
            self.curr_image1 = QImage(name)
            self.patimg1 = QImage(name)
            self.pixmap1 = QPixmap(f'{name}')
            self.lable_learn.setPixmap(self.pixmap1)
        if self.sender().text() == "НАЧАТЬ ТЕСТИРОВАНИЕ":
            self.test_preparing()
            self.stackedWidget.setCurrentIndex(4)
        if self.sender().text() == "НАЧАТЬ ОБУЧЕНИЕ":
            self.stackedWidget.setCurrentIndex(2)
            self.learn_preparing()

    def fill_combobox(self):
        with open('load_files/shapes.txt', 'r', encoding='utf-8') as f:
            for shape in f.readlines():
                self.comboBox.addItem(shape)
        with open('load_files/test_themes.txt', 'r', encoding='utf-8') as f:
            for theme in f.readlines():
                self.comboBox_theme.addItem(theme)

    def test_preparing(self):
        self.user_name = self.get_name.text().rstrip()
        self.get_name.clear()
        self.test_theme = self.comboBox_theme.currentText().rstrip()
        questions = generate_questions(self.test_theme)

    def show_picture(self):
        shape = self.comboBox.currentText().rstrip()
        theme = self.comboBox_learn.currentText().rstrip()
        name = f'load_files/{shape}/{theme}.png'
        self.curr_image1 = QImage(name)
        self.patimg1 = QImage(name)
        self.pixmap1 = QPixmap(f'{name}')
        self.lable_learn.setPixmap(self.pixmap1)

    def learn_preparing(self):
        shape = self.comboBox.currentText().rstrip()
        with open(f"load_files/{shape}/{shape}.txt", "r", encoding='utf-8') as f:
            text = f.readlines()
        self.info_learn.setText(text[0])
        for x in text[1::]:
            self.comboBox_learn.addItem(x)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyGeomHelper()
    ex.show()
    sys.exit(app.exec())
