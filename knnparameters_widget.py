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
    def __init__(self, parent = None):
        super().__init__(parent)
        transf_widget_size = QSize(200, 200)
        main_layout = QVBoxLayout()
        self.knn_real = 6
        self.max_dist_real = 5
   
        


        submain_layout = QVBoxLayout()
        container_groupbox = QGroupBox("Knn parameters")
        scroll_bar_1 = QScrollBar()
        scroll_bar_2 = QScrollBar()
        self.knn_value = QLabel(f"K = {self.knn_real}" )
        self.knn_value.alignment = Qt.AlignCenter
        self.max_dist = QLabel(f"Max dist = {self.max_dist_real}")
        self.max_dist.alignment = Qt.AlignCenter
        
        
        
        param_1_layout = QHBoxLayout()
        param_2_layout = QHBoxLayout()

        param_1_layout.add_widget(self.knn_value)
        param_1_layout.add_widget(scroll_bar_1)
        param_2_layout.add_widget(self.max_dist)
        param_2_layout.add_widget(scroll_bar_2)


        scroll_bar_1.setOrientation(Qt.Horizontal)
        scroll_bar_2.setOrientation(Qt.Horizontal)
        scroll_bar_1.set_fixed_width(200)
        scroll_bar_2.set_fixed_width(200)
        scroll_bar_1.setValue(0)
        scroll_bar_2.setValue(0)
        scroll_bar_1.setRange(0,100)
        scroll_bar_2.setRange(0,100)


        submain_layout.add_layout(param_1_layout)
        submain_layout.add_layout(param_2_layout)

        
       
        container_groupbox.set_layout(submain_layout)


        main_layout.add_widget(container_groupbox)
        

        self.set_layout(main_layout) 
        
    
    
    



if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = Knnparameters_widget()
    demo.window_title = 'Main'
    demo.show()

    sys.exit(app.exec_())  