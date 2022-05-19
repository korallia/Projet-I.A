import sys
from matplot import MPLApp

from db_credential import PostgreSQLCredential
from klustr_dao import PostgreSQLKlustRDAO
from klustr_utils import qimage_argb32_from_png_decoding
from klustr_widget import KlustRDataSourceViewWidget
from dataset_widget import Dataset_Widget
from singletest_widget import Singletest_widget
from knnparameters_widget import Knnparameters_widget
from ImageProcessing import Image_Processor
from KNN import KNN

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
        self.__tab_klstr_widget = QWidget()
        self.__tab_classification_widget = QWidget()
        self.add_tab(self.__tab_klstr_widget, "Kluster Source Viewer")
        self.add_tab(self.__tab_classification_widget, "KNN Image Classification")
        self.create_classication_widget()
        self.create_klstr_widget()
        

    def create_klstr_widget(self):
        layout  = QVBoxLayout()
        self.set_tab_text(0, "Kluster Source Viewer")
        layout.add_widget(KlustRDataSourceViewWidget(self.__dataset_widget.klustr_dao))
        self.__tab_klstr_widget.set_layout(layout)

    def create_classication_widget(self):
        self.__dataset_widget = Dataset_Widget()
        self.__single_test_widget = Singletest_widget()
        self.__knnparameters_widget = Knnparameters_widget()
        self.__conteneur_principal = QHBoxLayout()
        self.__conteneur_widget = QVBoxLayout()
        self.__conteneur_graphique_3d = QLabel()
        self.__conteneur_graphique_3d.set_fixed_size(QSize(500,500))
        self.__conteneur_graphique_3d = MPLApp(3)
        self.__button_about = QPushButton("About")

        self.__conteneur_widget.add_widget(self.__dataset_widget)
        self.__conteneur_widget.add_widget(self.__single_test_widget)
        self.__conteneur_widget.add_widget(self.__knnparameters_widget)
        self.__conteneur_widget.add_widget(self.__button_about)
        self.__conteneur_principal.add_layout(self.__conteneur_widget)
        self.__conteneur_principal.add_widget(self.__conteneur_graphique_3d)
    
        self.__tab_classification_widget.set_layout(self.__conteneur_principal)

    @property
    def dataset_widget(self):
        return self.__dataset_widget

    @property
    def single_test_widget(self):
        return self.__single_test_widget    
    
    @property
    def knnparameters_widget(self):
        return self.__knnparameters_widget    

    @property
    def conteneur_graphique_3d(self):
        return self.__conteneur_graphique_3d 

class Main_window(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__image_tag_list = []
        self.__binary_image_list = []
        self.__image_to_identify = None

        self.__KNN = KNN()
        self.__image_processor = Image_Processor()

        self.__tab_widget = Tab_widget()
        self.__tab_widget.dataset_widget.dataset_changed.connect(self.__tab_widget.single_test_widget.change_dataset)
        self.__tab_widget.dataset_widget.dataset_changed.connect(self.get_dataset_info)
        self.__tab_widget.single_test_widget.image_binaire_changed.connect(self.get_image_to_classify)
        self.__tab_widget.single_test_widget.classify_button.clicked.connect(self.classify_test_image)
        self.__tab_widget.knnparameters_widget.nb_voisins_changed.connect(self.actualize_knn_parameters)
        self.__tab_widget.knnparameters_widget.max_distance_changed.connect(self.actualize_knn_parameters)

        self.set_central_widget(self.__tab_widget)  

    def get_dataset_info(self):
        self.__image_tag_list = self.__tab_widget.dataset_widget.binary_image_tag_list
        self.__binary_image_list = self.__tab_widget.dataset_widget.binary_image_list
        self.__image_processor.load_practice_images(self.__binary_image_list, list(self.__tab_widget.dataset_widget.tag_list_indexes.keys()), self.__KNN)
        self.__tab_widget.conteneur_graphique_3d.training_image_dataset = self.__KNN.espace_solution

    def get_image_to_classify(self):
        self.__image_to_classify = self.__tab_widget.single_test_widget.image_binaire

    def actualize_knn_parameters(self):
        knn_nb_voisins = self.__tab_widget.knnparameters_widget.nb_voisins
        knn_max_distance = self.__tab_widget.knnparameters_widget.max_distance
        self.__KNN.nbr_voisins =  knn_nb_voisins
        self.__KNN.max_distance = knn_max_distance

    def classify_test_image(self):
        self.__image_to_classify = self.__tab_widget.single_test_widget.image_binaire
        image_processee = self.__image_processor.process_unknown_image(self.__image_to_classify, self.__KNN)
        tag = self.__tab_widget.dataset_widget.tag_list_indexes[image_processee[3]]
        self.__tab_widget.single_test_widget.label_text.text = tag
        self.__tab_widget.conteneur_graphique_3d.image_test = image_processee[0:3]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main_window()
    main_window.get_dataset_info()
    main_window.window_title = 'Main'
    main_window.show()
    sys.exit(app.exec_())    
