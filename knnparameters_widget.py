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
    knn_changed = Signal(int)
    max_dist_changed = Signal(int)



    def __init__(self, parent = None):
        super().__init__(parent)
        transf_widget_size = QSize(200, 200)
        main_layout = QVBoxLayout()
        self.knn_real = 0
        self.max_dist_real = 0


        submain_layout = QVBoxLayout()
        container_groupbox = QGroupBox("Knn parameters")
        self.scroll_bar_1 = QScrollBar()
        self.scroll_bar_2 = QScrollBar()
        self.knn_value = QLabel(f"K = {self.knn_real}" )
        self.knn_value.alignment = Qt.AlignCenter
        self.max_dist = QLabel(f"Max dist = {self.max_dist_real}") 
        self.max_dist.alignment = Qt.AlignCenter                        #TWEEKS
        
        
        
        param_1_layout = QHBoxLayout()
        param_2_layout = QHBoxLayout()

        param_1_layout.add_widget(self.knn_value)
        param_1_layout.add_widget(self.scroll_bar_1)
        param_2_layout.add_widget(self.max_dist)
        param_2_layout.add_widget(self.scroll_bar_2)

        #TWEEKS
        self.scroll_bar_1.orientation = Qt.Horizontal
        self.scroll_bar_2.orientation = Qt.Horizontal
        self.scroll_bar_1.fixed_width = 200
        self.scroll_bar_2.fixed_width = 200
        self.scroll_bar_1.value = 0
        self.scroll_bar_2.value = 0
        self.scroll_bar_1.set_minimum = 0
        self.scroll_bar_1.maximum = 1000
        self.scroll_bar_2.set_minimum = 0
        self.scroll_bar_2.maximum = 100

    
        
        self.scroll_bar_1.valueChanged.connect(self.update_scroll)
        self.scroll_bar_2.valueChanged.connect(self.update_scroll)

        submain_layout.add_layout(param_1_layout)
        submain_layout.add_layout(param_2_layout)

       
        container_groupbox.set_layout(submain_layout)


        main_layout.add_widget(container_groupbox)
        

        self.set_layout(main_layout) 

    def update_scroll(self):
        self.knn_real =  self.scroll_bar_1.value
        self.max_dist_real = self.scroll_bar_2.value

        self.knn_value.text = (f"K = {self.knn_real}")
        self.max_dist.text = (f"Max dist = {self.max_dist_real/100}")
        self.knn_changed.emit(self.knn_real)
        self.max_dist_changed.emit(self.max_dist_real)

    @property
    def knn_actual_value(self):
        return self.knn_real
        
    @property
    def knn_max_dist(self):
        return self.max_dist_real/100
    
    

        

        
        
    
    
    



if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = Knnparameters_widget()
    demo.window_title = 'Main'
    demo.show()

    sys.exit(app.exec_())  