from PyQt6.QtWidgets import*

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from constant import *


# Định nghĩa Plot Widget
class MplWidget(QWidget):
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.figure = figure(figsize=(100, 100))
        self.figure.gca().axis('off')
        self.canvas = FigureCanvas(self.figure)
        self.img = plt.imread("map2.png")
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        # self.canvas.background.axis('off')
        self.canvas.axes = self.figure.add_subplot(111)
        self.canvas.axes.imshow(self.img, extent=[0, 1000, 0, 1000])
        self.canvas.background = self.figure.add_subplot(111)
        self.setLayout(vertical_layout)