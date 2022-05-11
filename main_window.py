import sys
from matplot import MPLApp

from db_credential import PostgreSQLCredential
from klustr_dao import PostgreSQLKlustRDAO
from klustr_utils import qimage_argb32_from_png_decoding
from klustr_widget import KlustRDataSourceViewWidget
from dataset_widget import Dataset_Widget
from singletest_widget import Singletest_widget
from knnparameters_widget import Knnparameters_widget
from mpl_scatter_plot import MPL_Scatter_plot
from ImageProcessing import image_processe
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
        self.dataset_widget = Dataset_Widget()
        self.single_test_widget = Singletest_widget()
        self.knnparameters_widget = Knnparameters_widget()
        conteneur_principal = QHBoxLayout()
        conteneur_widget = QVBoxLayout()
        self.conteneur_graphique_3d = QLabel()
        self.conteneur_graphique_3d.set_fixed_size(QSize(500,500))
        self.conteneur_graphique_3d = MPLApp(3)

        button_about = QPushButton("About")

        conteneur_widget.add_widget(self.dataset_widget)
        conteneur_widget.add_widget(self.single_test_widget)
        conteneur_widget.add_widget(self.knnparameters_widget)
        conteneur_widget.add_widget(button_about)
        conteneur_principal.add_layout(conteneur_widget)
        conteneur_principal.add_widget(self.conteneur_graphique_3d)
    
        
        self.tab_classification_widget.set_layout(conteneur_principal)

        

class Main_window(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.tag_image_list = []
        self.binary_image_list = []
        self.image_to_identify = None
        self.knn_value = None
        self.knn_max_dist_value = None
        self.KNN = KNN()
        self.image_processor = image_processe()

        self.tab_widget = Tab_widget()
        self.tab_widget.dataset_widget.dataset_changed.connect(self.tab_widget.single_test_widget.change_dataset)
        self.tab_widget.dataset_widget.dataset_changed.connect(self.get_infos_knn_from_dataset)

        self.tab_widget.single_test_widget.image_binaire_etat.connect(self.get_infos_knn_from_singletest)
        self.tab_widget.single_test_widget.classify_button.clicked.connect(self.knn_function_placeholder)


        self.tab_widget.knnparameters_widget.knn_changed.connect(self.get_infos_knn_parameters)
        self.tab_widget.knnparameters_widget.max_dist_changed.connect(self.get_infos_knn_parameters)


        self.set_central_widget(self.tab_widget)  

    def get_infos_knn_from_dataset(self):
        self.tag_image_list = self.tab_widget.dataset_widget.tag_list_of_converted_image
        self.binary_image_list = self.tab_widget.dataset_widget.image_converted_to_binary
        self.tag_dictionary = self.tab_widget.dataset_widget.tag_list_dictionary
        print(self.tag_image_list)
        print(self.binary_image_list)
        self.image_processor.load_practice_images(self.binary_image_list, list(self.tag_dictionary.keys()), self.KNN)
        self.tab_widget.conteneur_graphique_3d.training_dataset = self.KNN.espace_solution
       
        

    def get_infos_knn_from_singletest(self):
        self.image_to_identify = self.tab_widget.single_test_widget.current_binary_image
        print(self.image_to_identify)
        pass

    def get_infos_knn_parameters(self):
        self.knn_value = self.tab_widget.knnparameters_widget.knn_actual_value
        self.knn_max_dist_value = self.tab_widget.knnparameters_widget.knn_max_dist
        #print(self.knn_value)
        #print(self.knn_max_dist_value)
        self.KNN.nbr_voisins = self.knn_value
        self.KNN.max_distance = self.knn_max_dist_value

    def knn_function_placeholder(self):
        #intervient quand classify is clicked
        self.image_to_identify = self.tab_widget.single_test_widget.current_binary_image
        id = self.image_processor.process_unknown_image(self.image_to_identify, self.KNN)
        tag = self.tag_dictionary[id]
        print(tag)
        self.tab_widget.single_test_widget.label_text.text = tag
        print("VIEUX CHIEN VACHE")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)


    main_window = Main_window()
    main_window.get_infos_knn_from_dataset()
    main_window.window_title = 'Main'
    main_window.show()
    sys.exit(app.exec_())    
