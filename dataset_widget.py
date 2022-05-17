import sys
import klustr_dao

from db_credential import PostgreSQLCredential
from klustr_dao import PostgreSQLKlustRDAO
from klustr_utils import qimage_argb32_from_png_decoding, ndarray_from_qimage_argb32
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

    dataset_changed = Signal(str)

    def __init__(self, parent = None):
        super().__init__(parent)

        self.klustr_dao = None
        self.dataset_list = None
        self.__binary_image_list = []
        self.__binary_image_tag_list = []
        self.__tag_list_indexes = {}

        self.__set_credentials()
        
        self.__main_layout = QVBoxLayout()
        self.__submain_layout = QVBoxLayout()
        self.__container_groupbox = QGroupBox("Dataset")
        self.__groupbox_layout = QHBoxLayout()

        self.__combo_box = QComboBox()

        self.__included_dataset_groupbox = QGroupBox("Included Dataset")
        self.__included_dataset_form_layout = QFormLayout()
        self.__label_category_count = QLabel()
        self.__label_training_image_count = QLabel()
        self.__label_test_image_count = QLabel()
        self.__label_total_image_count = QLabel()
        self.__included_dataset_groupbox.set_layout(self.__included_dataset_form_layout)
        self.__included_dataset_form_layout.add_row("Category count:", self.__label_category_count)
        self.__included_dataset_form_layout.add_row("Training image count:", self.__label_training_image_count)
        self.__included_dataset_form_layout.add_row("Test image count:", self.__label_test_image_count)
        self.__included_dataset_form_layout.add_row("Total image count:", self.__label_total_image_count)

        self.__transformation_groupbox = QGroupBox("Transformation")
        self.__transformation_form_layout = QFormLayout()
        self.__transformation_groupbox.set_layout(self.__transformation_form_layout)
        self.__label_translated = QLabel()
        self.__label_rotated = QLabel()
        self.__label_scaled = QLabel()  
        self.__transformation_form_layout.add_row("Translated :", self.__label_translated)
        self.__transformation_form_layout.add_row("Rotated :", self.__label_rotated)
        self.__transformation_form_layout.add_row("Scaled :", self.__label_scaled)
        
        self.__groupbox_layout.add_widget(self.__included_dataset_groupbox)
        self.__groupbox_layout.add_widget(self.__transformation_groupbox)

        self.__submain_layout.add_widget(self.__combo_box)
        self.__submain_layout.add_layout(self.__groupbox_layout)

        self.__container_groupbox.set_layout(self.__submain_layout)
        self.__main_layout.add_widget(self.__container_groupbox)

        self.set_layout(self.__main_layout) 

        self.__populate_combo_box()
        self.__combo_box.currentTextChanged.connect(self.update_infos)
        


    @Slot()
    def update_infos(self):

        self.__label_category_count.text = f'''{self.category_count}'''
        self.__label_training_image_count.text = f'''{self.training_image_count}'''
        self.__label_test_image_count.text = f'''{self.test_image_count}'''
        self.__label_total_image_count.text = f'''{self.total_image_count}'''
        self.__label_translated.text = f'''{self.translated}'''            
        self.__label_rotated.text  =  f'''{self.rotated}'''
        self.__label_scaled.text = f'''{self.scaled}'''
        
        self.__generate_training_image_list(self.dataset_name)
        self.__generate_training_image_tag_list(self.dataset_name)
        self.dataset_changed.emit(self.dataset_name)
        

    def __populate_combo_box(self):
        for i in range(len(self.dataset_list)):
            self.__combo_box.add_item(self.dataset_list[i][1] + " [" + f'''{self.dataset_list[i][5]}''' +"]"+ "[" + f'''{self.dataset_list[i][8]}''' +"] ")
        self.update_infos()

    def __generate_training_image_list(self, name_image):
        self.__binary_image_list.clear()
        for i in self.klustr_dao.image_from_dataset(name_image, True):
            image = qimage_argb32_from_png_decoding(i[6])
            self.__binary_image_list.append(ndarray_from_qimage_argb32(image))
    
    def __generate_training_image_tag_list(self, name_image):
        self.__binary_image_tag_list.clear()
        self.__tag_list_indexes.clear()
        for i in self.klustr_dao.image_from_dataset(name_image, True):
            self.__binary_image_tag_list.append(i[3])
            self.__tag_list_indexes[i[2]] = i[3]

        
    def __set_credentials(self):
        
        credential = PostgreSQLCredential(password='ASDasd123')
        self.klustr_dao = PostgreSQLKlustRDAO(credential)
        self.dataset_list = self.klustr_dao.available_datasets

    @property
    def dataset_name(self):
        return self.dataset_list[self.__combo_box.current_index][1]

    @property
    def category_count(self):
        return self.dataset_list[self.__combo_box.current_index][5]
    @property
    def training_image_count(self):
        return self.dataset_list[self.__combo_box.current_index][6]
    @property
    def test_image_count(self):
        return self.dataset_list[self.__combo_box.current_index][7]
    @property
    def total_image_count(self):
        return self.dataset_list[self.__combo_box.current_index][8]
    @property
    def translated(self):
        return self.dataset_list[self.__combo_box.current_index][2]
    @property
    def rotated(self):
        return self.dataset_list[self.__combo_box.current_index][3]
    @property
    def scaled(self):
        return self.dataset_list[self.__combo_box.current_index][4]
    @property
    def binary_image_list(self):
        return self.__binary_image_list
    @property
    def binary_image_tag_list(self):
        return self.__binary_image_tag_list

    @property
    def tag_list_indexes(self):
        return self.__tag_list_indexes




                   


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Dataset_Widget()
    demo.window_title = 'Main'
    demo.show()
    sys.exit(app.exec_())  
