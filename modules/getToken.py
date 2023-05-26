from PyQt6.QtCore import QUrl, QEventLoop, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from configparser import ConfigParser
from PyQt6 import QtGui
from PyQt6.QtGui import QAction
import sys

config = ConfigParser()
config.read('info/config.ini')


class Token(QMainWindow):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.token = ""
        self.setWindowIcon(QtGui.QIcon("assets/favicon.png"))
        self.setWindowTitle("Логин")
        self.browser = QWebEngineView()
        self.setGeometry(740, 160, 450, 800)
        self.setCentralWidget(self.browser)
        QAction("Quit", self).triggered.connect(self.closeEvent)
        self.browser.setUrl(
            QUrl(
                "https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d"))

        self.browser.urlChanged.connect(self.test)
        self.show()

    def test(self, q):
        if "#access_token" in q.toString():
            self.token = q.toString().split("=")[1].split("&")[0]
            self.closed.emit()

    def closeEvent(self, event):
        if len(QApplication.topLevelWidgets()) > 1:
            self.token = "0"
            self.closed.emit()
        else:
            sys.exit()


def UpdateToken():
    if len(QApplication.topLevelWidgets()) > 0:
        ...
    else:
        app = QApplication(sys.argv)
    w = Token()
    loop = QEventLoop()
    w.closed.connect(loop.quit)
    loop.exec()
    return w.token
