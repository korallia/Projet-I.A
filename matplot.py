import sys
from venv import create
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QTimer
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QImage, QPainter
from __feature__ import snake_case, true_property # !!! must be the last import


class MPLApp(QtWidgets.QWidget):
    
    def __init__(self, dimension, parent = None):
        super().__init__(parent)

        self.__training_image_dataset = np.empty((0,dimension), dtype=np.float32)
        self.__image_test = np.empty((dimension), dtype=np.float32)
        
        self.__elevation = 30
        self.__azimuth = 45
        self.__azimuth_inc = 2.5

        self.__plot_width = 500
        self.__plot_height = 500
        self.__plot_dpi = 100

        self.__plot_figure = Figure(figsize=(self.__plot_width / self.__plot_dpi, self.__plot_height / self.__plot_dpi), dpi=self.__plot_dpi)

        self.__mpl_widget = QtWidgets.QLabel()
        self.__main_layout = QVBoxLayout()

        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(self._rotate)
        self.__timer.start(1000)

        self.__main_layout.add_widget(self.__mpl_widget)
        self.set_layout(self.__main_layout)

    @property
    def training_image_dataset(self):
        return self.__training_image_dataset

    @training_image_dataset.setter
    def training_image_dataset(self, value):
        self.__training_image_dataset = value

    @property
    def image_test(self):
        return self.__image_test

    @image_test.setter
    def image_test(self, value):
        # value_np = np.array(value)
        self.__image_test = value
    
    
    @property
    def plot_width(self):
        return self.__plot_width
    
    @plot_width.setter
    def plot_width(self,value):
        self.__plot_width = value
        self.__plot_figure = Figure(figsize=(self.__plot_width / self.__plot_dpi, self.__plot_height / self.__plot_dpi), dpi=self.__plot_dpi)

    @property
    def plot_height(self):
        return self.__plot_height

    @plot_height.setter
    def plot_height(self,value):
        self.__plot_height = value
        self.__plot_figure = Figure(figsize=(self.__plot_width / self.__plot_dpi, self.__plot_height / self.__plot_dpi), dpi=self.__plot_dpi)

    @property
    def plot_dpi(self):
        return self.__plot_dpi
        
    @plot_dpi.setter
    def plot_dpi(self,value):
        self.__plot_dpi = value    
        self.__plot_figure = Figure(figsize=(self.__plot_width / self.__plot_dpi, self.__plot_height / self.__plot_dpi), dpi=self.__plot_dpi)
        
    @Slot()
    def _rotate(self):
        self.update_mpl()
        self.__azimuth += self.__azimuth_inc
   
    def update_mpl(self):


        self.__plot_figure = Figure(figsize=(self.__plot_width / self.__plot_dpi, self.__plot_height / self.__plot_dpi), dpi=self.__plot_dpi)
        canvas = FigureCanvas(self.__plot_figure)
        ax = self.__plot_figure.add_subplot(111, projection='3d')
        ax.set_proj_type('persp')

        ax.scatter(self.__training_image_dataset[:,0], self.__training_image_dataset[:,1], self.__training_image_dataset[:,2], marker='o', color='r')
        ax.scatter(self.__image_test[0], self.__image_test[1], self.__image_test[2], marker='*',color='b', s=421)

        ax.set_title('THAT ASSET')
        ax.set_xlabel('Complexité')
        ax.set_ylabel('Rayon inscrit / Rayon circonscrit')
        ax.set_zlabel('Aire/Aire Circonscrit')

        ax.view_init(self.__elevation, self.__azimuth)

        canvas.draw()
        w, h = canvas.get_width_height()
        img = QImage(canvas.buffer_rgba(), w, h, w * 4, QImage.Format_ARGB32)

        self.__mpl_widget.pixmap = QtGui.QPixmap.from_image(img)


# matplot = MPLApp(3)
# matplot.test_image = np.array([0.1, 0.2, 0.3])
# print(matplot)


