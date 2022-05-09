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
        self.credential = None
        self.klustr_dao = None
        self.dataset_list = None

        self.set_credentials()
        self.dataset_list = self.klustr_dao.available_datasets
        self.binary_image_list = []
        self.binary_image_tag_list = []
        

        self.main_layout = QVBoxLayout()
        self.combo_box = QComboBox()
        self.submain_layout = QVBoxLayout()
        self.container_groupbox = QGroupBox("Dataset")
        self.groupbox_layout = QHBoxLayout()

        self.included_groupbox = QGroupBox("Included Dataset")
        self.included_form_layout = QFormLayout()
        self.included_groupbox.set_layout(self.included_form_layout)

        self.label_category_count = QLabel()
        self.label_training_image_count = QLabel()
        self.label_test_image_count = QLabel()
        self.label_total_image_count = QLabel()

        self.included_form_layout.add_row("Category count:", self.label_category_count)
        self.included_form_layout.add_row("Training image count:", self.label_training_image_count)
        self.included_form_layout.add_row("Test image count:", self.label_test_image_count)
        self.included_form_layout.add_row("Total image count:", self.label_total_image_count)

        self.transformation_groupbox = QGroupBox("Transformation")
        self.transformation_form_layout = QFormLayout()
        self.transformation_groupbox.set_layout(self.transformation_form_layout)

        self.label_translated = QLabel()
        self.label_rotated = QLabel()
        self.label_scaled = QLabel()

        self.transformation_form_layout.add_row("Translated :", self.label_translated)
        self.transformation_form_layout.add_row("Rotated :", self.label_rotated)
        self.transformation_form_layout.add_row("Scaled :", self.label_scaled)
        

        self.included_formlayout = QFormLayout()
        self.transformation_formlayout = QFormLayout()
        self.included_groupbox.set_layout(self.included_formlayout)
        self.transformation_groupbox.set_layout(self.transformation_formlayout)
        self.groupbox_layout.add_widget(self.included_groupbox)
        self.groupbox_layout.add_widget(self.transformation_groupbox)

        self.submain_layout.add_widget(self.combo_box)
        self.submain_layout.add_layout(self.groupbox_layout)

        self.container_groupbox.set_layout(self.submain_layout)
        self.main_layout.add_widget(self.container_groupbox)
        self.set_layout(self.main_layout) 

        self.populate_combo_box()
        self.update_infos()
        self.combo_box.currentTextChanged.connect(self.update_infos)

    @Slot()
    def update_infos(self):

        self.label_category_count.text = f'''{self.category_count}'''
        self.label_training_image_count.text = f'''{self.training_image_count}'''
        self.label_test_image_count.text = f'''{self.test_image_count}'''
        self.label_total_image_count.text = f'''{self.total_image_count}'''
        self.label_translated.text = f'''{self.translated}'''            
        self.label_rotated.text  =  f'''{self.rotated}'''
        self.label_scaled.text = f'''{self.scaled}'''
        
        self.generate_training_image_list(self.name_image)
        self.generate_training_image_tag_list(self.name_image)
        self.dataset_changed.emit(self.name_image)
        

    def populate_combo_box(self):
        for i in range(len(self.dataset_list)):
            self.combo_box.add_item(self.dataset_list[i][1] + " [" + f'''{self.dataset_list[i][5]}''' +"]"+ "[" + f'''{self.dataset_list[i][8]}''' +"] ")
        self.update_infos

    def generate_training_image_list(self, name_image):
        self.binary_image_list.clear()
        for i in self.klustr_dao.image_from_dataset(name_image, True):
            image = qimage_argb32_from_png_decoding(i[6])
            self.binary_image_list.append(ndarray_from_qimage_argb32(image))
    
    def generate_training_image_tag_list(self, name_image):
        self.binary_image_tag_list.clear()
        for i in self.klustr_dao.image_from_dataset(name_image, True):
            self.binary_image_tag_list.append(i[3])


    def set_credentials(self):
        self.credential = PostgreSQLCredential(password='ASDasd123')
        self.klustr_dao = PostgreSQLKlustRDAO(self.credential)
        self.source_data_widget = KlustRDataSourceViewWidget(self.klustr_dao)

    @property
    def name_image(self):
        return self.dataset_list[self.combo_box.current_index][1]
    @property
    def category_count(self):
        return self.dataset_list[self.combo_box.current_index][5]
    @property
    def training_image_count(self):
        return self.dataset_list[self.combo_box.current_index][6]
    @property
    def test_image_count(self):
        return self.dataset_list[self.combo_box.current_index][7]
    @property
    def total_image_count(self):
        return self.dataset_list[self.combo_box.current_index][8]
    @property
    def translated(self):
        return self.dataset_list[self.combo_box.current_index][2]
    @property
    def rotated(self):
        return self.dataset_list[self.combo_box.current_index][3]
    @property
    def scaled(self):
        return self.dataset_list[self.combo_box.current_index][4]
    @property
    def image_converted_to_binary(self):
        return self.binary_image_list
    @property
    def tag_list_of_converted_image(self):
        return self.binary_image_tag_list





                   


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Dataset_Widget()
    demo.window_title = 'Main'
    demo.show()
    sys.exit(app.exec_())  
