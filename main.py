import os
from configparser import ConfigParser
from tkinter import messagebox

config = ConfigParser()
config.read('info/config.ini')
if len(config.get("main", "ym")) <= 2:
    messagebox.showinfo("[Яндекс Мimport os
from configparser import ConfigParser
from tkinter import messagebox
import traceback
from pypresence.exceptions import DiscordNotFound

config = ConfigParser()
config.read('info/config.ini')
if len(config.get("main", "ym")) <= 2:
    messagebox.showinfo("[Яндекс Музыка]", "[Яндекс Музыка] Установка необходимых пакетов.")
    os.system('pip install yandex-music --upgrade')
    os.system('pip install pypresence')
    os.system('pip install pyqt6')
    os.system('pip install pymem')
    os.system('pip install PyQt6-WebEngine')
import sys
import platform
try:
    from modules.rpc import MRPC
    from modules.yandexmusic import MYAPI
    from multiprocessing import Process, Queue
    from PyQt6 import QtGui
    from PyQt6.QtGui import QAction
    import webbrowser
    from PyQt6.QtCore import QRect, QMetaObject, QCoreApplication
    from PyQt6.QtWidgets import QWidget, QSystemTrayIcon, QMenu
    from PyQt6.QtWidgets import (
        QApplication,
        QCheckBox,
        QMainWindow,
        QPushButton
    )
except DiscordNotFound:
    messagebox.showerror(title="[Яндекс Музыка]", message="Сначала откройте Discord!")
    sys.exit()
except Exception as e:
    with open('error.txt', 'w') as f:
        f.write(str(traceback.format_exc()))
    messagebox.showerror(title="[Яндекс Музыка]", message="Произошла ошибка, попытайтесь разобратся сами или напишите разработчику.")
    sys.exit()
linux = False
# я делал на винде, поэтому не знаю имеет это смысл или нет
if "linux" in platform.system().lower():
    linux = True
q = Queue()
text_switch = 0
time_switch = 0
update = 0


class Ui_MainWindow(QMainWindow):
    global ISTOEXITBLYAT
    ISTOEXITBLYAT = False

    def __init__(self):
        super().__init__()
        self.MRPC = MRPC()
        self.setObjectName("MainWindow")
        self.setFixedSize(300, 200)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.setFont(font)
        self.setWindowIcon(QtGui.QIcon("assets/favicon.png"))
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QRect(16, 16, 550, 17))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(self.AppEnabling)
        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QRect(16, 46, 550, 17))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.stateChanged.connect(self.TimeSwitch)
        self.checkBox_3 = QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QRect(16, 76, 550, 17))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.stateChanged.connect(self.TextSwitch)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(16, 110, 269, 35))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.ForceUpdateToken)
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QRect(16, 150, 269, 35))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.fullexit)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)
        QMetaObject.connectSlotsByName(self)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("assets/favicon.png"))

        lable = QAction("Перейти на гитхаб", self)
        show_action = QAction("Показать", self)
        quit_action = QAction("Выход", self)
        hide_action = QAction("Севрнуть в трей", self)
        lable.triggered.connect(lambda: webbrowser.open('https://github.com/maj0roff/YandexMusicDiscordRPC', new=2))
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)

        quit_action.triggered.connect(self.fullexit)
        tray_menu = QMenu()
        tray_menu.addAction(lable)
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show()

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Яндекс Музыка RPC"))
        self.checkBox.setText(_translate("MainWindow", "Включить DiscordRPC"))
        if not linux:
            self.checkBox_2.setText(_translate("MainWindow", "Включить отображение времени трека"))
        else:
            self.checkBox_2.setEnabled(False)
            self.checkBox_2.setText(_translate("MainWindow", "времени трека (недоступно на Linux)"))
        self.checkBox_3.setText(_translate("MainWindow", "Включить кнопку текста песни (если есть)"))
        self.pushButton.setText(_translate("MainWindow", "Обновить токен Яндекс Музыки"))
        self.pushButton_2.setText(_translate("MainWindow", "Выход из приложения"))

    def AppEnabling(self, s):
        if s == 2:
            global thr
            thr = Process(target=MRPC().callPresence, args=(q,))
            thr.start()
            q.put([time_switch, text_switch, update])
        else:
            thr.terminate()
            self.MRPC.Clear()

    def TimeSwitch(self, s):
        global time_switch
        global update
        update = 1
        if s == 2:
            time_switch = 1
        else:
            time_switch = 0
        q.put([time_switch, text_switch, update])
        update = 0

    def TextSwitch(self, s):
        global text_switch
        global update
        update = 1
        if s == 2:
            text_switch = 1
        else:
            text_switch = 0
        q.put([time_switch, text_switch, update])
        update = 0

    def ForceUpdateToken(self, s):
        MYAPI().ForceUpdateToken()

    def fullexit(self, event):
        global ISTOEXITBLYAT
        ISTOEXITBLYAT = True
        try:
            thr.terminate()
        except NameError:
            ...
        finally:
            QApplication.quit()

    def closeEvent(self, event):
        if ISTOEXITBLYAT == False:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage("Яндекс Музыка | DiscordRPC", "Приложение свёрнуто в трей",
                                       QSystemTrayIcon.MessageIcon.NoIcon, 500)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Ui_MainWindow()
    window.show()
    app.exec()
