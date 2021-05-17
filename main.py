import sys

import qdarkstyle
from PyQt5 import QtWidgets
import csv
import os
from scipy.interpolate import interp1d
from apartment import Apartment
from dropbox_auth import authentication
from ui.energyui.auth import Ui_DialogAuth
from ui.energyui.form_new import Ui_MainUi  # импорт нашего сгенерированного файла


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainUi()
        self.ui.setupUi(self)

        self.ui.pushButtonCalc.clicked.connect(self.pushButtonCalcClicked)
        self.ui.actionAbout.triggered.connect(lambda x: QtWidgets.QMessageBox.about(
            self, 'Информация', 'Программа написана на PyQt5'))
        self.ui.actionExit.triggered.connect(self.close)
        # self.dialog = Ui_DialogAuth()
        # self.dialog = AuthWindow()
        # self.dialog.show()
        # self.dialog.exec_()

    def pushButtonCalcClicked(self):
        flats = self.ui.spinBoxFlats.value()
        hallways = self.ui.spinBoxHallways.value()
        lifts_per_hallway = self.ui.spinBoxLiftsPerHallway.value()
        lifts_power = self.ui.doubleSpinBoxPower.value()
        floors = self.ui.spinBoxFloors.value()
        ap = Apartment(hallways, floors, flats, lifts_per_hallway, lifts_power)
        self.ui.lineEditResult.setText(f'{ap.p_p_zh_zd}')


class AuthWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AuthWindow, self).__init__(parent)
        self.ui = Ui_DialogAuth()
        self.ui.setupUi(self)

        self.add_functions()

    def handle_login(self):
        dropbox = authentication.DropBoxAuth()
        login, password = self.ui.lineEditLogin.text(), self.ui.lineEditPass.text()
        if dropbox.signin(login, password):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Ошибка', 'Неверный логин или пароль!')

    def handle_register(self):
        dropbox = authentication.DropBoxAuth()

        login, password = self.ui.lineEditLogin.text(), self.ui.lineEditPass.text()

        if dropbox.register(login, password):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Ошибка', 'Такой логин уже существует!')

    def add_functions(self):
        self.ui.pushButtonLogIn.clicked.connect(self.handle_login)
        self.ui.pushButtonRegister.clicked.connect(self.handle_register)


if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    auth = AuthWindow()

    if auth.exec_() == QtWidgets.QDialog.DialogCode.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
