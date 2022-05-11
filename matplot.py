import sys
from venv import create

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar # wait for qt6!!! (is not working for now)

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QTimer
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QImage, QPainter
from __feature__ import snake_case, true_property # !!! must be the last import


# class KNNN:
#     def __init__(self, dimension):
#         self.training_data = np.empty((0,dimension), dtype=np.float32)
#         self.test_data = np.empty((0,dimension), dtype=np.float32)

#     def add_training_point(self, point, label):
#         if point.shape[1] is not self.training_data.shape[1]:
#             raise ValueError('ayoye')
#         self.training_data = np.append(self.training_data, point, axis=0)

#     def add_test_point(self, point, label):
#         if point.shape[1] is not self.test_data.shape[1]:
#             raise ValueError('ayoye')
#         self.test_data = np.append(self.test_data, point, axis=0)


# class Testies:

#     def __init__(self):
#         self._knn = KNNN(3)
#         self.create_data()
#         self.create_test_data()
    
#     def create_data(self):
#         rng = np.random.default_rng()
#         for _ in range(25):
#             self._knn.add_training_point(rng.random((1,3)), 'star')

#     def create_test_data(self):
#         rng = np.random.default_rng()
#         for _ in range(1):
#             self._knn.add_test_point(rng.random((1,3)), 'bloop')


class MPLApp(QtWidgets.QWidget):
    
    def __init__(self, dimension, parent = None):
        super().__init__(parent)

        self.training_dataset = np.empty((0,dimension), dtype=np.float32);
        self.test_dataset = np.empty((0,dimension), dtype=np.float32);
        
        self._elevation = 30
        self._azimuth = 45
        self._azimuth_inc = 2.5

        self._mpl_widget = QtWidgets.QLabel()
        self.layout = QVBoxLayout()

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._rotate)
        self._timer.start(1000)

        self.layout.add_widget(self._mpl_widget)
        self.set_layout(self.layout)


    @property
    def _set_training_data(self, training_dataset):
        self.training_dataset = training_dataset;

    @property
    def _set_test_data(self, test_dataset):
        self.test_dataset = test_dataset;

    
    @Slot()
    def _rotate(self):
        self.update_mpl()
        self._azimuth += self._azimuth_inc
   
    def update_mpl(self):

        width = 500
        height = 500
        dpi = 100
        figure = Figure(figsize=(width / dpi, height / dpi), dpi=dpi)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111, projection='3d')
        ax.set_proj_type('persp')

        ax.scatter(self.training_dataset[:,0], self.training_dataset[:,1], self.training_dataset[:,2], marker='o', color='r')
        ax.scatter(self.test_dataset[:,0], self.test_dataset[:,1], self.test_dataset[:,2], marker='*', color='b')

        ax.set_title('DATE À SEPT')
        ax.set_xlabel('METRIC 1')
        ax.set_ylabel('METRIC 2')
        ax.set_zlabel('METRIC 3')

        ax.view_init(self._elevation, self._azimuth)

        canvas.draw()
        w, h = canvas.get_width_height()
        img = QImage(canvas.buffer_rgba(), w, h, w * 4, QImage.Format_ARGB32)

        self._mpl_widget.pixmap = QtGui.QPixmap.from_image(img)


def main():
    QApplication.set_attribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)
    mpl_app = MPLApp(3)

    # test = Testies()
    
    # mpl_app.training_dataset = test._knn.training_data
    # mpl_app.test_dataset = test._knn.test_data

    mpl_app.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
