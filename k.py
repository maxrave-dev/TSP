# Form implementation generated from reading ui file 'TSP_VER2.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1376, 877)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1070, 110, 49, 16))
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.sbDelayTime = QtWidgets.QDoubleSpinBox(parent=self.centralwidget)
        self.sbDelayTime.setGeometry(QtCore.QRect(1070, 130, 101, 22))
        self.sbDelayTime.setStyleSheet("")
        self.sbDelayTime.setMinimum(0)
        self.sbDelayTime.setMaximum(10)
        self.sbDelayTime.setObjectName("sbDelayTime")
        self.btStart = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btStart.setGeometry(QtCore.QRect(1250, 130, 75, 24))
        self.btStart.setStyleSheet("")
        self.btStart.setObjectName("btStart")
        self.btStop = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btStop.setGeometry(QtCore.QRect(1250, 180, 75, 24))
        self.btStop.setStyleSheet("")
        self.btStop.setObjectName("btStop")
        self.tbResult = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.tbResult.setGeometry(QtCore.QRect(1070, 570, 281, 251))
        self.tbResult.setStyleSheet("")
        self.tbResult.setObjectName("tbResult")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1070, 550, 49, 16))
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.canvaWidget = MplWidget(parent=self.centralwidget)
        self.canvaWidget.setEnabled(True)
        self.canvaWidget.setGeometry(QtCore.QRect(10, 10, 1041, 821))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvaWidget.sizePolicy().hasHeightForWidth())
        self.canvaWidget.setSizePolicy(sizePolicy)
        self.canvaWidget.setAutoFillBackground(True)
        self.canvaWidget.setStyleSheet("")
        self.canvaWidget.setObjectName("canvaWidget")
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(8, 10, 601, 611))
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1070, 160, 91, 16))
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.sbCoolingFactor = QtWidgets.QDoubleSpinBox(parent=self.centralwidget)
        self.sbCoolingFactor.setGeometry(QtCore.QRect(1070, 180, 101, 22))
        self.sbCoolingFactor.setMinimum(0.0)
        self.sbCoolingFactor.setMaximum(1.0)
        self.sbCoolingFactor.setSingleStep(0.01)
        self.sbCoolingFactor.setStepType(QtWidgets.QAbstractSpinBox.StepType.DefaultStepType)
        self.sbCoolingFactor.setProperty("value", 1.0)
        self.sbCoolingFactor.setObjectName("sbCoolingFactor")
        self.label_5 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1070, 300, 91, 16))
        self.label_5.setStyleSheet("")
        self.label_5.setObjectName("label_5")
        self.cbAddLocation = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cbAddLocation.setGeometry(QtCore.QRect(1070, 320, 151, 22))
        self.cbAddLocation.setObjectName("cbAddLocation")
        self.btAdd = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btAdd.setGeometry(QtCore.QRect(1250, 320, 75, 24))
        self.btAdd.setStyleSheet("")
        self.btAdd.setObjectName("btAdd")
        self.label_6 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(1070, 350, 111, 16))
        self.label_6.setStyleSheet("")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1070, 220, 91, 16))
        self.label_7.setStyleSheet("")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1180, 240, 101, 16))
        self.label_8.setStyleSheet("")
        self.label_8.setObjectName("label_8")
        self.spinBox = QtWidgets.QSpinBox(parent=self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(1070, 240, 101, 22))
        self.spinBox.setMaximum(100000)
        self.spinBox.setSingleStep(1000)
        self.spinBox.setProperty("value", 20000)
        self.spinBox.setObjectName("spinBox")
        self.listLocation = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listLocation.setGeometry(QtCore.QRect(1070, 370, 271, 131))
        self.listLocation.setObjectName("listLocation")
        self.btRemove = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btRemove.setGeometry(QtCore.QRect(1260, 510, 75, 24))
        self.btRemove.setStyleSheet("")
        self.btRemove.setObjectName("btRemove")
        self.label.raise_()
        self.sbDelayTime.raise_()
        self.btStart.raise_()
        self.btStop.raise_()
        self.tbResult.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.canvaWidget.raise_()
        self.label_2.raise_()
        self.sbCoolingFactor.raise_()
        self.label_5.raise_()
        self.cbAddLocation.raise_()
        self.btAdd.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.spinBox.raise_()
        self.listLocation.raise_()
        self.btRemove.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1376, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TSP with Simulated Annealing"))
        self.label.setText(_translate("MainWindow", "Delay (s)"))
        self.btStart.setText(_translate("MainWindow", "Start"))
        self.btStop.setText(_translate("MainWindow", "Stop"))
        self.label_3.setText(_translate("MainWindow", "Result"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "Cooling Factor"))
        self.label_5.setText(_translate("MainWindow", "Add Location"))
        self.btAdd.setText(_translate("MainWindow", "Add"))
        self.label_6.setText(_translate("MainWindow", "Current Location"))
        self.label_7.setText(_translate("MainWindow", "Cost"))
        self.label_8.setText(_translate("MainWindow", "VND per kilometer"))
        self.btRemove.setText(_translate("MainWindow", "Remove"))
from mplwidget import MplWidget
