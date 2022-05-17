from cProfile import label
import sys

from db_credential import PostgreSQLCredential
from klustr_dao import PostgreSQLKlustRDAO
from klustr_utils import qimage_argb32_from_png_decoding
from klustr_widget import KlustRDataSourceViewWidget

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import  (QApplication, QWidget, QListView, QTreeView,  
                                QGroupBox, QLabel, QCheckBox, QPlainTextEdit,
                                QGridLayout, QHBoxLayout, QVBoxLayout, QSplitter, QSizePolicy,
                                QMessageBox, QComboBox, QFormLayout, QPushButton, QScrollBar)
from PySide6.QtGui import  (QImage, QPixmap, QIcon, QPainter, QFont, QPen, QBrush, QColor, 
                            QStandardItemModel, QStandardItem,
                            QClipboard)
from __feature__ import snake_case, true_property 

class Knnparameters_widget(QtWidgets.QWidget):
    nb_voisins_changed = Signal(int)
    max_distance_changed = Signal(int)



    def __init__(self, parent = None):
        super().__init__(parent)
        self.__widget_size = QSize(200, 200)
        self.__main_layout = QVBoxLayout()
        self.__submain_layout = QVBoxLayout()
        self.__groupbox = QGroupBox("KNN parameters")

        self.__nb_voisins = 3
        self.__scrollbar_voisins = QScrollBar()
        self.__nb_voisins_label = QLabel(f"K = {self.__nb_voisins}" )
        self.__nb_voisins_label.alignment = Qt.AlignCenter
        self.__nb_voisins_layout = QHBoxLayout()
        self.__nb_voisins_layout.add_widget(self.__nb_voisins_label)
        self.__nb_voisins_layout.add_widget(self.__scrollbar_voisins)
        self.__scrollbar_voisins.orientation = Qt.Horizontal
        self.__scrollbar_voisins.fixed_width = 200
        self.__scrollbar_voisins.value = 3
        self.__scrollbar_voisins.minimum = 2
        self.__scrollbar_voisins.maximum = 10
        self.__scrollbar_voisins.valueChanged.connect(self.update_scroll)

        self.__max_distance = 1
        self.__scrollbar_max_distance = QScrollBar()
        self.__max_distance_label = QLabel(f"Max dist = {self.__max_distance}") 
        self.__max_distance_label.alignment = Qt.AlignCenter     
        self.__max_distance_layout = QHBoxLayout()
        self.__max_distance_layout.add_widget(self.__max_distance_label)
        self.__max_distance_layout.add_widget(self.__scrollbar_max_distance)
        self.__scrollbar_max_distance.orientation = Qt.Horizontal
        self.__scrollbar_max_distance.fixed_width = 200
        self.__scrollbar_max_distance.minimum = 1
        self.__scrollbar_max_distance.maximum = 1000
        self.__scrollbar_max_distance.value = 1000
        self.__scrollbar_max_distance.valueChanged.connect(self.update_scroll)     

        self.__submain_layout.add_layout(self.__nb_voisins_layout)
        self.__submain_layout.add_layout(self.__max_distance_layout)

        self.__groupbox.set_layout(self.__submain_layout)

        self.__main_layout.add_widget(self.__groupbox)
        
        self.set_layout(self.__main_layout) 

    @Slot()
    def update_scroll(self):
        self.__nb_voisins =  self.__scrollbar_voisins.value
        self.__max_distance = self.__scrollbar_max_distance.value
        self.__nb_voisins_label.text = (f"K = {self.__nb_voisins}")
        self.__max_distance_label.text = (f"Max dist = {self.__max_distance/1000}")
        self.nb_voisins_changed.emit(self.__nb_voisins)
        self.max_distance_changed.emit(self.__max_distance)

    @property
    def nb_voisins(self):
        return self.__nb_voisins
        
    @property
    def max_distance(self):
        return self.__max_distance/1000
    @property
    def widget_size(self):
        return self.__widget_size
    
    @widget_size.setter
    def widget_size(self,value):
        self.__widget_size = value