узыка]", "[Яндекс Музыка] Установка необходимых пакетов.")
    os.system('pip install yandex-music --upgrade')
    os.system('pip install pypresence')
    os.system('pip install pyqt6')
    os.system('pip install pymem')
    os.system('pip install PyQt6-WebEngine')
import sys
import platform
from modules.rpc import MRPC
from modules.yandexmusic import MYAPI
from multiprocessing import Process, Queue
from PyQt6 import QtGui
from PyQt6.QtGui import QAction
import webbrowser
from PyQt6.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt6.QtWidgets import QWidget, QSystemTrayIcon, QMenu
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QMainWindow,
    QPushButton
)
linux = False
# я делал на винде, поэтому не знаю имеет это смысл или нет
if "linux" in platform.system().lower():
    linux = True
q = Queue()
text_switch = 0
time_switch = 0
update = 0


class Ui_MainWindow(QMainWindow):
    global ISTOEXITBLYAT
    ISTOEXITBLYAT = False

    def __init__(self):
        super().__init__()
        self.MRPC = MRPC()
        self.setObjectName("MainWindow")
        self.setFixedSize(300, 200)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.setFont(font)
        self.setWindowIcon(QtGui.QIcon("assets/favicon.png"))
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QRect(16, 16, 550, 17))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(self.AppEnabling)
        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QRect(16, 46, 550, 17))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.stateChanged.connect(self.TimeSwitch)
        self.checkBox_3 = QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QRect(16, 76, 550, 17))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.stateChanged.connect(self.TextSwitch)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(16, 110, 269, 35))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.ForceUpdateToken)
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QRect(16, 150, 269, 35))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.fullexit)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)
        QMetaObject.connectSlotsByName(self)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("assets/favicon.png"))

        lable = QAction("Перейти на гитхаб", self)
        show_action = QAction("Показать", self)
        quit_action = QAction("Выход", self)
        hide_action = QAction("Севрнуть в трей", self)
        lable.triggered.connect(lambda: webbrowser.open('https://github.com/maj0roff/YandexMusicDiscordRPC', new=2))
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)

        quit_action.triggered.connect(self.fullexit)
        tray_menu = QMenu()
        tray_menu.addAction(lable)
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show()

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Яндекс Музыка RPC"))
        self.checkBox.setText(_translate("MainWindow", "Включить DiscordRPC"))
        if not linux:
            self.checkBox_2.setText(_translate("MainWindow", "Включить отображение времени трека"))
        else:
            self.checkBox_2.setEnabled(False)
            self.checkBox_2.setText(_translate("MainWindow", "времени трека (недоступно на Linux)"))
        self.checkBox_3.setText(_translate("MainWindow", "Включить кнопку текста песни (если есть)"))
        self.pushButton.setText(_translate("MainWindow", "Обновить токен Яндекс Музыки"))
        self.pushButton_2.setText(_translate("MainWindow", "Выход из приложения"))

    def AppEnabling(self, s):
        if s == 2:
            global thr
            thr = Process(target=MRPC().callPresence, args=(q,))
            thr.start()
            q.put([time_switch, text_switch, update])
        else:
            thr.terminate()
            self.MRPC.Clear()

    def TimeSwitch(self, s):
        global time_switch
        global update
        update = 1
        if s == 2:
            time_switch = 1
        else:
            time_switch = 0
        q.put([time_switch, text_switch, update])
        update = 0

    def TextSwitch(self, s):
        global text_switch
        global update
        update = 1
        if s == 2:
            text_switch = 1
        else:
            text_switch = 0
        q.put([time_switch, text_switch, update])
        update = 0

    def ForceUpdateToken(self, s):
        MYAPI().ForceUpdateToken()

    def fullexit(self, event):
        global ISTOEXITBLYAT
        ISTOEXITBLYAT = True
        try:
            thr.terminate()
        except NameError:
            ...
        finally:
            QApplication.quit()

    def closeEvent(self, event):
        if ISTOEXITBLYAT == False:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage("Яндекс Музыка | DiscordRPC", "Приложение свёрнуто в трей",
                                       QSystemTrayIcon.MessageIcon.NoIcon, 500)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Ui_MainWindow()
    window.show()
    app.exec()
