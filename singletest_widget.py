from cProfile import label
import sys
import dataset_widget

from db_credential import PostgreSQLCredential
from klustr_dao import PostgreSQLKlustRDAO
from klustr_utils import qimage_argb32_from_png_decoding, ndarray_from_qimage_argb32
from klustr_widget import KlustRDataSourceViewWidget

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

    image_binaire_etat = Signal(str)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.credential = None
        self.klustr_dao = None
        self.set_credentials()
        self.image_binaire = None



        self.main_layout = QVBoxLayout()
        self.combo_box = QComboBox()
        self.submain_layout = QVBoxLayout()
        self.container_groupbox = QGroupBox("Single test")
        self.label_image = QLabel()

        self.label_text = QLabel("not classified")
        self.label_text.alignment = Qt.AlignCenter

        self.classify_button = QPushButton("Classify")
        
        
        self.label_image.style_sheet = "border:1px solid black; background-color: #204774"
        self.label_image.set_fixed_height(170)
        self.label_image.alignment = Qt.AlignCenter

        self.submain_layout.add_widget(self.combo_box)
        self.submain_layout.add_widget(self.label_image)
        self.submain_layout.add_widget(self.classify_button)
        self.submain_layout.add_widget(self.label_text)
       
        self.container_groupbox.set_layout(self.submain_layout)
        self.main_layout.add_widget(self.container_groupbox)
        self.set_layout(self.main_layout)
        self.change_dataset(dataset_widget.Dataset_Widget().name_image)
        self.combo_box.currentTextChanged.connect(self.update_image)

        # self.classify_button.clicked.connect(self.classify_action)
        

    @Slot()
    def change_dataset(self, dataset_name):
        self.combo_box.clear()
        self.list = self.klustr_dao.image_from_dataset(dataset_name, False)
        for i in range(len(self.list)):
            self.combo_box.add_item(self.list[i][3])
        
        self.update_image()

    @Slot()
    def update_image(self):
        image = qimage_argb32_from_png_decoding(self.list[self.combo_box.current_index][6])
        image_out = image.scaled(150,150)
        self.label_image.pixmap = QPixmap.from_image(image_out)
        self.image_binaire = ndarray_from_qimage_argb32(image)
        self.image_binaire_etat.emit(self.image_binaire)
        
        if (self.label_text.text != "not classified"):
            self.label_text.text = "not classified"


    def classify_action(self):
        self.label_text.text = "classification"
    
    @property
    def current_binary_image(self):
        return self.image_binaire

    @property
    def current_images_list(self):
        return self.list


    def set_credentials(self):
        self.credential = PostgreSQLCredential(password='ASDasd123')
        self.klustr_dao = PostgreSQLKlustRDAO(self.credential)
        self.source_data_widget = KlustRDataSourceViewWidget(self.klustr_dao)



if __name__ == '__main__':
    temp_str = "ABC"
    print(temp_str)
    app = QApplication(sys.argv)

    demo = Singletest_widget()
    demo.window_title = 'Main'
    demo.show()

    sys.exit(app.exec_())  