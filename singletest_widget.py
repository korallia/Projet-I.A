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
                                QMessageBox, QComboBox, QFormLayout, QPushButton)
from PySide6.QtGui import  (QImage, QPixmap, QIcon, QPainter, QFont, QPen, QBrush, QColor, 
                            QStandardItemModel, QStandardItem,
                            QClipboard)
from __feature__ import snake_case, true_property 

class Singletest_widget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        main_layout = QVBoxLayout()
        combo_box = QComboBox()
        submain_layout = QVBoxLayout()
        container_groupbox = QGroupBox("Single test")
        label_image = QLabel()

        label_text = QLabel("codification_image_pipi")
        label_text.alignment = Qt.AlignCenter
        classify_button = QPushButton("Classify")

        

        label_image.setStyleSheet("border:1px solid black; background-color: #204774")
       

        submain_layout.add_widget(combo_box)

        submain_layout.add_widget(label_image)
        submain_layout.add_widget(classify_button)
        submain_layout.add_widget(label_text)
        
       
        container_groupbox.set_layout(submain_layout)


        main_layout.add_widget(container_groupbox)

        self.set_layout(main_layout) 
        
    
    
    



if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = Singletest_widget()
    demo.window_title = 'Main'
    demo.show()

    sys.exit(app.exec_())  