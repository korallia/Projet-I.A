import sys

from db_credential import PostgreSQLCredential
from klustr_dao import PostgreSQLKlustRDAO
from klustr_utils import qimage_argb32_from_png_decoding
from klustr_widget import KlustRDataSourceViewWidget
from dataset_widget import Dataset_Widget
from singletest_widget import Singletest_widget
from knnparameters_widget import Knnparameters_widget

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import  (QApplication, QWidget, QListView, QTreeView,  
                                QGroupBox, QLabel, QCheckBox, QPlainTextEdit,
                                QGridLayout, QHBoxLayout, QVBoxLayout, QSplitter, QSizePolicy,
                                QMessageBox, QPushButton)
from PySide6.QtGui import  (QImage, QPixmap, QIcon, QPainter, QFont, QPen, QBrush, QColor, 
                            QStandardItemModel, QStandardItem,
                            QClipboard)
from __feature__ import snake_case, true_property 

class Tab_widget(QtWidgets.QTabWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.tab_klstr_widget = QWidget()
        self.tab_classification_widget = QWidget()
        self.add_tab(self.tab_klstr_widget, "Kluster Source Viewer")
        self.add_tab(self.tab_classification_widget, "KNN Image Classification")
        self.get_klstr_widget()
        self.get_classication_widget()

    def get_klstr_widget(self):
        layout  = QVBoxLayout()
        self.set_tab_text(0, "Kluster Source Viewer")
        
        credential = PostgreSQLCredential(password='ASDasd123')
        klustr_dao = PostgreSQLKlustRDAO(credential)
        layout.add_widget(KlustRDataSourceViewWidget(klustr_dao))
        self.tab_klstr_widget.set_layout(layout)

    def get_classication_widget(self):
        conteneur_principal = QHBoxLayout()
        conteneur_widget = QVBoxLayout()
        conteneur_graphique_3d = QLabel()
        conteneur_graphique_3d.set_fixed_size(QSize(500,500))
        button_about = QPushButton("About")
        

        conteneur_widget.add_widget(Dataset_Widget())
        conteneur_widget.add_widget(Singletest_widget())
        conteneur_widget.add_widget(Knnparameters_widget())
        conteneur_widget.add_widget(button_about)
        conteneur_principal.add_layout(conteneur_widget)
        conteneur_principal.add_widget(conteneur_graphique_3d)
    
        
        self.tab_classification_widget.set_layout(conteneur_principal)


        



        

class Main_window(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.set_central_widget(Tab_widget())        

if __name__ == '__main__':
    app = QApplication(sys.argv)


    main_window = Main_window()
    main_window.window_title = 'Main'
    main_window.show()
    sys.exit(app.exec_())    
