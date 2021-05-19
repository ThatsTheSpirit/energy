import sys
import typing
import qdarkstyle
from PyQt5 import QtWidgets
import csv
import os

from PyQt5.QtCore import QDir
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
        self.ui.actionOpen.triggered.connect(self.readFromFile)
        self.ui.actionSave.triggered.connect(self.saveToFile)

        self._rows = 0

    def pushButtonCalcClicked(self):
        flats = self.ui.spinBoxFlats.value()
        hallways = self.ui.spinBoxHallways.value()
        lifts_per_hallway = self.ui.spinBoxLiftsPerHallway.value()
        lift_power = self.ui.doubleSpinBoxPower.value()
        floors = self.ui.spinBoxFloors.value()
        ap = Apartment(hallways, floors, flats, lifts_per_hallway, lift_power)
        self.ui.lineEditResult.setText(f'{ap.p_p_zh_zd}')

        self.showTable(ap)

    def showTable(self, apart: Apartment, i=0):
        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
        self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(apart.hallways)))
        self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(apart.floors)))
        self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(apart.flats)))
        self.ui.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(str(apart.p_kv_ud)))
        self.ui.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(str(apart.lifts)))
        self.ui.tableWidget.setItem(i, 6, QtWidgets.QTableWidgetItem(str(apart.lift_power)))
        self.ui.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(str(apart.k_s_l)))
        self.ui.tableWidget.setItem(i, 8, QtWidgets.QTableWidgetItem(str(apart.p_p_kv)))
        self.ui.tableWidget.setItem(i, 9, QtWidgets.QTableWidgetItem(str(apart.p_pl)))
        self.ui.tableWidget.setItem(i, 10, QtWidgets.QTableWidgetItem(str(apart.p_p_zh_zd)))

    def readFromFile(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,
                                                         "Open File", QDir.homePath(), "CSV Files (*.csv)")
        aparts = []
        headersInput = ['hallways', 'floors', 'flats', 'lifts_per_hallway', 'lift_power']

        with open(fileName[0], 'r') as csvfile:
            next(csvfile)
            for line in csv.DictReader(csvfile, fieldnames=headersInput):
                aparts.append(Apartment(float(line['hallways']), float(line['floors']), float(line['flats']),
                                        float(line['lifts_per_hallway']),
                                        float(line['lift_power'])))

        self._rows = len(aparts)  # нужно для корректного вывода без пустых строк (в файл)

        self.ui.tableWidget.setRowCount(self._rows)
        for i, ap in enumerate(aparts):
            self.showTable(ap, i)

    def saveToFile(self):
        fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                                                         "Save File", QDir.homePath() + "/export.csv",
                                                         "CSV Files (*.csv)")
        data = []
        headersOutput = ['№', 'Nn', 'Nэ', 'Nкв', 'Pуд', 'Nл', 'Pл', 'Kс.л', 'Pр.кв', 'Pр.л', 'Pр.ж.зд']

        with open(fileName[0], 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headersOutput)

            writer.writeheader()
            for row in range(self._rows):
                rowdata = []
                for col in range(self.ui.tableWidget.columnCount()):
                    item = self.ui.tableWidget.item(row, col)
                    if item is not None:
                        rowdata.append(item.text())
                    else:
                        rowdata.append('')

                writer.writerow(dict(zip(headersOutput, rowdata)))


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
