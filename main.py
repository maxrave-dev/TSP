import sys
from typing import Optional
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QVBoxLayout, QLabel
import PyQt6.QtWidgets as QtWidgets
from matplotlib.backend_bases import FigureCanvasBase
from TSP import Ui_MainWindow
import algorithm as A
import asyncio
from asyncqt import QEventLoop, asyncSlot
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QRunnable, QThreadPool, QCoreApplication
import qtinter
import asyncio
import random
import numpy as np
import pyqtgraph as pg
from decimal import Decimal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

def convert_to_array(list):
    result = []
    for i in list:
        x, y = i
        a = np.array([x, y])
        result.append(a)
    return result
class AlertDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Warning")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.setModal(True)
        self.layout = QVBoxLayout()
        if message == None:
            self.message = QLabel("Please enter the number of destinations")
        else:
            self.message = QLabel(message)
        self.layout.addWidget(self.message)
        self.setLayout(self.layout)
class Core(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.isRunning = False
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btStart.clicked.connect(self.start)
        self.ui.btStop.clicked.connect(self.stop)
        self.task = None
        
    def stop(self):  
        self.isRunning = False
    def start(self):
        if self.isRunning == False:
            if (self.ui.sbNumberDestinations.value()) > 1:
                self.isRunning = True
                print("Start")
                map = A.Map(A.random_city(self.ui.sbNumberDestinations.value()))
                sa = A.SimulatedAnnealing(map, 100, 0.95, float(self.ui.sbDelayTime.value()))
                self.ui.canvaWidget.canvas.axes.set_xlim(0, 100)
                self.ui.canvaWidget.canvas.axes.set_ylim(0, 100)
                data = convert_to_array(map.cities)
                # for i in data:
                #     self.ui.canvaWidget.canvas.axes.plot([i[0]], [i[1]],'o')
                #     print(i[0], i[1])
                # self.ui.canvaWidget.canvas.draw()
                
                # data = convert_to_array(map.cities)
                # print(data)
                async def update_state():
                    while self.isRunning == True:
                        await asyncio.sleep(sa.delay)
                        sa.isRunning = self.isRunning
                    sa.isRunning == False
                async def update_plot():
                    while self.isRunning == True:
                        print(sa.current_solution)
                        temp = sa.current_solution
                        self.ui.canvaWidget.canvas.axes.clear()
                        index = 0
                        for i in data:
                            self.ui.canvaWidget.canvas.axes.plot([i[0]], [i[1]],'o', markersize=12)
                            self.ui.canvaWidget.canvas.axes.text(i[0], i[1], index)
                            print(i[0], i[1])
                            index+=1
                        for i in range(0, len(temp)-1, 1):
                            x_value = [data[temp[i]][0], data[temp[i+1]][0]]
                            y_value = [data[temp[i]][1], data[temp[i+1]][1]]
                            self.ui.canvaWidget.canvas.axes.plot(x_value, y_value, 'c')
                        self.ui.canvaWidget.canvas.draw()
                        await asyncio.sleep(sa.delay)
                async def update_result():
                    while self.isRunning == True:
                        await asyncio.sleep(sa.delay)
                        self.ui.tbResult.clear()
                        
                        if (sa.result != []):
                            data = sa.result[len(sa.result)-1]
                            self.ui.tbResult.append("#: " + str(data[0]) + " | Temperature: " + str(data[1]) + " | Solution: " + str(data[2]) + " | Cost: " + str(data[3]))
                        print(sa.result)
                
                async def all():
                    task = [asyncio.create_task(update_result()), asyncio.create_task(sa.solve()), asyncio.create_task(update_plot()), asyncio.create_task(update_state())]
                    self.task = asyncio.gather(*task)
                    while self.isRunning == True:
                        await self.task
                        if self.isRunning == False:
                            sa.isRunning = False
                            break
                with qtinter.using_qt_from_asyncio(): 
                    asyncio.run(all())

            else:
                dlg = AlertDialog("Please enter the number of destinations")
                dlg.exec()
        else:
            dlg = AlertDialog()
            dlg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Core()
    plt.axis('off')
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    with qtinter.using_qt_from_asyncio():
        window.show()
        sys.exit(app.exec())