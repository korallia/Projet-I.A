from cProfile import label
import sys
import dataset_widget

from db_credential import PostgreSQLCredential
from klustr_dao import PostgreSQLKlustRDAO
from klustr_utils import qimage_argb32_from_png_decoding, ndarray_from_qimage_argb32
from klustr_widget import KlustRDataSourceViewWidget
from dataset_widget import Dataset_Widget

import numpy as np
from numpy import matrix

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import  (QApplication, QWidget, QListView, QTreeView,  
                                QGroupBox, QLabel, QCheckBox, QPlainTextEdit,
                                QGridLayout, QHBoxLayout, QVBoxLayout, QSplitter, QSizePolicy,
                                QMessageBox, QComboBox, QFormLayout, QPushButton)
from PySide6.QtGui import  (QImage, QPixmap, QIcon, QPainter, QFont, QPen, QBrush, QColor, 
                            QStandardItemModel, QStandardItem,
                            QClipboard)
from __feature__ import snake_case, true_property 

class Singletest_widget(QtWidgets.QWidget):

    image_binaire_changed = Signal(str)

    def __init__(self, parent = None):
        super().__init__(parent)

        self.__image_binaire = None
        self.__liste_images = None
        self.dataset_widget = Dataset_Widget()

        self.__main_layout = QVBoxLayout()
        self.__submain_layout = QVBoxLayout()
        self.__container_groupbox = QGroupBox("Single test")
        self.__combo_box = QComboBox()
        self.__label_image = QLabel()
        self.__label_text = QLabel("not classified")
        self.__classify_button = QPushButton("Classify")
        
        self.__label_text.alignment = Qt.AlignCenter
        self.__label_image.style_sheet = "border:1px solid black; background-color: #204774"
        self.__label_image.set_fixed_height(170)
        self.__label_image.alignment = Qt.AlignCenter

        self.__submain_layout.add_widget(self.__combo_box)
        self.__submain_layout.add_widget(self.__label_image)
        self.__submain_layout.add_widget(self.__classify_button)
        self.__submain_layout.add_widget(self.__label_text)
       
        self.__container_groupbox.set_layout(self.__submain_layout)

        self.__main_layout.add_widget(self.__container_groupbox)
        self.set_layout(self.__main_layout)

        self.change_dataset(self.dataset_widget.dataset_name)
        self.__combo_box.currentTextChanged.connect(self.update_image)
        

    @Slot()
    def change_dataset(self, dataset_name):
        self.__combo_box.clear()
        self.__liste_images = self.dataset_widget.klustr_dao.image_from_dataset(dataset_name, False)
        for i in range(len(self.__liste_images)):
            self.__combo_box.add_item(self.__liste_images[i][3])
        
        self.update_image()

    @Slot()
    def update_image(self):
        image = qimage_argb32_from_png_decoding(self.__liste_images[self.__combo_box.current_index][6])
        image_out = image.scaled(150,150)
        self.__label_image.pixmap = QPixmap.from_image(image_out)
        self.__image_binaire = ndarray_from_qimage_argb32(image)
        self.image_binaire_changed.emit(self.__image_binaire)
        
        if (self.__label_text.text != "not classified"):
            self.__label_text.text = "not classified"

    
    @property
    def image_binaire(self):
        return self.__image_binaire

    @property
    def liste_images(self):
        return self.__liste_images

    @property
    def classify_button(self):
        return self.__classify_button

    @property
    def label_text(self):
        return self.__label_text

    @label_text.setter
    def label_text(self, value):
        self.__label_text = value
