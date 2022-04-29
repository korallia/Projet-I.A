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
                                QMessageBox, QComboBox, QFormLayout)
from PySide6.QtGui import  (QImage, QPixmap, QIcon, QPainter, QFont, QPen, QBrush, QColor, 
                            QStandardItemModel, QStandardItem,
                            QClipboard)
from __feature__ import snake_case, true_property 

class Dataset_Widget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        main_layout = QVBoxLayout()
        combo_box = QComboBox()

        submain_layout = QVBoxLayout()
        
        container_groupbox = QGroupBox("Dataset")
        
        

        groupbox_layout = QHBoxLayout()

        included_groupbox = QGroupBox("Included Dataset")
        included_form_layout = QFormLayout()
        included_groupbox.set_layout(included_form_layout)

        self.label_category_count = QLabel()
        self.label_training_image_count = QLabel()
        self.label_test_image_count = QLabel()
        self.label_total_image_count = QLabel()

        included_form_layout.add_row("Category count:", self.label_category_count)
        included_form_layout.add_row("Training image count:", self.label_training_image_count)
        included_form_layout.add_row("Test image count:", self.label_test_image_count)
        included_form_layout.add_row("Total image count:", self.label_total_image_count)


        transformation_groupbox = QGroupBox("Transformation")
        transformation_form_layout = QFormLayout()
        transformation_groupbox.set_layout(transformation_form_layout)

        self.label_translated = QLabel()
        self.label_rotated = QLabel()
        self.label_scaled = QLabel()

        transformation_form_layout.add_row("Translated :", self.label_translated)
        transformation_form_layout.add_row("Rotated :", self.label_rotated)
        transformation_form_layout.add_row("Scaled :", self.label_scaled)




        included_formlayout = QFormLayout()
        transformation_formlayout = QFormLayout()


        
        included_groupbox.set_layout(included_formlayout)
        transformation_groupbox.set_layout(transformation_formlayout)
        groupbox_layout.add_widget(included_groupbox)
        groupbox_layout.add_widget(transformation_groupbox)

        

        submain_layout.add_widget(combo_box)
        submain_layout.add_layout(groupbox_layout)
        
       
        container_groupbox.set_layout(submain_layout)


        main_layout.add_widget(container_groupbox)

        self.set_layout(main_layout) 
        
    
    
    



if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = Dataset_Widget()
    demo.window_title = 'Main'
    demo.show()

    sys.exit(app.exec_())  
