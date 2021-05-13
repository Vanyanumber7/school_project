import datetime
import sqlite3
import sys

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFormLayout, QLabel, QLineEdit, QScrollArea, \
    QGridLayout, QPushButton, QDialog, QHBoxLayout, QVBoxLayout, QColorDialog

DEFAULT_BACKGROUND_COLOR = '(255, 255, 255)'
DEFAULT_BUTTONS_COLOR = '(219, 175, 255)'
DEFAULT_LISTS_COLOR = '(255, 224, 252)'


class MyWidget(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()

        # подключение базы данных и первичный вывод
        self.con = sqlite3.connect("project.db")
        self.cur = self.con.cursor()

        self.colors()

        self.setupUi(self)
        self.ui_init()

    def ui_init(self):
        self.setFixedSize(750, 500)
        # подключение к кнопкам методов
        self.pushButton_week.clicked.connect(self.week)
        self.pushButton_help.clicked.connect(self.help)
        self.pushButton_purposes.clicked.connect(self.purposes)
        self.pushButton_settings.clicked.connect(self.settings)

        # передача информации от календаря
        self.date_display.setReadOnly(True)
        self.date = self.calendarWidget.selectedDate().toString('dd.MM.yyyy')
        self.lineEdit_date.setText(self.date)
        self.date_display.setText(self.date)
        self.date_display.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.calendarWidget.clicked.connect(self.calendar)
        self.pushButton_create.clicked.connect(self.create_business)
        self.duties()

        # выбор окна для показа
        self.radioButton_not_done.setChecked(True)
        self.radiobuttons(self.radioButton_not_done)
        self.buttonGroup_2.buttonClicked.connect(self.radiobuttons)
        self.close_deadlines()

        # создание объектов для добавления дел
        self.pushButton_add.clicked.connect(self.add)
        self.time.hide()
        self.business.hide()
        self.lineEdit_date.hide()
        self.pushButton_add.hide()
        self.lbl_successfully.hide()
        self.lbl_error.hide()
        self.label_date.hide()
        self.label_business.hide()
        self.label_time.hide()
        self.change_color()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 516)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(10, 10, 360, 200))
        self.calendarWidget.setStyleSheet("background-color: rgb(219, 175, 255);\n"
                                          "alternate-background-color: rgb(255, 170, 255);\n"
                                          "")
        self.calendarWidget.setObjectName("calendarWidget")
        self.lbl_selected_date = QtWidgets.QLabel(self.centralwidget)
        self.lbl_selected_date.setGeometry(QtCore.QRect(440, 20, 130, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_selected_date.setFont(font)
        self.lbl_selected_date.setObjectName("lbl_selected_date")
        self.date_display = QtWidgets.QLineEdit(self.centralwidget)
        self.date_display.setGeometry(QtCore.QRect(570, 20, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.date_display.setFont(font)
        self.date_display.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.date_display.setObjectName("date_display")
        self.radioButton_done = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_done.setGeometry(QtCore.QRect(410, 50, 140, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_done.setFont(font)
        self.radioButton_done.setObjectName("radioButton_done")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.radioButton_done)
        self.radioButton_not_done = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_not_done.setGeometry(QtCore.QRect(560, 50, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_not_done.setFont(font)
        self.radioButton_not_done.setObjectName("radioButton_not_done")
        self.buttonGroup_2.addButton(self.radioButton_not_done)
        self.pushButton_create = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_create.setGeometry(QtCore.QRect(510, 330, 101, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_create.setFont(font)
        self.pushButton_create.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.pushButton_create.setObjectName("pushButton_create")
        self.lbl_nearest_deadlines = QtWidgets.QLabel(self.centralwidget)
        self.lbl_nearest_deadlines.setGeometry(QtCore.QRect(119, 230, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_nearest_deadlines.setFont(font)
        self.lbl_nearest_deadlines.setObjectName("lbl_nearest_deadlines")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(400, 80, 321, 241))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.main_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.main_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.main_gridLayout.setObjectName("main_gridLayout")
        self.scroll = QtWidgets.QLabel(self.gridLayoutWidget)
        self.scroll.setStyleSheet("")
        self.scroll.setText("")
        self.scroll.setObjectName("scroll")
        self.main_gridLayout.addWidget(self.scroll, 0, 0, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(30, 260, 321, 161))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.main_gridLayout2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.main_gridLayout2.setContentsMargins(0, 0, 0, 0)
        self.main_gridLayout2.setObjectName("main_gridLayout2")
        self.scroll2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.scroll2.setStyleSheet("")
        self.scroll2.setText("")
        self.scroll2.setObjectName("scroll2")
        self.main_gridLayout2.addWidget(self.scroll2, 0, 0, 1, 1)
        self.label_date = QtWidgets.QLabel(self.centralwidget)
        self.label_date.setGeometry(QtCore.QRect(390, 370, 71, 20))
        self.label_date.setAlignment(QtCore.Qt.AlignCenter)
        self.label_date.setObjectName("label_date")
        self.label_time = QtWidgets.QLabel(self.centralwidget)
        self.label_time.setGeometry(QtCore.QRect(470, 370, 41, 20))
        self.label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_time.setObjectName("label_time")
        self.label_business = QtWidgets.QLabel(self.centralwidget)
        self.label_business.setGeometry(QtCore.QRect(520, 370, 131, 20))
        self.label_business.setAlignment(QtCore.Qt.AlignCenter)
        self.label_business.setObjectName("label_business")
        self.lineEdit_date = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_date.setGeometry(QtCore.QRect(390, 390, 71, 20))
        self.lineEdit_date.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_date.setObjectName("lineEdit_date")
        self.time = QtWidgets.QLineEdit(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(470, 390, 41, 20))
        self.time.setAlignment(QtCore.Qt.AlignCenter)
        self.time.setObjectName("time")
        self.pushButton_add = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add.setGeometry(QtCore.QRect(660, 390, 71, 21))
        self.pushButton_add.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.pushButton_add.setObjectName("pushButton_add")
        self.business = QtWidgets.QLineEdit(self.centralwidget)
        self.business.setGeometry(QtCore.QRect(520, 390, 131, 20))
        self.business.setObjectName("business")
        self.lbl_error = QtWidgets.QLabel(self.centralwidget)
        self.lbl_error.setGeometry(QtCore.QRect(400, 410, 321, 20))
        self.lbl_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_error.setObjectName("lbl_error")
        self.lbl_successfully = QtWidgets.QLabel(self.centralwidget)
        self.lbl_successfully.setEnabled(True)
        self.lbl_successfully.setGeometry(QtCore.QRect(400, 380, 321, 20))
        self.lbl_successfully.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_successfully.setObjectName("lbl_successfully")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 440, 681, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_settings = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_settings.setFont(font)
        self.pushButton_settings.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.pushButton_settings.setObjectName("pushButton_settings")
        self.horizontalLayout.addWidget(self.pushButton_settings)
        self.pushButton_purposes = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_purposes.setFont(font)
        self.pushButton_purposes.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.pushButton_purposes.setObjectName("pushButton_purposes")
        self.horizontalLayout.addWidget(self.pushButton_purposes)
        self.pushButton_week = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_week.setFont(font)
        self.pushButton_week.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.pushButton_week.setObjectName("pushButton_week")
        self.horizontalLayout.addWidget(self.pushButton_week)
        self.pushButton_help = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_help.setFont(font)
        self.pushButton_help.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.pushButton_help.setObjectName("pushButton_help")
        self.horizontalLayout.addWidget(self.pushButton_help)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Планер"))
        self.calendarWidget.setToolTip(_translate("MainWindow", "Выберите нужную вам дату"))
        self.lbl_selected_date.setText(_translate("MainWindow", "Выбранная дата:"))
        self.radioButton_done.setText(_translate("MainWindow", "Выполненные дела"))
        self.radioButton_not_done.setText(_translate("MainWindow", "Невыполненные дела"))
        self.pushButton_create.setText(_translate("MainWindow", "Создать"))
        self.lbl_nearest_deadlines.setText(_translate("MainWindow", "Ближайшие дела:"))
        self.label_date.setText(_translate("MainWindow", "Дата"))
        self.label_time.setText(_translate("MainWindow", "Время"))
        self.label_business.setText(_translate("MainWindow", "Название дела"))
        self.pushButton_add.setText(_translate("MainWindow", "Добавить"))
        self.lbl_error.setText(_translate("MainWindow", "Ой... Что-то пошло не так. Проверьте введенные данные."))
        self.lbl_successfully.setText(_translate("MainWindow", "Успешно добавлено!"))
        self.pushButton_settings.setText(_translate("MainWindow", "Настройки цветов"))
        self.pushButton_purposes.setText(_translate("MainWindow", "Цели"))
        self.pushButton_week.setText(_translate("MainWindow", "Список дел на неделю"))
        self.pushButton_help.setText(_translate("MainWindow", "Помощь"))

    def calendar(self):
        # изменяет self.date на дату, выбранную в календаре
        self.date = self.calendarWidget.selectedDate().toString('dd.MM.yyyy')
        self.date_display.setText(self.date)
        self.lineEdit_date.setText(self.date)
        self.duties()
        self.radioButton_not_done.setChecked(True)
        self.radiobuttons(self.radioButton_not_done)

    def duties(self):
        # забор и сортировка дел по выбранной дате
        self.resultTrue = self.cur.execute("""SELECT id, time, duty FROM duties
                    WHERE status = 'True' AND date=?""", (self.date,)).fetchall()
        self.resultTrue.sort(key=lambda x: x[1])
        self.resultFalse = self.cur.execute("""SELECT id, time, duty FROM duties
                    WHERE status = 'False' AND date=?""", (self.date,)).fetchall()
        self.resultFalse.sort(key=lambda x: x[1])

    def radiobuttons(self, btn):
        # вывод дел
        self.btn_radio = btn
        if btn.text() == 'Невыполненные дела':
            layout = QGridLayout()
            if not self.resultFalse:
                # если нет дел
                lbl = QLabel(self)
                lbl.setText('На этот день ещё ничего нет.')
                lbl.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                lbl.setFont(QtGui.QFont('Times', 12))
                layout.addWidget(lbl)
            else:
                layout.setRowStretch(111, 1)
            layout.setHorizontalSpacing(3)
            layout.setVerticalSpacing(8)
            # добавление информации в layout
            for j in range(1, len(self.resultFalse) + 1):
                time = QLineEdit(self)
                time.setText(self.resultFalse[j - 1][1])
                time.setReadOnly(True)
                time.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                business = QLineEdit(self)
                business.setText(self.resultFalse[j - 1][2])
                business.setReadOnly(True)

                btn_done = QPushButton()
                btn_done.setToolTip('Нажмите, если дело сделано')
                btn_done.setText(chr(9989))
                btn_done.setObjectName(str(self.resultFalse[j - 1][0]))
                btn_done.clicked.connect(self.done)
                btn_delete = QPushButton()

                btn_delete.setText(chr(10060))
                btn_delete.setToolTip('Удалить дело')
                btn_delete.setObjectName(str(self.resultFalse[j - 1][0]))
                btn_delete.clicked.connect(self.delete)

                time.setFixedSize(40, 20)
                btn_done.setFixedSize(20, 20)
                btn_delete.setFixedSize(20, 20)

                time.setStyleSheet("background-color: rgb(255, 255, 255);")
                business.setStyleSheet("background-color: rgb(255, 255, 255);")
                btn_done.setStyleSheet("background-color: rgb(255, 255, 255);")
                btn_delete.setStyleSheet("background-color: rgb(255, 255, 255);")

                layout.addWidget(time, j, 0)
                layout.addWidget(business, j, 1)
                layout.addWidget(btn_done, j, 2)
                layout.addWidget(btn_delete, j, 3)

            # добавление информации в главный layout
            self.main_gridLayout.removeWidget(self.scroll)
            self.scroll = QScrollArea()
            w = QWidget()
            w.setLayout(layout)
            w.setStyleSheet(f"background-color: rgb{self.list_color[0]};")
            self.scroll.setWidget(w)
            self.scroll.setWidgetResizable(True)
            self.scroll.setFixedSize(320, 240)
            self.main_gridLayout.addWidget(self.scroll)

        else:
            layout = QGridLayout()
            if not self.resultTrue:
                lbl = QLabel(self)
                lbl.setText('На этот день ещё ничего не выполнено.')
                lbl.setFont(QtGui.QFont('Times', 12))
                lbl.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                layout.addWidget(lbl)
            else:
                layout.setRowStretch(111, 1)
            layout.setHorizontalSpacing(3)
            layout.setVerticalSpacing(8)
            # добавление информации в layout
            for j in range(1, len(self.resultTrue) + 1):
                time = QLineEdit(self)
                time.setText(self.resultTrue[j - 1][1])
                time.setReadOnly(True)
                time.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                business = QLineEdit(self)
                business.setText(self.resultTrue[j - 1][2])
                business.setReadOnly(True)

                btn_delete = QPushButton()
                btn_delete.setToolTip('Удалить дело')
                btn_delete.setText(chr(10060))
                btn_delete.setObjectName(str(self.resultTrue[j - 1][0]))
                btn_delete.clicked.connect(self.delete)

                time.setFixedSize(40, 20)
                btn_delete.setFixedSize(20, 20)

                time.setStyleSheet("background-color: rgb(255, 255, 255);")
                business.setStyleSheet("background-color: rgb(255, 255, 255);")
                btn_delete.setStyleSheet("background-color: rgb(255, 255, 255);")

                layout.addWidget(time, j, 0)
                layout.addWidget(business, j, 1)
                layout.addWidget(btn_delete, j, 2)

            # добавление информации в главный layout
            self.main_gridLayout.removeWidget(self.scroll)
            self.scroll = QScrollArea()
            w = QWidget()
            w.setLayout(layout)
            w.setStyleSheet(f"background-color: rgb{self.list_color[0]};")
            self.scroll.setWidget(w)
            self.scroll.setWidgetResizable(True)
            self.scroll.setFixedSize(320, 240)
            self.main_gridLayout.addWidget(self.scroll)

    def create_business(self):
        # показ объектов для ввода
        self.time.setText('')
        self.time.show()
        self.lineEdit_date.show()
        self.time.setToolTip('Время')
        self.business.setText('')
        self.business.show()
        self.business.setToolTip('Название дела')
        self.pushButton_add.show()
        self.label_date.show()
        self.label_time.show()
        self.label_business.show()
        self.lbl_successfully.hide()
        self.lbl_error.hide()

    def add(self):
        # метод для создания нового дела
        self.lbl_error.hide()
        try:
            # проверка на правильный формат
            if (0, 0) <= tuple(map(int, self.time.text().split(':'))) <= (23, 59) and self.business.text() != '':
                # обновление информации в базе данных
                self.cur.execute("""INSERT INTO duties (date, time, duty, status)
                VALUES (?, ?, ?, "False")""", (self.date, self.time.text(), self.business.text()))
                self.time.hide()
                self.business.hide()
                self.pushButton_add.hide()
                self.label_date.hide()
                self.label_time.hide()
                self.label_business.hide()
                self.lineEdit_date.hide()
                self.lbl_successfully.show()
                self.con.commit()
                self.duties()
                # проверка. Если текущая дата, то обновить "Ближайшие дедлайны"
                if self.date == datetime.datetime.now().date().strftime('%d.%m.%Y'):
                    self.close_deadlines()
                self.radioButton_not_done.setChecked(True)
                self.radiobuttons(self.radioButton_not_done)
            else:
                self.lbl_error.show()
                self.create()
        except:
            self.lbl_error.show()
            self.create()

    def done(self):
        # метод для переноса дела в список выполненных
        self.sender()
        self.cur.execute("""UPDATE duties SET status = 'True' WHERE id=?""", (self.sender().objectName(),))
        self.con.commit()
        self.duties()
        self.radiobuttons(self.btn_radio)
        if self.date == datetime.datetime.now().date().strftime('%d.%m.%Y'):
            self.close_deadlines()

    def delete(self):
        # метод для удаления дела
        self.sender()
        self.cur.execute("""DELETE FROM duties WHERE id=?""", (self.sender().objectName(),))
        self.con.commit()
        self.duties()
        if self.date == datetime.datetime.now().date().strftime('%d.%m.%Y'):
            self.close_deadlines()
        self.radiobuttons(self.btn_radio)

    def close_deadlines(self):
        # формирование "Ближайшие дедлайны"
        date = datetime.datetime.now().date().strftime('%d.%m.%Y')
        result = self.cur.execute("""SELECT id, time, duty FROM duties
                            WHERE status = 'False' AND date=?""", (date,)).fetchall()
        result.sort(key=lambda x: x[1])
        layout = QGridLayout()
        # проверка на наличие дел
        if not result:
            lbl = QLabel(self)
            lbl.setText('Ближайших дедлайнов нет.')
            lbl.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            lbl.setFont(QtGui.QFont('Times', 12))
            layout.addWidget(lbl)
        else:
            layout.setRowStretch(111, 1)
        layout.setHorizontalSpacing(3)
        layout.setVerticalSpacing(8)
        # добавление информации в первичный layout
        for j in range(1, len(result) + 1):
            time = QLineEdit(self)
            time.setText(result[j - 1][1])
            time.setReadOnly(True)
            time.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

            business = QLineEdit(self)
            business.setText(result[j - 1][2])
            business.setReadOnly(True)

            btn_done = QPushButton()
            btn_done.setToolTip('Нажмите, если дело сделано')
            btn_done.setText(chr(9989))
            btn_done.setObjectName(str(result[j - 1][0]))
            btn_done.clicked.connect(self.done)

            btn_delete = QPushButton()
            btn_delete.setToolTip('Удалить дело')
            btn_delete.setText(chr(10060))
            btn_delete.setObjectName(str(result[j - 1][0]))
            btn_delete.clicked.connect(self.delete)

            time.setFixedSize(40, 20)
            btn_done.setFixedSize(20, 20)
            btn_delete.setFixedSize(20, 20)

            time.setStyleSheet("background-color: rgb(255, 255, 255);")
            business.setStyleSheet("background-color: rgb(255, 255, 255);")
            btn_done.setStyleSheet("background-color: rgb(255, 255, 255);")
            btn_delete.setStyleSheet("background-color: rgb(255, 255, 255);")

            layout.addWidget(time, j, 0)
            layout.addWidget(business, j, 1)
            layout.addWidget(btn_done, j, 2)
            layout.addWidget(btn_delete, j, 3)

        # добавление информации в конечный layout
        self.main_gridLayout2.removeWidget(self.scroll2)
        self.scroll2 = QScrollArea()
        w = QWidget()
        w.setLayout(layout)
        w.setStyleSheet(f"background-color: rgb{self.list_color[0]};")
        self.scroll2.setWidget(w)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.setFixedSize(320, 160)
        self.main_gridLayout2.addWidget(self.scroll2)

    def change_color(self):
        self.setStyleSheet(f"background-color: rgb{self.background_color[0]};")
        self.calendarWidget.setStyleSheet(f"background-color: rgb{self.button_color[0]};\n"
                                          f"alternate-background-color: rgb{self.list_color[0]};\n")
        self.pushButton_purposes.setStyleSheet(f"background-color: rgb{self.button_color[0]};")
        self.pushButton_week.setStyleSheet(f"background-color: rgb{self.button_color[0]};")
        self.pushButton_help.setStyleSheet(f"background-color: rgb{self.button_color[0]};")
        self.pushButton_create.setStyleSheet(f"background-color: rgb{self.button_color[0]};")
        self.pushButton_add.setStyleSheet(f"background-color: rgb{self.button_color[0]};")
        self.pushButton_settings.setStyleSheet(f"background-color: rgb{self.button_color[0]};")

    def colors(self):
        self.button_color = self.cur.execute("""SELECT rgb FROM colors WHERE color_type = 'buttons'""").fetchone()
        self.background_color = self.cur.execute(
            """SELECT rgb FROM colors WHERE color_type = 'background'""").fetchone()
        self.list_color = self.cur.execute("""SELECT rgb FROM colors WHERE color_type = 'lists'""").fetchone()

    def week(self):
        # открытие окна на всю неделю
        dialog = Week(self.button_color, self.background_color, self.list_color)
        sys.excepthook = except_hook
        dialog.exec_()
        self.duties()
        if self.date == datetime.datetime.now().date().strftime('%d.%m.%Y'):
            self.close_deadlines()
        self.radiobuttons(self.btn_radio)

    def help(self):
        # открытие помощи
        dialog = Help(self.background_color)
        sys.excepthook = except_hook
        dialog.exec_()

    def purposes(self):
        # открытие целей
        dialog = Purposes(self.button_color, self.background_color, self.list_color)
        sys.excepthook = except_hook
        dialog.exec_()

    def settings(self):
        # открытие настроек
        dialog = Settings()
        sys.excepthook = except_hook
        dialog.exec_()
        self.colors()
        self.change_color()
        self.radiobuttons(self.btn_radio)
        self.close_deadlines()


class Week(QDialog):
    # дополнительное окно для формирование списка дел на неделю
    def __init__(self, button_color, background_color, list_color):
        super().__init__()
        self.button_color = button_color
        self.background_color = background_color
        self.list_color = list_color
        self.setupUi(self)
        # подключение базы данных
        self.con = sqlite3.connect("project.db")
        self.cur = self.con.cursor()
        self.UI_init()

    def UI_init(self):
        # инициализация объектов
        self.setStyleSheet(f"background-color: rgb{self.background_color[0]};")
        self.setLayout(self.verticalLayout)
        self.day_lists = [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday,
                          self.sunday]
        self.scroll_area = [self.mon, self.tues, self.wednes, self.thurs, self.fri, self.satur, self.sun]
        self.namedays = [self.nameday_mon, self.nameday_tues, self.nameday_wednes, self.nameday_thurs, self.nameday_fri,
                         self.nameday_satur, self.nameday_sun]

        # выяснение дат начала недели и конца
        self.date1 = datetime.datetime.now().date() - datetime.timedelta(
            days=(datetime.datetime.now().date().isoweekday() - 1))
        self.date2 = self.date1 + datetime.timedelta(days=6)
        self.date()

        self.week.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.week.setReadOnly(True)
        self.early.clicked.connect(self.early_week)
        self.next.clicked.connect(self.next_week)

        # фиксирование размеров названий дней недели
        for day in self.namedays:
            day.setFixedSize(210, 30)
            day.setStyleSheet(f"background-color: rgb{self.button_color[0]};")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(920, 624)
        Dialog.setStyleSheet("")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 30, 751, 491))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(100, -1, 100, -1)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.early = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.early.setFont(font)
        self.early.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.early.setObjectName("early")
        self.horizontalLayout.addWidget(self.early)
        self.week = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.week.setFont(font)
        self.week.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.week.setObjectName("week")
        self.horizontalLayout.addWidget(self.week)
        self.next = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.next.setFont(font)
        self.next.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.next.setObjectName("next")
        self.horizontalLayout.addWidget(self.next)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.saturday = QtWidgets.QVBoxLayout()
        self.saturday.setObjectName("saturday")
        self.satur = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.satur.setText("")
        self.satur.setObjectName("satur")
        self.saturday.addWidget(self.satur)
        self.gridLayout_2.addLayout(self.saturday, 3, 2, 1, 1)
        self.nameday_satur = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameday_satur.setFont(font)
        self.nameday_satur.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.nameday_satur.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.nameday_satur.setObjectName("nameday_satur")
        self.gridLayout_2.addWidget(self.nameday_satur, 2, 2, 1, 1)
        self.nameday_sun = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameday_sun.setFont(font)
        self.nameday_sun.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.nameday_sun.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.nameday_sun.setObjectName("nameday_sun")
        self.gridLayout_2.addWidget(self.nameday_sun, 2, 4, 1, 1)
        self.wednesday = QtWidgets.QVBoxLayout()
        self.wednesday.setObjectName("wednesday")
        self.wednes = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.wednes.setText("")
        self.wednes.setObjectName("wednes")
        self.wednesday.addWidget(self.wednes)
        self.gridLayout_2.addLayout(self.wednesday, 1, 4, 1, 1)
        self.sunday = QtWidgets.QVBoxLayout()
        self.sunday.setObjectName("sunday")
        self.sun = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.sun.setText("")
        self.sun.setObjectName("sun")
        self.sunday.addWidget(self.sun)
        self.gridLayout_2.addLayout(self.sunday, 3, 4, 1, 1)
        self.thursday = QtWidgets.QVBoxLayout()
        self.thursday.setObjectName("thursday")
        self.thurs = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.thurs.setText("")
        self.thurs.setObjectName("thurs")
        self.thursday.addWidget(self.thurs)
        self.gridLayout_2.addLayout(self.thursday, 1, 5, 1, 1)
        self.tuesday = QtWidgets.QVBoxLayout()
        self.tuesday.setObjectName("tuesday")
        self.tues = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.tues.setText("")
        self.tues.setObjectName("tues")
        self.tuesday.addWidget(self.tues)
        self.gridLayout_2.addLayout(self.tuesday, 1, 2, 1, 1)
        self.nameday_fri = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameday_fri.setFont(font)
        self.nameday_fri.setStyleSheet("background-color: rgb(219, 175, 255);\n"
                                       "")
        self.nameday_fri.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.nameday_fri.setObjectName("nameday_fri")
        self.gridLayout_2.addWidget(self.nameday_fri, 2, 1, 1, 1)
        self.monday = QtWidgets.QVBoxLayout()
        self.monday.setObjectName("monday")
        self.mon = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.mon.setText("")
        self.mon.setObjectName("mon")
        self.monday.addWidget(self.mon)
        self.gridLayout_2.addLayout(self.monday, 1, 1, 1, 1)
        self.friday = QtWidgets.QVBoxLayout()
        self.friday.setObjectName("friday")
        self.fri = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.fri.setText("")
        self.fri.setObjectName("fri")
        self.friday.addWidget(self.fri)
        self.gridLayout_2.addLayout(self.friday, 3, 1, 1, 1)
        self.nameday_mon = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setStrikeOut(False)
        self.nameday_mon.setFont(font)
        self.nameday_mon.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.nameday_mon.setAcceptDrops(False)
        self.nameday_mon.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.nameday_mon.setAutoFillBackground(False)
        self.nameday_mon.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.nameday_mon.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.nameday_mon.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.nameday_mon.setObjectName("nameday_mon")
        self.gridLayout_2.addWidget(self.nameday_mon, 0, 1, 1, 1)
        self.nameday_tues = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameday_tues.setFont(font)
        self.nameday_tues.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.nameday_tues.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.nameday_tues.setObjectName("nameday_tues")
        self.gridLayout_2.addWidget(self.nameday_tues, 0, 2, 1, 1)
        self.nameday_wednes = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameday_wednes.setFont(font)
        self.nameday_wednes.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.nameday_wednes.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.nameday_wednes.setObjectName("nameday_wednes")
        self.gridLayout_2.addWidget(self.nameday_wednes, 0, 4, 1, 1)
        self.nameday_thurs = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameday_thurs.setFont(font)
        self.nameday_thurs.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.nameday_thurs.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.nameday_thurs.setObjectName("nameday_thurs")
        self.gridLayout_2.addWidget(self.nameday_thurs, 0, 5, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Список дел на неделю"))
        self.early.setText(_translate("Dialog", "Пред. неделя"))
        self.next.setText(_translate("Dialog", "След. неделя"))
        self.nameday_satur.setText(_translate("Dialog", "Суббота"))
        self.nameday_sun.setText(_translate("Dialog", "Воскресенье"))
        self.nameday_fri.setText(_translate("Dialog", "Пятница"))
        self.nameday_mon.setText(_translate("Dialog", "Понедельник"))
        self.nameday_tues.setText(_translate("Dialog", "Вторник"))
        self.nameday_wednes.setText(_translate("Dialog", "Среда"))
        self.nameday_thurs.setText(_translate("Dialog", "Четверг"))

    def date(self):
        # вывод временного промежутка
        self.week.setText(self.date1.strftime('%d.%m.%Y') + ' - ' + self.date2.strftime('%d.%m.%Y'))
        self.days_of_week()

    def days_of_week(self):
        # формирование списков дел
        for i in range(7):
            date = (self.date1 + datetime.timedelta(days=i)).strftime('%d.%m.%Y')
            result = self.cur.execute("""SELECT id, time, duty FROM duties
                                WHERE status = 'False' AND date=?""", (date,)).fetchall()
            result.sort(key=lambda x: x[1])
            layout = QGridLayout()
            # проверка на наличие дел
            if not result:
                label = QLabel(self)
                label.setText('На этот день ничего нет.')
                label.setFont(QtGui.QFont('Times', 11))
                label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                layout.addWidget(label, 5, 0)
            else:
                layout.setRowStretch(111, 1)
            layout.setHorizontalSpacing(2)
            layout.setVerticalSpacing(8)

            for j in range(1, len(result) + 1):
                time = QLineEdit(self)
                time.setText(result[j - 1][1])
                time.setFixedSize(33, 20)
                time.setReadOnly(True)
                time.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

                business = QLineEdit(self)
                business.setText(result[j - 1][2])
                business.setReadOnly(True)

                btn_done = QPushButton()
                btn_done.setToolTip('Нажмите, если дело сделано')
                btn_done.setFixedSize(20, 20)
                btn_done.setText(chr(9989))
                btn_done.setObjectName(str(result[j - 1][0]))
                btn_done.clicked.connect(self.done1)

                btn_delete = QPushButton()
                btn_delete.setToolTip('Удалить дело')
                btn_delete.setFixedSize(20, 20)
                btn_delete.setText(chr(10060))
                btn_delete.setObjectName(str(result[j - 1][0]))
                btn_delete.clicked.connect(self.delete)

                time.setStyleSheet("background-color: rgb(255, 255, 255);")
                business.setStyleSheet("background-color: rgb(255, 255, 255);")
                btn_done.setStyleSheet("background-color: rgb(255, 255, 255);")
                btn_delete.setStyleSheet("background-color: rgb(255, 255, 255);")

                layout.addWidget(time, j + 1, 0)
                layout.addWidget(business, j + 1, 1)
                layout.addWidget(btn_done, j + 1, 2)
                layout.addWidget(btn_delete, j + 1, 3)

            self.day_lists[i].removeWidget(self.scroll_area[i])
            self.scroll_area[i] = QScrollArea()
            w = QWidget()
            w.setLayout(layout)
            w.setStyleSheet(f"background-color: rgb{self.list_color[0]};")
            self.scroll_area[i].setWidget(w)
            self.scroll_area[i].setWidgetResizable(True)
            self.scroll_area[i].setFixedSize(210, 235)

            self.day_lists[i].addWidget(self.scroll_area[i])

    def early_week(self):
        # переход на неделю назад
        self.date1 -= datetime.timedelta(days=7)
        self.date2 -= datetime.timedelta(days=7)
        self.date()

    def next_week(self):
        # переход на неделю вперед
        self.date1 += datetime.timedelta(days=7)
        self.date2 += datetime.timedelta(days=7)
        self.date()

    def done1(self):
        self.sender()
        self.cur.execute("""UPDATE duties SET status = 'True' WHERE id=?""", (self.sender().objectName(),))
        self.con.commit()
        self.days_of_week()

    def delete(self):
        self.sender()
        self.cur.execute("""DELETE FROM duties WHERE id=?""", (self.sender().objectName(),))
        self.con.commit()
        self.days_of_week()


class Purposes(QDialog):
    # класс для создания окна целей
    def __init__(self, button_color, background_color, list_color):
        super().__init__()
        self.button_color = button_color
        self.background_color = background_color
        self.list_color = list_color
        self.setupUi(self)
        self.UI_init()

    def UI_init(self):
        self.setLayout(self.verticalLayout)
        self.lineEdit.setToolTip('Название дела')
        self.con = sqlite3.connect("project.db")
        self.cur = self.con.cursor()
        self.setStyleSheet(f"background-color: rgb{self.background_color[0]};")
        self.pushButton.setStyleSheet(f"background-color: rgb{self.button_color[0]};")
        self.pushButton.clicked.connect(self.create_purpose)
        self.list()
        self.setStyleSheet("background-color: rgb(0, 255, 255);")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(424, 447)
        Dialog.setStyleSheet("")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 371, 401))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(20, 10, 20, 15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(219, 175, 255);")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.scroll = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.scroll.setText("")
        self.scroll.setObjectName("scroll")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.scroll)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Цели"))
        self.label.setText(_translate("Dialog", "Мои цели"))
        self.pushButton.setText(_translate("Dialog", "Добавить"))

    def list(self):
        # формирование спика целей
        result = self.cur.execute("""SELECT id, name FROM purposes""").fetchall()
        size = QtGui.QFont()
        size.setPointSize(10)
        layout = QFormLayout()
        for i in range(len(result)):
            btn = QPushButton()
            btn.setObjectName(str(result[i][0]))
            btn.setText("Удалить")
            btn.setFont(size)
            btn.setFixedWidth(70)
            btn.setToolTip('Удалить цель')
            btn.clicked.connect(self.delete)
            btn.setStyleSheet(f"background-color: rgb{self.button_color[0]};")

            lbl = QLineEdit()
            lbl.setText(result[i][1])
            lbl.setFont(size)
            lbl.setReadOnly(True)
            lbl.setStyleSheet("background-color: rgb(255, 255, 255);")

            layout.addRow(btn, lbl)
        # вывод списка
        self.formLayout.removeWidget(self.scroll)
        self.scroll = QScrollArea()
        w = QWidget()
        w.setLayout(layout)
        w.setStyleSheet(f"background-color: rgb{self.list_color[0]};")
        self.scroll.setWidget(w)
        self.scroll.setWidgetResizable(True)
        # self.scroll.resize(310, 350)
        self.formLayout.addWidget(self.scroll)

    def create_purpose(self):
        if self.lineEdit.text():
            self.cur.execute("""INSERT INTO purposes (name) VALUES (?)""", (self.lineEdit.text(),))
            self.con.commit()
            self.list()

    def delete(self):
        self.sender()
        self.cur.execute("""DELETE FROM purposes WHERE id=?""", (int(self.sender().objectName()),))
        self.con.commit()
        self.list()

    def colors(self):
        self.button_color = self.cur.execute("""SELECT rgb FROM colors WHERE color_type = 'buttons'""").fetchone()
        self.background_color = self.cur.execute(
            """SELECT rgb FROM colors WHERE color_type = 'background'""").fetchone()
        self.list_color = self.cur.execute("""SELECT rgb FROM colors WHERE color_type = 'lists'""").fetchone()


class Help(QDialog):
    # класс для создания доп. окна с кратким описанием
    def __init__(self, background_color):
        super().__init__()
        self.background_color = background_color
        self.UI_init()

    def UI_init(self):
        self.setWindowTitle("Помощь")
        self.setFixedSize(609, 368)
        self.setStyleSheet(f"background-color: rgb{self.background_color[0]};")
        self.label_maintext = QLabel(self)
        self.label_maintext.setGeometry(QtCore.QRect(20, 30, 571, 311))
        self.label_maintext.setTextFormat(QtCore.Qt.RichText)
        self.label_maintext.setObjectName("label")
        self.label_title = QLabel(self)
        self.label_title.setGeometry(QtCore.QRect(270, 10, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_2")
        self.label_maintext.setText(
            "<html><head/><body><p><span style=\" font-size:9pt;\"> Привет! Здесь ты узнаешь всю информацию, которая "
            "тебе нужна.</span></p><p><span style=\" font-size:9pt; font-weight:600;\">Часто задаваемые вопросы:</span>"
            "</p><p><span style=\" font-size:9pt; font-style:italic;\">1. Что это? </span><span style=\" font-size:9pt;"
            "\">Это специальное приложение, которое поможет тебе планировать свои дела.</span></p><p><span style=\" "
            "font-size:9pt; font-style:italic;\">2. Как посмотреть мои дела? </span><span style=\" font-size:9pt;\">"
            "Всё очень просто: в календаре выбираете дату, правее Вы можете</span></p><p><span style=\" font-size:9pt;"
            "\">решить, что хотите посмотреть: &quot;Выполненные дела&quot; или &quot;Невыполненные дела&quot;.</span>"
            "</p><p><span style=\" font-size:9pt; font-style:italic;\">3. Как добавить дело? </span><span style=\" "
            "font-size:9pt;\">Ниже таблицы со списком дел есть кнопка &quot;Создать. Далее в появившихся</span></p><p>"
            "<span style=\" font-size:9pt;\">окошках введите время и дело. Потом нажмине на кнопку &quot;"
            "Добавить&quot;. Вот и всё.</span></p><p><span style=\" font-size:9pt; font-style:italic;\">4. "
            "Как удалить дело? </span><span style=\" font-size:9pt;\">В списке дел нажмине на крестик того дела, "
            "которое хотите удалить.</span></p><p><span style=\" font-size:9pt; font-style:italic;\">5. Что ещё "
            "здесь есть</span><span style=\" font-size:9pt;\">? Здесь вы ещё можете посмотреть свое расписание на "
            "неделю, нажав на</span></p><p><span style=\" font-size:9pt;\"> соответствующую кнопу.Также есть цели, "
            "куда вы можете записывать свои планы на будущее.</span></p><p><span style=\" font-size:9pt; font-style:"
            "italic;\">6. Сколько это стоит? </span><span style=\" font-size:9pt;\">Всё это </span><span style=\" "
            "font-size:9pt; font-weight:600;\">бесплатно</span><span style=\" font-size:9pt;\">.</span></p></body>"
            "</html>")
        self.label_title.setText("Помощь")


class Settings(QDialog):
    # класс для настройки цветов
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("project.db")
        self.cur = self.con.cursor()
        self.colors()
        self.UI_init()

    def UI_init(self):
        self.setGeometry(300, 300, 250, 200)
        self.setWindowTitle('Настройки цветов')
        layout = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        # создание кнопок для изменения цвета
        self.btn_background_color = QPushButton(self)
        self.btn_background_color.setText('Выбор цвета фона')
        self.btn_background_color.setObjectName('background')
        self.btn_background_color.clicked.connect(self.get_color)

        self.btn_button_color = QPushButton(self)
        self.btn_button_color.setText('Выбор цвета кнопок')
        self.btn_button_color.setObjectName('buttons')
        self.btn_button_color.clicked.connect(self.get_color)

        self.btn_list_color = QPushButton(self)
        self.btn_list_color.setText('Выбор цвета списков')
        self.btn_list_color.setObjectName('lists')
        self.btn_list_color.clicked.connect(self.get_color)

        self.btn_background_color.setStyleSheet(f"background-color: rgb{self.background_color[0]};")
        self.btn_button_color.setStyleSheet(f"background-color: rgb{self.button_color[0]};")
        self.btn_list_color.setStyleSheet(f"background-color: rgb{self.list_color[0]};")

        # создание кнопок для возврата к начальному чвету
        self.btn_default_background_color = QPushButton(self)
        self.btn_default_background_color.setText('Цвет фона по умолчанию')
        self.btn_default_background_color.setStyleSheet(f"background-color: rgb{DEFAULT_BACKGROUND_COLOR};")
        self.btn_default_background_color.setObjectName('background')
        self.btn_default_background_color.clicked.connect(self.default_get_color)

        self.btn_default_button_color = QPushButton(self)
        self.btn_default_button_color.setText('Цвет кнопок по умолчанию')
        self.btn_default_button_color.setStyleSheet(f"background-color: rgb{DEFAULT_BUTTONS_COLOR};")
        self.btn_default_button_color.setObjectName('buttons')
        self.btn_default_button_color.clicked.connect(self.default_get_color)

        self.btn_default_list_color = QPushButton(self)
        self.btn_default_list_color.setText('Цвет списков по умолчанию')
        self.btn_default_list_color.setStyleSheet(f"background-color: rgb{DEFAULT_LISTS_COLOR};")
        self.btn_default_list_color.setObjectName('lists')
        self.btn_default_list_color.clicked.connect(self.default_get_color)

        layout_left.addWidget(self.btn_background_color)
        layout_right.addWidget(self.btn_default_background_color)
        layout_left.addWidget(self.btn_button_color)
        layout_right.addWidget(self.btn_default_button_color)
        layout_left.addWidget(self.btn_list_color)
        layout_right.addWidget(self.btn_default_list_color)

        layout.addLayout(layout_left)
        layout.addLayout(layout_right)
        self.setLayout(layout)

    def get_color(self):
        color = QColorDialog.getColor().getRgb()
        color = color[:3]
        self.cur.execute("""UPDATE colors SET rgb=? WHERE color_type=?""", (str(color), self.sender().objectName()))
        self.con.commit()
        self.colors()
        self.change_color()

    def default_get_color(self):
        self.cur.execute("""UPDATE colors SET rgb=? WHERE color_type=?""",
                         (globals().get('DEFAULT_' + self.sender().objectName().upper() + '_COLOR'),
                          self.sender().objectName()))
        self.con.commit()
        self.colors()
        self.change_color()

    def colors(self):
        self.button_color = self.cur.execute("""SELECT rgb FROM colors WHERE color_type = 'buttons'""").fetchone()
        self.background_color = self.cur.execute(
            """SELECT rgb FROM colors WHERE color_type = 'background'""").fetchone()
        self.list_color = self.cur.execute("""SELECT rgb FROM colors WHERE color_type = 'lists'""").fetchone()

    def change_color(self):
        self.btn_background_color.setStyleSheet(f"background-color: rgb{self.background_color[0]};")
        self.btn_button_color.setStyleSheet(f"background-color: rgb{self.button_color[0]};")
        self.btn_list_color.setStyleSheet(f"background-color: rgb{self.list_color[0]};")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
