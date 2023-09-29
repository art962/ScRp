from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import QLineEdit, QComboBox
from random import choice
import sys
from PyQt5.QtWidgets import QApplication


error_stylesheet = """
QWidget {
   color: #B22222;
}
"""

not_error_stylesheet = """
QWidget {
   color: #000000;
}
"""


class StringGenerator:
    def __init__(self, file):
        self.file = file  # файл с текстом

    def get(self):
        with open(self.file, encoding='utf-8') as text:
            text = text.read()
        t = text.split('. ')
        string = list(choice(t).strip() + '.')
        while '\n' in string:
            string[string.index('\n')] = ' '
        if len(string) < 33:
            return ''.join(string)
        ind = 32
        while string[ind] != ' ':
            ind -= 1
        string = string[:ind]
        return ''.join(string)


SGenerator = StringGenerator('text.txt')


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, 1920, 1280)
        self.setWindowTitle('Тестер набора на клавиатуре')
        self.all_open_windows = [self]
        self.main_label = QLabel(self)
        self.main_label.setGeometry(330, 100, 1200, 120)
        self.main_label.setText('Тестер')
        self.main_label.setFont(QtGui.QFont('inter', 60))
        self.main_label.setAlignment(Qt.AlignCenter)
        self.help_label = QLabel(self)
        self.help_label.setGeometry(735, 350, 400, 60)
        self.help_label.setText('Программа для измерения скорости вашей печати')
        self.help_label.setAlignment(Qt.AlignCenter)
        self.help_label.setFont(QtGui.QFont('inter', 30))
        self.start_button = QPushButton(self)
        self.start_button.setGeometry(730, 660, 400, 60)
        self.start_button.setText('СТАРТ')
        self.start_button.setFont(QtGui.QFont('inter', 30))
        self.start_button.clicked.connect(self.config2)
        self.generate_button = QPushButton(self)
        self.generate_button.setGeometry(430, 790, 1000, 90)
        self.generate_button.setText('Начать!')

        self.generate_button.setFont(QtGui.QFont('inter', 45))
        self.generate_button.clicked.connect(self.start)
        self.time_choice_box = QComboBox(self)
        self.time_choice_box.setGeometry(1550, 20, 350, 90)
        self.time_choice_box.setFont(QtGui.QFont('inter', 45))
        self.time_choice_box.addItems(['30 сек.', '1 мин.', '2 мин.',
                                       '3 мин.', '5 мин.'])
        self.time_choice_box.activated[str].connect(self.time_box_choice)

        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.update_time1)
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_time2)
        self.text_input = QLineEdit(self)
        self.text_input.setGeometry(330, 500, 1200, 90)
        self.text_input.setFont(QtGui.QFont('inter', 45))
        self.string_label = QLabel(self)
        self.string_label.setGeometry(330, 300, 1200, 60)
        self.string_label.setAlignment(Qt.AlignCenter)
        self.string_label.setFont(QtGui.QFont('inter', 30))
        self.exit_button = QPushButton(self)
        self.exit_button.setGeometry(50, 950, 300, 60)
        self.exit_button.setText('На главную')
        self.exit_button.setFont(QtGui.QFont('inter', 30))
        self.exit_button.clicked.connect(self.config1)
        self.config1()

    def time_box_choice(self, time):
        if time == '30 сек.':
            self.step2 = 30
        elif time == '1 мин.':
            self.step2 = 60
        elif time == '2 мин.':
            self.step2 = 120
        elif time == '3 мин.':
            self.step2 = 180
        elif time == '5 мин.':
            self.step2 = 300
        self.last_step2 = self.step2

    def generate_string(self):
        self.string = SGenerator.get()
        self.string_label.setText(self.string)

    def start(self):
        self.sym_count = 0
        self.generate_button.setEnabled(False)
        self.time_choice_box.setEnabled(False)
        self.exit_button.setEnabled(False)
        self.text_input.clear()
        self.step1 = 3
        self.main_label.setText('3')
        self.timer1.start(1000)
        self.text_input.textChanged.connect(self.check_string)

    def check_string(self):
        text = self.text_input.text()
        text_len = len(text)
        if self.string[:text_len] != text:  # ошибка
            self.text_input.setStyleSheet(error_stylesheet)
        if self.string[:text_len] == text:  # правильно
            self.sym_count += 1
            self.text_input.setStyleSheet(not_error_stylesheet)
            if self.string == text:
                self.text_input.clear()
                self.generate_string()

    def update_time1(self):
        self.step1 -= 1
        self.main_label.setText(str(self.step1))
        if self.step1 == 0:
            self.main_label.setText('Старт!')
        if self.step1 < 0:
            self.timer1.stop()
            self.generate_string()  # генерация нового предложения
            try:
                self.main_label.setText(str(self.step2))
            except AttributeError:
                self.step2 = 30
                self.last_step2 = 30
                self.main_label.setText(str(self.step2))
            self.string_label.show()
            self.timer2.start(1000)

    def update_time2(self):
        self.step2 -= 1
        self.main_label.setText(str(self.step2))
        if self.step2 == 0:
            self.timer2.stop()
            self.main_label.setText('Тест скорости печати')
            self.generate_button.setEnabled(True)
            self.time_choice_box.setEnabled(True)
            self.exit_button.setEnabled(True)
            self.text_input.clear()  # очистка текста
            self.string_label.hide()
            self.step2 = self.last_step2  # взводим таймер
            score = str(self.sym_count / self.step2)  # вычисляыем счёт
            if len(score) > 5:
                score = score[:5]
            score = float(score)
            self.show_results(score)

    def show_results(self, score):
        try:
            self.all_open_windows.remove(self.results_window)
            self.results_window.destroy()
        except AttributeError:
            pass
        self.results_window = ResultsWindow(score, self.sym_count, self.step2)
        self.results_window.show()
        self.all_open_windows.append(self.results_window)

    def config1(self):
        self.main_label.move(330, 100)
        self.help_label.setGeometry(550, 350, 800, 100)
        self.help_label.setText('Программа для измерения\nскорости вашей печати')
        self.main_label.setText('Тестер')
        self.generate_button.hide()
        self.text_input.hide()
        self.string_label.hide()
        self.time_choice_box.hide()
        self.exit_button.hide()
        self.start_button.show()

    def config2(self):
        self.main_label.move(330, 50)
        self.help_label.setGeometry(250, 200, 1500, 60)
        self.main_label.setText('Тест скорости печати')
        self.help_label.setText(
            'Переписывайте части предложений как можно скорее!')
        self.start_button.hide()
        self.exit_button.show()
        self.generate_button.show()
        self.text_input.show()
        self.string_label.show()
        self.time_choice_box.show()


class ResultsWindow(QWidget):
    def __init__(self, medium_score, sym_count, time):
        self.medium_score = medium_score  # средний результат
        self.sym_count = sym_count  # набрано символов
        self.time = time  # потрачено времени
        super().__init__()
        self.initUI()

    def initUI(self):
        self.move(300, 200)
        self.setFixedSize(420, 420)
        self.setWindowTitle('Результаты')
        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 400, 400)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QtGui.QFont('inter', 30))
        self.label.setText("Результат -\n" + str(self.medium_score)
                           + "\nсимв/сек.\n" + '(Набрано ' + str(self.sym_count)
                           + '\nсимволов за\n' + str(self.time) +
                           ' секунд)')