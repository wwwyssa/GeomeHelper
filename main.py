import sqlite3
import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QTableWidgetItem

from testing import generate_questions, check_results, update_db
from f import Ui_MainWindow


class MyGeomHelper(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.launch()
        self.user_name = None
        self.test_theme = None
        self.questions = None
        self.test_result = None
        self.diff = None
        self.user_answer_list = []
        self.get_result_btn.setEnabled(False)
        self.question_idx = 0
        self.learn_btn.clicked.connect(self.move_to_another)
        self.test_btn.clicked.connect(self.move_to_another)
        self.learning_back_btn.clicked.connect(self.move_to_another)
        self.testing_back_btn.clicked.connect(self.move_to_another)
        self.learning_start_btn.clicked.connect(self.move_to_another)
        self.testing_start_btn.clicked.connect(self.move_to_another)
        self.l_back_btn.clicked.connect(self.move_to_another)
        self.pushButton_learn.clicked.connect(self.show_picture)
        self.testing_btn.clicked.connect(self.get_ans)
        self.get_result_btn.clicked.connect(self.move_to_another)
        self.result_back_btn.clicked.connect(self.move_to_another)
        self.con = sqlite3.connect("geoma_db")
        self.titles = None

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
            if self.check_name():
                self.test_preparing()
                self.stackedWidget.setCurrentIndex(4)
        if self.sender().text() == "НАЧАТЬ ОБУЧЕНИЕ":
            self.stackedWidget.setCurrentIndex(2)
            self.learn_preparing()
        if self.sender().text() == "Получить результат":
            self.question_idx = 0
            self.testing_btn.setEnabled(True)
            self.get_result_btn.setEnabled(False)
            self.lineEdit.setEnabled(True)
            self.stackedWidget.setCurrentIndex(5)

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

        self.label_testing.setText(f"Тема теста: {self.test_theme}")
        self.questions = generate_questions(self.test_theme)
        self.textBrowser_task.setText(self.questions[self.question_idx][1])
        self.question_idx += 1

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

    def check_name(self):
        if len(self.get_name.text().rstrip()) == 0:
            text, ok = QInputDialog.getText(self, 'Введите имя', 'Введите имя:')
            if ok:
                self.get_name.setText(str(text))
                if len(self.get_name.text().rstrip()) != 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    def show_question(self, question):
        self.textBrowser_task.setText(question)

    def fill_result(self):
        self.textBrowser_name.setText(str(self.user_name))
        self.textBrowser_theme.setText(str(self.test_theme))
        self.textBrowser_result.setText(str(self.test_result))

    def get_ans(self):
        ans = self.lineEdit.text()
        ans = ans.replace(' ', '')
        self.user_answer_list.append(ans)
        if len(self.user_answer_list) == 5:
            self.testing_btn.setEnabled(False)
            self.get_result_btn.setEnabled(True)
            self.lineEdit.setDisabled(True)
            self.test_result, self.diff = check_results(self.user_answer_list, self.questions)
            self.fill_result()
            self.question_idx = 0
            update_db(self.test_theme, self.user_name, self.test_result)
            self.user_answer_list = list()
            self.update_result()
        self.lineEdit.clear()
        self.show_question(self.questions[self.question_idx][1])
        self.question_idx += 1

    def update_result(self):
        dif = ""
        print(self.diff[0][0])
        for e in self.diff:
            dif = dif + f"Ваш ответ: {e[0]}, Верный ответ: {e[1]}\n"
        self.differense.setText(dif)
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM results").fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            return
        self.tableWidget.setColumnCount(len(result[0]))
        titles = [i[0] for i in cur.description]
        result.sort(key=lambda x: (x[0], -x[2]))
        self.tableWidget.setHorizontalHeaderLabels(titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyGeomHelper()
    ex.show()
    sys.exit(app.exec())
