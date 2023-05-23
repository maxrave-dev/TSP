import sys
# PyQt6 giúp tạo giao diện người dùng
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QVBoxLayout, QLabel
from TSP import Ui_MainWindow
# Import code thuật toán chính
import algorithm as A

# Các thư viện hỗ trợ Async
import asyncio
from asyncqt import QEventLoop, asyncSlot
import qtinter

# Các thư viện hỗ trợ vẽ đồ thị
import numpy as np
import matplotlib.pyplot as plt


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
        self.task = None

    # Dừng thuật toán 
    def stop(self):  
        self.isRunning = False

    # Khởi động thuật toán
    def start(self):
        if self.isRunning == False:
            if (self.ui.sbNumberDestinations.value()) > 1:
                self.isRunning = True
                print("Start")
                # Init Simulated Annealing
                map = A.Map(A.random_city(self.ui.sbNumberDestinations.value()))
                sa = A.SimulatedAnnealing(map, 100, 0.95, float(self.ui.sbDelayTime.value()))
                # Init Plot
                self.ui.canvaWidget.canvas.axes.set_xlim(0, 100)
                self.ui.canvaWidget.canvas.axes.set_ylim(0, 100)
                data = convert_to_array(map.cities)
                # Task 1: Cập nhật trạng thái thuật toán
                async def update_state():
                    while self.isRunning == True:
                        await asyncio.sleep(sa.delay)
                        sa.isRunning = self.isRunning
                    sa.isRunning == False
                # Task 2: Cập nhật đồ thị
                async def update_plot():
                    while self.isRunning == True:
                        print(sa.current_solution)
                        temp = sa.current_solution
                        self.ui.canvaWidget.canvas.axes.clear()
                        index = 0
                        for i in data:
                            if index == 0:
                                self.ui.canvaWidget.canvas.axes.plot([i[0]], [i[1]],'o', markersize=12, color='r')
                                self.ui.canvaWidget.canvas.axes.text(i[0]+1, i[1]+2, index)
                            else:
                                self.ui.canvaWidget.canvas.axes.plot([i[0]], [i[1]],'o', markersize=12, color='c')
                                self.ui.canvaWidget.canvas.axes.text(i[0]+1, i[1]+2, index)
                            print(i[0], i[1])
                            index+=1
                        for i in range(0, len(temp)-1, 1):
                            x_value = [data[temp[i]][0], data[temp[i+1]][0]]
                            y_value = [data[temp[i]][1], data[temp[i+1]][1]]
                            self.ui.canvaWidget.canvas.axes.plot(x_value, y_value, 'c')
                        x_value = [data[temp[len(temp)-1]][0], data[temp[0]][0]]
                        y_value = [data[temp[len(temp)-1]][1], data[temp[0]][1]]
                        self.ui.canvaWidget.canvas.axes.plot(x_value, y_value, 'c')
                        self.ui.canvaWidget.canvas.draw()
                        await asyncio.sleep(sa.delay)
                # Task 3: Cập nhật kết quả trên Text Browser
                async def update_result():
                    while self.isRunning == True:
                        await asyncio.sleep(sa.delay)
                        self.ui.tbResult.clear()
                        
                        if (sa.result != []):
                            data = sa.result[len(sa.result)-1]
                            self.ui.tbResult.append("#: " + str(data[0]) + " | Temperature: " + str(data[1]) + " | Solution: " + str(data[2]) + " | Cost: " + str(data[3]))
                            if (data[4] <= 1e-5):
                                self.isRunning = False
                                self.ui.tbResult.clear()
                                self.ui.tbResult.append("\n"+"BEST SOLUTION: "+ "\n" +"#: " + str(data[0]) + " | Temperature: " + str(data[1]) + " | Solution: " + str(data[2]) + " | Cost: " + str(data[3]))
                                break
                        print(sa.result)
                
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
                dlg = AlertDialog("Please enter the number of destinations")
                dlg.exec()
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