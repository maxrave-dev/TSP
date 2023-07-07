import sys
# PyQt6 giúp tạo giao diện người dùng
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QVBoxLayout, QLabel
import PyQt6.QtCore as QtCore
from k import Ui_MainWindow
# Import code thuật toán chính
import algorithm as A

# Các thư viện hỗ trợ Async
import asyncio
import qtinter

# Các thư viện hỗ trợ vẽ đồ thị
import numpy as np
import matplotlib.pyplot as plt

import constant as C

from constant import name


# Hàm này dùng để chuyển đổi dữ liệu từ list sang array, mục đích nhằm phục vụ cho việc vẽ đồ thị
def convert_to_array(list):
    result = []
    for i in list:
        x, y = i
        a = np.array([x, y])
        result.append(a)
    return result

# Định nghĩa Custom Alert Dialog
class AlertDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Warning")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.message = QLabel(message)
        self.layout.addWidget(self.message)
        self.setLayout(self.layout)

# Lớp Xử lý UI và Sự kiện chính
class Core(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.isRunning = False
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btStart.clicked.connect(self.start)
        self.ui.btStop.clicked.connect(self.stop)
        self.ui.btAdd.clicked.connect(self.add_location)
        self.ui.btRemove.clicked.connect(self.remove_location)
        self.map = A.Map()
        self.task = None
        for i in name:
            self.ui.cbAddLocation.addItem(i)

    # Thêm địa điểm 
    def add_location(self):
        temp = self.ui.cbAddLocation.currentText()
        index = name.index(temp)
        search = self.ui.listLocation.findItems(temp, QtCore.Qt.MatchFlag.MatchExactly)
        if (len(search) >= 1):
            AlertDialog("This location was added before").exec()
        else:
            self.ui.listLocation.addItem(temp)
            self.map.add_city(index)
            self.ui.canvaWidget.canvas.axes.set_xlim(0, 1000)
            self.ui.canvaWidget.canvas.axes.set_ylim(0, 1000)
            self.ui.canvaWidget.canvas.axes.clear()
            data = convert_to_array(self.map.cities)
            self.ui.canvaWidget.canvas.axes.axis('on')
            self.ui.canvaWidget.canvas.axes.imshow(self.ui.canvaWidget.img, extent=[0, 1000, 0, 1000])
            for index in range(0, len(data), 1):
                i = data[index]
                self.ui.canvaWidget.canvas.axes.plot([i[0]], [i[1]],'o', markersize=5, color='c')
                self.ui.canvaWidget.canvas.axes.text(i[0]+1, i[1]+2, name[C.data_xy.index({"x": i[0], "y": i[1]})], fontsize=8)
            self.ui.canvaWidget.canvas.draw()

    # Xoá địa điểm 
    def remove_location(self):
        selected = self.ui.listLocation.selectedItems()
        if (len(selected) > 0):
            for item in selected:
                self.map.remove_city(self.ui.listLocation.row(item))
                self.ui.listLocation.takeItem(self.ui.listLocation.row(item))
            self.ui.canvaWidget.canvas.axes.set_xlim(0, 1000)
            self.ui.canvaWidget.canvas.axes.set_ylim(0, 1000)
            self.ui.canvaWidget.canvas.axes.clear()
            data = convert_to_array(self.map.cities)
            self.ui.canvaWidget.canvas.axes.axis('on')
            self.ui.canvaWidget.canvas.axes.imshow(self.ui.canvaWidget.img, extent=[0, 1000, 0, 1000])
            for index in range(0, len(data), 1):
                i = data[index]
                self.ui.canvaWidget.canvas.axes.plot([i[0]], [i[1]],'o', markersize=5, color='c')
                self.ui.canvaWidget.canvas.axes.text(i[0]+1, i[1]+2, name[C.data_xy.index({"x": i[0], "y": i[1]})], fontsize=8)
            self.ui.canvaWidget.canvas.draw()
    # Dừng thuật toán 
    def stop(self):  
        self.isRunning = False
        self.ui.canvaWidget.canvas.axes.set_xlim(0, 1000)
        self.ui.canvaWidget.canvas.axes.set_ylim(0, 1000)
        data = convert_to_array(self.map.cities)
        self.ui.canvaWidget.canvas.axes.clear()
        self.ui.canvaWidget.canvas.axes.axis('on')
        self.ui.canvaWidget.canvas.axes.imshow(self.ui.canvaWidget.img, extent=[0, 1000, 0, 1000])
        for index in range(0, len(data), 1):
            i = data[index]
            self.ui.canvaWidget.canvas.axes.plot([i[0]], [i[1]],'o', markersize=5, color='c')
            self.ui.canvaWidget.canvas.axes.text(i[0]+1, i[1]+2, name[C.data_xy.index({"x": i[0], "y": i[1]})], fontsize=8)
        self.ui.canvaWidget.canvas.draw()
    # Khởi động thuật toán
    def start(self):
        if self.isRunning == False:
            if (self.ui.sbDelayTime.value() > 0.00 and 0.00 < self.ui.sbCoolingFactor.value() < 1.00):
                if (self.ui.listLocation.count()) > 1:
                    self.isRunning = True
                    print("Start")
                    # Init Simulated Annealing
                    sa = A.SimulatedAnnealing(self.map, 100, self.ui.sbCoolingFactor.value(), float(self.ui.sbDelayTime.value()), self.ui.spinBox.value())
                    # Init Plot
                    self.ui.canvaWidget.canvas.axes.set_xlim(0, 1000)
                    self.ui.canvaWidget.canvas.axes.set_ylim(0, 1000)
                    data = convert_to_array(self.map.cities)
                    # Task 1: Cập nhật trạng thái thuật toán
                    async def update_state():
                        while self.isRunning == True:
                            await asyncio.sleep(sa.delay)
                            sa.isRunning = self.isRunning
                        sa.isRunning == False
                    # Task 2: Cập nhật đồ thị
                    async def update_plot():
                        while self.isRunning == True:
                            temp = sa.current_solution
                            # self.ui.canvaWidget.canvas.axes.cla()
                            self.ui.canvaWidget.canvas.axes.clear()
                            self.ui.canvaWidget.canvas.axes.imshow(self.ui.canvaWidget.img, extent=[0, 1000, 0, 1000])
                            for i in range(0, len(temp)-1, 1):
                                x_value = [data[temp[i]][0], data[temp[i+1]][0]]
                                y_value = [data[temp[i]][1], data[temp[i+1]][1]]
                                self.ui.canvaWidget.canvas.axes.plot(x_value, y_value, 'c')
                            x_value = [data[temp[len(temp)-1]][0], data[temp[0]][0]]
                            y_value = [data[temp[len(temp)-1]][1], data[temp[0]][1]]
                            self.ui.canvaWidget.canvas.axes.plot(x_value, y_value, 'c')
                            for x in range(0, len(data), 1):
                                i = data[x]
                                if x == temp[0]:
                                    self.ui.canvaWidget.canvas.axes.plot([i[0]], [i[1]],'o', markersize=5, color='r')
                                    self.ui.canvaWidget.canvas.axes.text(i[0]+1, i[1]+2, name[C.data_xy.index({"x": i[0], "y": i[1]})], fontsize=8)
                                else:
                                    self.ui.canvaWidget.canvas.axes.plot([i[0]], [i[1]],'o', markersize=5, color='c')
                                    self.ui.canvaWidget.canvas.axes.text(i[0]+1, i[1]+2, name[C.data_xy.index({"x": i[0], "y": i[1]})], fontsize=8)
                            self.ui.canvaWidget.canvas.draw()
                            await asyncio.sleep(sa.delay)
                    # Task 3: Cập nhật kết quả trên Text Browser
                    async def update_result():
                        while self.isRunning == True:
                            await asyncio.sleep(sa.delay)
                            self.ui.tbResult.clear()
                            
                            if (sa.result != []):
                                data = sa.result[len(sa.result)-1]
                                self.ui.tbResult.append("#: " + str(data[0]) + " | Temperature: " + str(data[1]) + " | Solution: " + str(data[2]) + " | Distance: " + str(data[3]) + "km | Cost: " + str(data[4]) + "VND")
                                if (data[5] <= 1e-5):
                                    self.isRunning = False
                                    self.ui.tbResult.clear()
                                    self.ui.tbResult.append("BEST SOLUTION: "+ "\n" +"#: " + str(data[0]) + " | Temperature: " + str(data[1]) + " | Solution: " + str(data[2]) + " | Distance: " + str(data[3]) + "km | Cost: " + str(data[4]) + "VND")
                                    break
                    
                    # Task 4: Gom tất cả Task con lại vào 1 Task lớn
                    async def all():
                        task = [asyncio.create_task(update_state()), asyncio.create_task(sa.solve()), asyncio.create_task(update_plot()), asyncio.create_task(update_result())]
                        self.task = asyncio.gather(*task)
                        while self.isRunning == True:
                            await self.task
                            if self.isRunning == False:
                                sa.isRunning = False
                                break
                    with qtinter.using_qt_from_asyncio(): 
                        asyncio.run(all())

                else:
                    dlg = AlertDialog("Please add at least 2 locations")
                    dlg.exec()
            else:
                dlg = AlertDialog("Please set delay time and cooling factor").exec()
        else:
            dlg = AlertDialog("Please stop the current algorithm before starting a new one")
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
