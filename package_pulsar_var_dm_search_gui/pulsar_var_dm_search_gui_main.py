from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLabel
from PyQt5.QtWidgets import QTabWidget, QPushButton, QDoubleSpinBox, QAbstractSpinBox, QRadioButton, QLineEdit
from PyQt5.QtWidgets import QFileDialog, QPlainTextEdit, QSlider, QCheckBox, QComboBox, QSizePolicy
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import *

from threading import *
import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pylab
from os import path
import numpy as np
import struct
import scipy
import shutil
import sys
import os

# To change system path to the directory where script is running:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_pulsar_profile_analysis_gui.f_calculate_spectrum_of_profile import calculate_spectrum_of_profile
from package_pulsar_var_dm_search_gui.f_make_var_dm_file_from_jds import make_var_dm_file_from_jds
from package_pulsar_profile_analysis_gui.f_make_transient_profile_from_jds_file_pairs import (
    f_make_transient_profile_from_jds_file_pairs)

# from package_common_modules.text_manipulations import read_one_value_txt_file
# from package_ra_data_processing.filtering import median_filter


# Keep in mind that for Linux (Ubuntu 22.04) you may will need to use headless opencv:
# pip uninstall opencv-python
# pip install opencv-python-headless

software_version = '2025.01.05'


# Main window
class Window(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window geometry and hierarchy
        self.setWindowTitle('Pulsar & transient search    v.' + software_version + '    Serge Yerin @ IRA NASU')  # Win title
        self.setGeometry(100, 100, 1300, 700)
        # menu_bar = self.menuBar()
        # file_menu = menu_bar.addMenu('&File')

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Preprocess JDS data")
        self.tabs.addTab(self.tab2, "Data in time domain")
        self.tabs.addTab(self.tab3, "Data in spectral domain")
        self.tabs.addTab(self.tab4, "Spectral domain analysis")
        self.tabs.addTab(self.tab5, "Spectrum of spectrum")

        self.time_resolution = (1 / 66000000) * 16384 * 32  # Data time resolution, s   # 0.007944





        ##############################
        #         First tab          #
        ##############################

        # First tab
        self.tab1.layout = QGridLayout(self.tab1)

        # First tab raw one
        self.radiobutton_txt = QRadioButton("Ready var DM .vdm file: ")
        self.radiobutton_txt.setChecked(True)
        self.radiobutton_txt.process_type = "vdm file only"
        self.radiobutton_txt.toggled.connect(self.rb_txt_on_click)
        self.tab1.layout.addWidget(self.radiobutton_txt, 0, 0)

        # Path to txt file line
        self.vdm_file_path_line = QLineEdit()  # self, placeholderText='Enter a keyword to search...'

        common_path = '../RA_DATA_ARCHIVE/ADDITIONAL_var_DM_files/'
        filename = 'Transient_P130422_121607.jds_Data_chA_var_DM_4.255-7.255.vdm'
        self.vdm_filepath, self.vdm_filename = common_path, filename

        self.vdm_file_path_line.setText(common_path + filename)
        self.tab1.layout.addWidget(self.vdm_file_path_line, 0, 1)

        # Button "Open txt file"
        self.button_open_vdm = QPushButton('Open .vdm file')
        self.button_open_vdm.clicked.connect(self.one_vdm_file_dialog)  # adding action to the button
        self.button_open_vdm.setFixedSize(QSize(150, 30))
        self.tab1.layout.addWidget(self.button_open_vdm, 0, 2)

        # Label with further instructions
        self.label_vdm_file_selected = QLabel('After selecting correct .vdm file, you can switch to ' +
                                              'the second tab "Analyze profile" and begin analysis', self)
        self.tab1.layout.addWidget(self.label_vdm_file_selected, 1, 1)

        # Added empty label to separate workflows
        self.empty_label = QLabel(' ', self)
        self.tab1.layout.addWidget(self.empty_label, 2, 1)


        # First tab second part
        self.radiobutton_jds = QRadioButton("Raw .jds files preprocess:")
        self.radiobutton_jds.process_type = "raw jds files"
        self.radiobutton_jds.toggled.connect(self.rb_jds_on_click)
        self.tab1.layout.addWidget(self.radiobutton_jds, 3, 0, Qt.AlignTop)

        # Line for txt file path
        self.jds_file_path_line = QPlainTextEdit()
        self.jds_file_path_line.setEnabled(False)
        self.tab1.layout.addWidget(self.jds_file_path_line, 3, 1)

        # Button "Open jds file"
        self.button_open_jds = QPushButton('Open jds files')
        self.button_open_jds.clicked.connect(self.jds_files_open_dialog)  # adding action to the button
        self.button_open_jds.setFixedSize(QSize(150, 30))
        self.button_open_jds.setEnabled(False)
        self.tab1.layout.addWidget(self.button_open_jds, 3, 2, Qt.AlignTop)

        # Path to result folder line
        self.result_path_line = QLineEdit()
        self.result_path_line.setEnabled(False)
        self.tab1.layout.addWidget(self.result_path_line, 4, 1)

        # Button "Specify result folder"
        self.button_select_result_path = QPushButton('Specify result folder')
        self.button_select_result_path.clicked.connect(self.specify_result_folder_dialog)  # adding action to the button
        self.button_select_result_path.setFixedSize(QSize(150, 30))
        self.button_select_result_path.setEnabled(False)
        self.tab1.layout.addWidget(self.button_select_result_path, 4, 2)




        # Nested horizontal layout for DM entry
        self.dm_entry_layout = QHBoxLayout()

        self.label_dm_dummy_entry = QLabel(" ", self)
        self.label_dm_dummy_entry.setEnabled(False)
        self.label_dm_dummy_entry.setFixedSize(QSize(140, 30))
        self.dm_entry_layout.addWidget(self.label_dm_dummy_entry)

        self.label_dm_entry = QLabel("Central DM: ", self)
        self.label_dm_entry.setEnabled(False)
        self.label_dm_entry.setFixedSize(QSize(80, 30))
        self.dm_entry_layout.addWidget(self.label_dm_entry)

        # Entry of DM value
        self.line_dm_entry = QLineEdit()
        self.line_dm_entry.setText('5.755')
        self.line_dm_entry.setFixedSize(QSize(60, 30))
        self.line_dm_entry.setEnabled(False)
        self.dm_entry_layout.addWidget(self.line_dm_entry)

        self.label_dm_units = QLabel(f' pc/cm\N{SUPERSCRIPT THREE}', self)
        self.label_dm_units.setFixedSize(QSize(80, 30))
        self.label_dm_units.setEnabled(False)
        self.dm_entry_layout.addWidget(self.label_dm_units)


        self.label_dm_range_entry = QLabel("  DM range: ±", self)
        self.label_dm_range_entry.setEnabled(False)
        self.label_dm_range_entry.setFixedSize(QSize(80, 30))
        self.dm_entry_layout.addWidget(self.label_dm_range_entry)

        # Entry of DM range value
        self.line_dm_range_entry = QLineEdit()
        self.line_dm_range_entry.setText('0.5')
        self.line_dm_range_entry.setFixedSize(QSize(60, 30))
        self.line_dm_range_entry.setEnabled(False)
        self.dm_entry_layout.addWidget(self.line_dm_range_entry)

        self.label_dm_range_units = QLabel(f' pc/cm\N{SUPERSCRIPT THREE}', self)
        self.label_dm_range_units.setFixedSize(QSize(80, 30))
        self.label_dm_range_units.setEnabled(False)
        self.dm_entry_layout.addWidget(self.label_dm_range_units)


        self.label_dm_points_entry = QLabel("  Points (odd): ", self)
        self.label_dm_points_entry.setEnabled(False)
        self.label_dm_points_entry.setFixedSize(QSize(80, 30))
        self.dm_entry_layout.addWidget(self.label_dm_points_entry)

        # Entry of DM range value
        self.line_dm_points_entry = QLineEdit()
        self.line_dm_points_entry.setText('101')
        self.line_dm_points_entry.setFixedSize(QSize(60, 30))
        self.line_dm_points_entry.setEnabled(False)
        self.dm_entry_layout.addWidget(self.line_dm_points_entry)


        self.label_dm_dummy2_entry = QLabel(" ", self)
        self.label_dm_dummy2_entry.setEnabled(False)
        self.label_dm_dummy2_entry.setFixedSize(QSize(80, 30))
        self.dm_entry_layout.addWidget(self.label_dm_dummy2_entry)

        # Add nested horizontal layout to the main one
        self.tab1.layout.addLayout(self.dm_entry_layout, 5, 1)



        # Nested horizontal layout for DM entry
        self.dm_calc_layout = QHBoxLayout()

        # Button "Calculate DM values"
        self.button_calc_dm = QPushButton('Calculate DM values')
        self.button_calc_dm.clicked.connect(self.calculate_dm_values)
        self.button_calc_dm.setEnabled(False)
        self.button_calc_dm.setFixedSize(QSize(140, 25))
        self.dm_calc_layout.addWidget(self.button_calc_dm)

        self.label_dm_start = QLabel("DM start:", self)
        self.label_dm_start.setEnabled(False)
        self.label_dm_start.setFixedSize(QSize(80, 30))
        self.dm_calc_layout.addWidget(self.label_dm_start)

        # Entry of DM value
        self.line_start_dm_entry = QLineEdit()
        self.line_start_dm_entry.setText('0.0')
        self.line_start_dm_entry.setFixedSize(QSize(60, 30))
        self.line_start_dm_entry.setEnabled(False)
        self.dm_calc_layout.addWidget(self.line_start_dm_entry)

        self.label_stert_dm_unit = QLabel(f' pc/cm\N{SUPERSCRIPT THREE}', self)
        self.label_stert_dm_unit.setFixedSize(QSize(80, 30))
        self.label_stert_dm_unit.setEnabled(False)
        self.dm_calc_layout.addWidget(self.label_stert_dm_unit)


        self.label_dm_step_entry = QLabel("  DM step:", self)
        self.label_dm_step_entry.setEnabled(False)
        self.label_dm_step_entry.setFixedSize(QSize(80, 30))
        self.dm_calc_layout.addWidget(self.label_dm_step_entry)

        # Entry of DM range value
        self.line_dm_step_entry = QLineEdit()
        self.line_dm_step_entry.setText('0.0')
        self.line_dm_step_entry.setFixedSize(QSize(60, 30))
        self.line_dm_step_entry.setEnabled(False)
        self.dm_calc_layout.addWidget(self.line_dm_step_entry)

        self.label_dm_step_units = QLabel(f' pc/cm\N{SUPERSCRIPT THREE}', self)
        self.label_dm_step_units.setFixedSize(QSize(80, 30))
        self.label_dm_step_units.setEnabled(False)
        self.dm_calc_layout.addWidget(self.label_dm_step_units)


        self.label_dm_stop_entry = QLabel("  DM stop: ", self)
        self.label_dm_stop_entry.setEnabled(False)
        self.label_dm_stop_entry.setFixedSize(QSize(80, 30))
        self.dm_calc_layout.addWidget(self.label_dm_stop_entry)

        # Entry of DM range value
        self.line_dm_stop_entry = QLineEdit()
        self.line_dm_stop_entry.setText('0.0')
        self.line_dm_stop_entry.setFixedSize(QSize(60, 30))
        self.line_dm_stop_entry.setEnabled(False)
        self.dm_calc_layout.addWidget(self.line_dm_stop_entry)

        self.label_dm_stop_units = QLabel(f' pc/cm\N{SUPERSCRIPT THREE}', self)
        self.label_dm_stop_units.setFixedSize(QSize(80, 30))
        self.label_dm_stop_units.setEnabled(False)
        self.dm_calc_layout.addWidget(self.label_dm_stop_units)

        # Add nested horizontal layout to the main one
        self.tab1.layout.addLayout(self.dm_calc_layout, 6, 1)




        # Nested horizontal layout for processing parameters entry
        self.proc_param_entry_layout = QHBoxLayout()

        self.label_dm_dummy_entry_1 = QLabel(" ", self)
        self.label_dm_dummy_entry_1.setEnabled(False)
        self.label_dm_dummy_entry_1.setFixedSize(QSize(140, 30))
        self.proc_param_entry_layout.addWidget(self.label_dm_dummy_entry_1)

        self.label_data_channels_entry = QLabel("Channels: ", self)
        self.label_data_channels_entry.setFixedSize(QSize(80, 30))
        self.label_data_channels_entry.setEnabled(False)
        self.proc_param_entry_layout.addWidget(self.label_data_channels_entry)

        self.channel_select_dropdown = QComboBox(self)
        self.channel_select_dropdown.addItem("A")
        self.channel_select_dropdown.addItem("B")
        self.channel_select_dropdown.addItem("A & B")
        self.channel_select_dropdown.move(50, 50)
        self.channel_select_dropdown.setFixedSize(QSize(60, 30))
        self.channel_select_dropdown.setEnabled(False)
        self.proc_param_entry_layout.addWidget(self.channel_select_dropdown)


        self.label_channels_dummy_1 = QLabel(' ', self)
        self.label_channels_dummy_1.setFixedSize(QSize(80, 30))
        self.label_channels_dummy_1.setEnabled(False)
        self.proc_param_entry_layout.addWidget(self.label_channels_dummy_1)

        self.label_channels_dummy_2 = QLabel(' ', self)
        self.label_channels_dummy_2.setFixedSize(QSize(80, 30))
        self.label_channels_dummy_2.setEnabled(False)
        self.proc_param_entry_layout.addWidget(self.label_channels_dummy_2)

        self.label_channels_dummy_3 = QLabel(' ', self)
        self.label_channels_dummy_3.setFixedSize(QSize(60, 30))
        self.label_channels_dummy_3.setEnabled(False)
        self.proc_param_entry_layout.addWidget(self.label_channels_dummy_3)

        self.label_channels_dummy_4 = QLabel(' ', self)
        self.label_channels_dummy_4.setFixedSize(QSize(20, 30))
        self.label_channels_dummy_4.setEnabled(False)
        self.proc_param_entry_layout.addWidget(self.label_channels_dummy_4)

        self.label_no_of_processes_entry = QLabel("  Number of processes: ", self)
        self.label_no_of_processes_entry.setEnabled(False)
        self.label_no_of_processes_entry.setFixedSize(QSize(140, 30))
        self.label_no_of_processes_entry.setEnabled(False)
        self.proc_param_entry_layout.addWidget(self.label_no_of_processes_entry)

        self.process_no_select_dropdown = QComboBox(self)
        # self.process_no_select_dropdown.addItem("1")
        # self.process_no_select_dropdown.addItem("2")
        # self.process_no_select_dropdown.addItem("3")
        # self.process_no_select_dropdown.addItem("4")
        # self.process_no_select_dropdown.addItem("5")
        # self.process_no_select_dropdown.addItem("6")
        # self.process_no_select_dropdown.addItem("7")
        processes_number_list = ["1", "2", "3", "4", "5", "6", "7"]
        self.process_no_select_dropdown.addItems(processes_number_list)
        self.process_no_select_dropdown.move(50, 50)
        self.process_no_select_dropdown.setFixedSize(QSize(60, 30))
        self.process_no_select_dropdown.setEnabled(False)
        self.proc_param_entry_layout.addWidget(self.process_no_select_dropdown)

        self.label_processes_no_dummy = QLabel(' ', self)
        self.label_processes_no_dummy.setFixedSize(QSize(80, 30))
        self.label_processes_no_dummy.setEnabled(False)
        self.proc_param_entry_layout.addWidget(self.label_processes_no_dummy)

        # Add nested horizontal layout to the main one
        self.tab1.layout.addLayout(self.proc_param_entry_layout, 7, 1)







        # Button "Preprocess jds files"
        self.button_process_jds = QPushButton('Preprocess jds files')
        self.button_process_jds.clicked.connect(self.thread_preprocess_jds_files)  # adding action to the button
        self.button_process_jds.setEnabled(False)
        self.tab1.layout.addWidget(self.button_process_jds, 8, 1, Qt.AlignTop)

        # JDS processing status label
        self.label_processing_status = QLabel('', self)
        self.label_processing_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_processing_status.setFont(QFont('Arial', 14))
        self.tab1.layout.addWidget(self.label_processing_status, 9, 1)



        # First tab third part
        self.radiobutton_pairs = QRadioButton("Raw .jds pairs preprocess:")
        self.radiobutton_pairs.process_type = "raw jds pairs files"
        self.radiobutton_pairs.toggled.connect(self.rb_pairs_on_click)
        self.tab1.layout.addWidget(self.radiobutton_pairs, 10, 0)  # , Qt.AlignTop

        # Path to source folder line
        self.source_pairs_path_line = QLineEdit()
        self.source_pairs_path_line.setEnabled(False)
        self.tab1.layout.addWidget(self.source_pairs_path_line, 10, 1)

        # Button "Specify result folder"
        self.button_select_pairs_source_path = QPushButton('Specify source folder')
        self.button_select_pairs_source_path.clicked.connect(self.specify_source_pairs_folder_dialog)  # add new action!!!
        self.button_select_pairs_source_path.setFixedSize(QSize(150, 30))
        self.button_select_pairs_source_path.setEnabled(False)
        self.tab1.layout.addWidget(self.button_select_pairs_source_path, 10, 2)

        # Path to result folder line
        self.result_pairs_path_line = QLineEdit()
        self.result_pairs_path_line.setEnabled(False)
        self.tab1.layout.addWidget(self.result_pairs_path_line, 11, 1)

        # Button "Specify result folder"
        self.button_select_pairs_result_path = QPushButton('Specify result folder')
        self.button_select_pairs_result_path.clicked.connect(self.specify_result_pairs_folder_dialog)  # adding action
        self.button_select_pairs_result_path.setFixedSize(QSize(150, 30))
        self.button_select_pairs_result_path.setEnabled(False)
        self.tab1.layout.addWidget(self.button_select_pairs_result_path, 11, 2)

        # Nested horizontal layout for DM entry
        self.pairs_dm_entry_layout = QHBoxLayout()

        self.label_pairs_dm_entry = QLabel("Source dispersion measure (DM):", self)
        self.label_pairs_dm_entry.setEnabled(False)
        self.label_pairs_dm_entry.setFixedSize(QSize(160, 30))
        self.pairs_dm_entry_layout.addWidget(self.label_pairs_dm_entry)

        # Entry of DM value
        self.line_pairs_dm_entry = QLineEdit()
        self.line_pairs_dm_entry.setText('5.755')
        self.line_pairs_dm_entry.setEnabled(False)
        self.pairs_dm_entry_layout.addWidget(self.line_pairs_dm_entry)

        self.label_pairs_dm_units = QLabel(f' pc/cm\N{SUPERSCRIPT THREE}', self)
        self.label_pairs_dm_units.setFixedSize(QSize(490, 30))
        self.label_pairs_dm_units.setEnabled(False)
        self.pairs_dm_entry_layout.addWidget(self.label_pairs_dm_units)

        # Add nested horizontal layout to the main one
        self.tab1.layout.addLayout(self.pairs_dm_entry_layout, 12, 1)

        # Button "Preprocess pairs of jds files"
        self.button_process_pairs_jds = QPushButton('Preprocess pairs of jds files from specified folder')
        self.button_process_pairs_jds.clicked.connect(self.thread_preprocess_pairs_jds_files)  # adding action
        self.button_process_pairs_jds.setEnabled(False)
        self.tab1.layout.addWidget(self.button_process_pairs_jds, 13, 1, Qt.AlignTop)

        # JDS pairs processing status label
        self.label_pairs_processing_status = QLabel('', self)
        self.label_pairs_processing_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pairs_processing_status.setFont(QFont('Arial', 14))
        self.tab1.layout.addWidget(self.label_pairs_processing_status, 14, 1)



        # Adding stretch lines to get all elements pulled to top
        self.tab1.layout.setRowStretch(self.tab1.layout.rowCount(), 1)
        # self.tab1.layout.setColumnStretch(self.tab1.layout.columnCount(), 1)

        self.tab1.setLayout(self.tab1.layout)







        ##############################
        #         Second tab         #
        ##############################

        # Layouts in the second tab
        self.tab2.layout = QVBoxLayout(self.tab2)
        self.input_controls_layout_t2_l1 = QHBoxLayout()  # Line 1 of controls
        self.input_controls_layout_t2_l2 = QHBoxLayout()  # Line 2 of controls
        self.canvas_and_input_controls_layout_t2 = QHBoxLayout() 

        self.canvas_and_toolbox_left_vertical_layout_t2 = QVBoxLayout()
        # self.input_controls_left_vertical_layout_t2 = QVBoxLayout()
        # self.input_controls_right_vertical_layout_t2 = QVBoxLayout()

        self.toolbar_layout_t2 = QHBoxLayout()

        # Creating labels near spinboxes to describe the input
        self.label_median_win = QLabel("Median window:", self)
        self.label_median_win.setFixedSize(QSize(100, 30))
        self.label_median_win.setAlignment(QtCore.Qt.AlignCenter)

        # Creating labels near spinboxes to describe the input
        self.label_dummy_t2 = QLabel(" ", self)
        self.label_dummy_t2.setFixedSize(QSize(80, 30))
        self.label_dummy_t2.setAlignment(QtCore.Qt.AlignCenter)


        # Creating labels near spinboxes to describe the input
        self.label_image_amplitude_color_min_t2 = QLabel("Min color:", self)
        self.label_image_amplitude_color_min_t2.setFixedSize(QSize(70, 30))
        self.label_image_amplitude_color_min_t2.setAlignment(QtCore.Qt.AlignCenter)

        # Creating labels near spinboxes to describe the input
        self.label_image_amplitude_color_max_t2 = QLabel("Max color:", self)
        self.label_image_amplitude_color_max_t2.setFixedSize(QSize(70, 30))
        self.label_image_amplitude_color_max_t2.setAlignment(QtCore.Qt.AlignCenter)


        # Spinbox min color amplitude on figure
        self.spinbox_image_amplitude_color_min_t2 = QDoubleSpinBox()
        self.spinbox_image_amplitude_color_min_t2.setFixedSize(QSize(70, 30))
        self.spinbox_image_amplitude_color_min_t2.setMinimum(0.0)
        self.spinbox_image_amplitude_color_min_t2.setMaximum(1.0)
        self.spinbox_image_amplitude_color_min_t2.setDecimals(4) 
        self.spinbox_image_amplitude_color_min_t2.setSingleStep(0.001) 
        self.spinbox_image_amplitude_color_min_t2.setValue(0.0)

        # Spinbox max color amplitude on figure
        self.spinbox_image_amplitude_color_max_t2 = QDoubleSpinBox()
        self.spinbox_image_amplitude_color_max_t2.setFixedSize(QSize(70, 30))
        self.spinbox_image_amplitude_color_max_t2.setMinimum(0.0)
        self.spinbox_image_amplitude_color_max_t2.setMaximum(1.0)
        self.spinbox_image_amplitude_color_max_t2.setDecimals(4) 
        self.spinbox_image_amplitude_color_max_t2.setSingleStep(0.001) 
        self.spinbox_image_amplitude_color_max_t2.setValue(1.0)

        # Label dummy before chackbox
        self.label_dummy_t2l1 = QLabel(" ", self)
        self.label_dummy_t2l1.setFixedSize(QSize(5, 30))
        self.label_dummy_t2l1.setAlignment(QtCore.Qt.AlignCenter)

        # Label dummy below strachable
        self.label_dummy_t2l2 = QLabel(" ", self)
        self.label_dummy_t2l2.setFixedSize(QSize(140, 30))
        self.label_dummy_t2l2.setAlignment(QtCore.Qt.AlignCenter)


        # Labels before sliders
        self.label_cut_start_t2l1 = QLabel("Cut start:", self)
        self.label_cut_start_t2l1.setFixedSize(QSize(70, 30))
        self.label_cut_start_t2l1.setAlignment(QtCore.Qt.AlignCenter)

        self.label_cut_finish_t2l2 = QLabel("Cut finish:", self)
        self.label_cut_finish_t2l2.setFixedSize(QSize(70, 30))
        self.label_cut_finish_t2l2.setAlignment(QtCore.Qt.AlignCenter)

        # Spinbox filter window length
        self.filter_win_input = QDoubleSpinBox()
        self.filter_win_input.setFixedSize(QSize(70, 30))
        self.filter_win_input.setMinimum(0)
        self.filter_win_input.setMaximum(100000)
        self.filter_win_input.setValue(100)

        # Slider 1 - data cut
        self.slider_data_begins_at = QSlider(Qt.Horizontal)  
        self.slider_data_begins_at.setFixedSize(QSize(450, 30))
        self.slider_data_begins_at.setRange(0, 16)
        self.slider_data_begins_at.setValue(0)
        self.slider_data_begins_at.setTickPosition(QSlider.TicksAbove)
        self.slider_data_begins_at.valueChanged.connect(self.slider_data_begins_at_value_changed)
        
        # Slider 2 - data cut
        self.slider_data_finishes_at = QSlider(Qt.Horizontal)  
        self.slider_data_finishes_at.setFixedSize(QSize(450, 30))
        self.slider_data_finishes_at.setRange(0, 16)
        self.slider_data_finishes_at.setValue(16)
        self.slider_data_finishes_at.setTickPosition(QSlider.TicksBelow)
        self.slider_data_finishes_at.valueChanged.connect(self.slider_data_finishes_at_value_changed)

        # Label Slider 1
        self.label_data_begins_at = QLabel("0", self)
        self.label_data_begins_at.setFixedSize(QSize(40, 30))
        self.label_data_begins_at.setAlignment(QtCore.Qt.AlignCenter)

        # Label Slider 2
        self.label_data_finishes_at = QLabel("16", self)
        self.label_data_finishes_at.setFixedSize(QSize(40, 30))
        self.label_data_finishes_at.setAlignment(QtCore.Qt.AlignCenter)

        # Checkbox - show red dots on image
        self.checkbox_show_color_markers_t2 = QCheckBox(self)
        self.checkbox_show_color_markers_t2.setFixedSize(QSize(30, 30))
        self.checkbox_show_color_markers_t2.setChecked(True)

        # Label checkbox - show red dots on image
        self.label_checkbox_show_maxima_t2 = QLabel("Show max", self)
        self.label_checkbox_show_maxima_t2.setFixedSize(QSize(60, 30))
        self.label_checkbox_show_maxima_t2.setAlignment(QtCore.Qt.AlignCenter)


        # Main plot window
        self.figure_time = plt.figure()  # a figure instance to plot on
        self.canvas_time = FigureCanvas(self.figure_time)  # takes the 'figure' instance as a parameter to __init__

        # This is the Matplotlib Navigation widget it takes the Canvas widget and a parent
        self.toolbar_time = NavigationToolbar(self.canvas_time, self)

        # Button "Read data"
        self.button_read_time = QPushButton('Read data')
        self.button_read_time.clicked.connect(self.thread_read_initial_data)
        self.button_read_time.setFixedSize(QSize(80, 30))

        # Button "Subtract median"
        self.button_filter_time = QPushButton('Subtract median')
        self.button_filter_time.clicked.connect(self.thread_subtract_median_in_time)
        self.button_filter_time.setFixedSize(QSize(263, 30))
        self.button_filter_time.setEnabled(False)

        # Button "Cut data"
        self.button_cut_data_time = QPushButton('Cut data')
        self.button_cut_data_time.clicked.connect(self.thread_cut_initial_data_in_time)  
        self.button_cut_data_time.setFixedSize(QSize(80, 30))
        self.button_cut_data_time.setEnabled(False)

        # Button "Apply color range"
        self.button_apply_color_range_t2 = QPushButton('Apply color range')
        self.button_apply_color_range_t2.clicked.connect(self.thread_update_cut_data_with_color_amplitude_value)  
        self.button_apply_color_range_t2.setFixedSize(QSize(120, 30))
        self.button_apply_color_range_t2.setEnabled(False)

        # Work status label tab 2
        self.label_processing_status_t2 = QLabel(" ", self)
        self.label_processing_status_t2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_processing_status_t2.setFixedHeight(30)
        self.label_processing_status_t2.setFont(QFont('Arial', 14))

        # Cut index status label tab 2
        self.label_cut_index_status_t2 = QLabel(" ", self)
        self.label_cut_index_status_t2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cut_index_status_t2.setFixedHeight(30)
        self.label_cut_index_status_t2.setFont(QFont('Arial', 14))

        # Creating label to indicate the array dimensions
        self.label_array_dimensions_t2 = QLabel("DM:  0  pts,   time:  0  pts", self)
        self.label_array_dimensions_t2.setFixedSize(QSize(200, 30))
        self.label_array_dimensions_t2.setAlignment(QtCore.Qt.AlignCenter)
        
        # Creating labels to indicate the initial time resolution
        label = "Time resolution assumed: {:8.4f}".format(np.round(self.time_resolution * 1000, 6)) + "  ms."
        self.label_time_resolution = QLabel(label, self)
        self.label_time_resolution.setFixedSize(QSize(300, 30))
        self.label_time_resolution.setAlignment(QtCore.Qt.AlignCenter)

        # Packing layouts in the window line 1
        self.input_controls_layout_t2_l1.addWidget(self.button_read_time)
        self.input_controls_layout_t2_l1.addWidget(self.label_median_win)
        self.input_controls_layout_t2_l1.addWidget(self.filter_win_input)
        self.input_controls_layout_t2_l1.addWidget(self.label_cut_start_t2l1)
        self.input_controls_layout_t2_l1.addWidget(self.slider_data_begins_at)
        self.input_controls_layout_t2_l1.addWidget(self.label_data_begins_at)
        self.input_controls_layout_t2_l1.addWidget(self.label_dummy_t2)
        self.input_controls_layout_t2_l1.addWidget(self.label_image_amplitude_color_min_t2)
        self.input_controls_layout_t2_l1.addWidget(self.spinbox_image_amplitude_color_min_t2)
        self.input_controls_layout_t2_l1.addWidget(self.label_dummy_t2l1)
        self.input_controls_layout_t2_l1.addWidget(self.checkbox_show_color_markers_t2)
        self.input_controls_layout_t2_l1.addWidget(self.label_checkbox_show_maxima_t2)
        self.input_controls_layout_t2_l1.addWidget(self.label_processing_status_t2)
        
        # Packing layouts in the window line 2
        self.input_controls_layout_t2_l2.addWidget(self.button_filter_time)
        self.input_controls_layout_t2_l2.addWidget(self.label_cut_finish_t2l2)
        self.input_controls_layout_t2_l2.addWidget(self.slider_data_finishes_at)
        self.input_controls_layout_t2_l2.addWidget(self.label_data_finishes_at)
        self.input_controls_layout_t2_l2.addWidget(self.button_cut_data_time)
        self.input_controls_layout_t2_l2.addWidget(self.label_image_amplitude_color_max_t2)
        self.input_controls_layout_t2_l2.addWidget(self.spinbox_image_amplitude_color_max_t2)
        self.input_controls_layout_t2_l2.addWidget(self.button_apply_color_range_t2)
        self.input_controls_layout_t2_l2.addWidget(self.label_dummy_t2l2)
        self.input_controls_layout_t2_l2.addWidget(self.label_cut_index_status_t2)
        
        self.toolbar_layout_t2.addWidget(self.toolbar_time)
        self.toolbar_layout_t2.addWidget(self.label_array_dimensions_t2)
        self.toolbar_layout_t2.addWidget(self.label_time_resolution)

        self.canvas_and_toolbox_left_vertical_layout_t2.addLayout(self.toolbar_layout_t2)
        self.canvas_and_toolbox_left_vertical_layout_t2.addWidget(self.canvas_time, stretch=1)
        
        self.canvas_and_input_controls_layout_t2.addLayout(self.canvas_and_toolbox_left_vertical_layout_t2)

        self.tab2.layout.addLayout(self.input_controls_layout_t2_l1)
        self.tab2.layout.addLayout(self.input_controls_layout_t2_l2)
        self.tab2.layout.addLayout(self.canvas_and_input_controls_layout_t2)

        self.tab2.setLayout(self.tab2.layout)




        ##############################################
        #         Third tab - Spectral domain        #
        ##############################################

        # Layouts in the third tab
        self.tab3.layout = QVBoxLayout(self.tab3)
        self.input_controls_layout_t3_l1 = QHBoxLayout()
        self.input_controls_layout_t3_l2 = QHBoxLayout()

        # Main plot window
        self.figure_freq = plt.figure()  # a figure instance to plot on
        self.canvas_freq = FigureCanvas(self.figure_freq)  # takes the 'figure' instance as a parameter to __init__

        # This is the Matplotlib Navigation widget it takes the Canvas widget and a parent
        self.toolbar_freq = NavigationToolbar(self.canvas_freq, self)

        # Checkbox - cut data with limits
        self.checkbox_cut_data_amp_with_limits_t3 = QCheckBox(self)
        self.checkbox_cut_data_amp_with_limits_t3.setFixedSize(QSize(20, 30))
        self.checkbox_cut_data_amp_with_limits_t3.setChecked(False)

        # Label checkbox
        self.label_cut_data_amp_with_limits_t3 = QLabel("Cut data\namplitude", self)
        self.label_cut_data_amp_with_limits_t3.setFixedSize(QSize(60, 30))
        self.label_cut_data_amp_with_limits_t3.setAlignment(QtCore.Qt.AlignCenter)

        # Label dummy to align 1 and 2 lines
        self.label_dummy_align_t3_l1_1 = QLabel('', self)
        self.label_dummy_align_t3_l1_1.setFixedSize(QSize(27, 30))

        # Button "Calculate FFT"
        self.button_calc_fft = QPushButton('Calculate FFT')
        self.button_calc_fft.clicked.connect(self.thread_calculate_fft_of_data)  # adding action to the button
        self.button_calc_fft.setFixedSize(QSize(120, 30))
        self.button_calc_fft.setEnabled(False)

        # Button "Apply range"
        self.button_apply_range = QPushButton('Apply range')
        self.button_apply_range.clicked.connect(self.thread_button_action_apply_range_t3)  # adding action to the button
        self.button_apply_range.setFixedSize(QSize(190, 30))
        self.button_apply_range.setEnabled(False)

    # Creating labels near spinboxes to describe the input
        self.label_image_amplitude_color_min_t3 = QLabel("Min color:", self)
        self.label_image_amplitude_color_min_t3.setFixedSize(QSize(70, 30))
        self.label_image_amplitude_color_min_t3.setAlignment(QtCore.Qt.AlignCenter)

        # Creating labels near spinboxes to describe the input
        self.label_image_amplitude_color_max_t3 = QLabel("Max color:", self)
        self.label_image_amplitude_color_max_t3.setFixedSize(QSize(70, 30))
        self.label_image_amplitude_color_max_t3.setAlignment(QtCore.Qt.AlignCenter)

        # Spinbox min color amplitude on figure
        self.spinbox_image_amplitude_color_min_t3 = QDoubleSpinBox()
        self.spinbox_image_amplitude_color_min_t3.setFixedSize(QSize(70, 30))
        self.spinbox_image_amplitude_color_min_t3.setMinimum(0.0)
        self.spinbox_image_amplitude_color_min_t3.setMaximum(1.0)
        self.spinbox_image_amplitude_color_min_t3.setDecimals(4) 
        self.spinbox_image_amplitude_color_min_t3.setSingleStep(0.001) 
        self.spinbox_image_amplitude_color_min_t3.setValue(0.0)

        # Spinbox max color amplitude on figure
        self.spinbox_image_amplitude_color_max_t3 = QDoubleSpinBox()
        self.spinbox_image_amplitude_color_max_t3.setFixedSize(QSize(70, 30))
        self.spinbox_image_amplitude_color_max_t3.setMinimum(0.0)
        self.spinbox_image_amplitude_color_max_t3.setMaximum(1.0)
        self.spinbox_image_amplitude_color_max_t3.setDecimals(4) 
        self.spinbox_image_amplitude_color_max_t3.setSingleStep(0.001) 
        self.spinbox_image_amplitude_color_max_t3.setValue(1.0)

        # Work status label tab 3 
        self.label_processing_status_t3 = QLabel('', self)
        self.label_processing_status_t3.setFixedHeight(30)
        self.label_processing_status_t3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_processing_status_t3.setFont(QFont('Arial', 14))

        # Dummy label to align tab 3 line 2
        self.label_dummy_t3_l2 = QLabel('', self)
        self.label_dummy_t3_l2.setFixedHeight(30)
        self.label_dummy_t3_l2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dummy_t3_l2.setFont(QFont('Arial', 14))

        self.toolbar_frequency_layout_t3 = QHBoxLayout()

        # Creating label to indicate the initial time resolution
        label = "Time resolution assumed: {:8.4f}".format(np.round(self.time_resolution * 1000, 6)) + "  ms."
        self.label_time_resolution = QLabel(label, self)
        self.label_time_resolution.setFixedSize(QSize(300, 30))
        self.label_time_resolution.setAlignment(QtCore.Qt.AlignCenter)

        # Creating label to indicate the initial time resolution
        label = "Max frequency: {:8.4f}".format(np.round(0.0, 2)) + "  Hz"
        self.label_max_frequency_t3 = QLabel(label, self)
        self.label_max_frequency_t3.setFixedSize(QSize(200, 30))
        self.label_max_frequency_t3.setAlignment(QtCore.Qt.AlignCenter)

        self.label_freq_limit_t3 = QLabel('Fig frequency limit:', self)
        self.label_freq_limit_t3.setFixedSize(QSize(100, 30))
        self.label_freq_limit_t3.setAlignment(QtCore.Qt.AlignCenter)

        self.label_hz = QLabel('Hz', self)
        self.label_hz.setFixedSize(QSize(15, 30))
        self.label_hz.setAlignment(QtCore.Qt.AlignCenter)

        frequency_limit_init = 60  # Hz
        step_type = QAbstractSpinBox.AdaptiveDecimalStepType  # step type

        self.freq_limit_input = QDoubleSpinBox()
        self.freq_limit_input.setStepType(step_type)
        self.freq_limit_input.setMinimum(0.0)
        self.freq_limit_input.setFixedSize(QSize(60, 30))
        self.freq_limit_input.setValue(frequency_limit_init)

        self.toolbar_frequency_layout_t3.addWidget(self.toolbar_freq)
        self.toolbar_frequency_layout_t3.addWidget(self.label_max_frequency_t3)
        self.toolbar_frequency_layout_t3.addWidget(self.label_time_resolution)
        
        # Adding elements and packing layouts in the window
        self.input_controls_layout_t3_l1.addWidget(self.checkbox_cut_data_amp_with_limits_t3)
        self.input_controls_layout_t3_l1.addWidget(self.label_cut_data_amp_with_limits_t3)
        self.input_controls_layout_t3_l1.addWidget(self.label_dummy_align_t3_l1_1)
        self.input_controls_layout_t3_l1.addWidget(self.label_image_amplitude_color_min_t3)
        self.input_controls_layout_t3_l1.addWidget(self.spinbox_image_amplitude_color_min_t3)
        self.input_controls_layout_t3_l1.addWidget(self.label_freq_limit_t3)
        self.input_controls_layout_t3_l1.addWidget(self.freq_limit_input)
        self.input_controls_layout_t3_l1.addWidget(self.label_hz)
        self.input_controls_layout_t3_l1.addWidget(self.label_processing_status_t3)

        
        self.input_controls_layout_t3_l2.addWidget(self.button_calc_fft)
        self.input_controls_layout_t3_l2.addWidget(self.label_image_amplitude_color_max_t3)
        self.input_controls_layout_t3_l2.addWidget(self.spinbox_image_amplitude_color_max_t3)
        self.input_controls_layout_t3_l2.addWidget(self.button_apply_range)
        self.input_controls_layout_t3_l2.addWidget(self.label_dummy_t3_l2)
        self.tab3.layout.addLayout(self.input_controls_layout_t3_l1)
        self.tab3.layout.addLayout(self.input_controls_layout_t3_l2)

        self.tab3.layout.addLayout(self.toolbar_frequency_layout_t3)
        self.tab3.layout.addWidget(self.canvas_freq)
        self.tab3.setLayout(self.tab3.layout)




        # ############################################################
        # #         Fourth tab - analysis in spectral domain         #
        # ############################################################

        # Fourth tab
        self.tab4.layout = QVBoxLayout(self.tab4)
        self.input_controls_layout_t4_l1 = QHBoxLayout()
        self.figures_layout_t4_l1 = QHBoxLayout()
        self.figures_layout_t4_l2 = QHBoxLayout()

        # Button "Plot data"
        self.button_plot_data_t4_l1 = QPushButton('Plot data')
        self.button_plot_data_t4_l1.clicked.connect(self.plot_or_update_figures_tab_4)  # adding action to the button
        self.button_plot_data_t4_l1.setFixedSize(QSize(250, 30))

        # Label before slider
        self.label_dm_selection_t4l1 = QLabel("Select DM:", self)
        self.label_dm_selection_t4l1.setFixedSize(QSize(90, 30))
        self.label_dm_selection_t4l1.setAlignment(QtCore.Qt.AlignCenter)


        # Preparing dummy dm_vector for slider_dm_selection_t4l1 to be updated after data read
        self.vdm_dm_vector = np.linspace(0, 100, num=100)


        # Slider t4l1
        self.slider_dm_selection_t4l1 = QSlider(Qt.Horizontal)  
        self.slider_dm_selection_t4l1.setFixedSize(QSize(650, 30))
        self.slider_dm_selection_t4l1.setRange(0, len(self.vdm_dm_vector))
        self.slider_dm_selection_t4l1.setValue(0)
        self.slider_dm_selection_t4l1.setTickPosition(QSlider.TicksAbove)
        self.slider_dm_selection_t4l1.valueChanged.connect(self.slider_dm_selection_t4l1_changed)

        # Label Slider t4l1
        self.label_dm_selection_value_t4l1 = QLabel(str(np.round(self.vdm_dm_vector[0], 3)), self)
        self.label_dm_selection_value_t4l1.setFixedSize(QSize(40, 30))
        self.label_dm_selection_value_t4l1.setAlignment(QtCore.Qt.AlignCenter)

        # Work status label tab 4
        self.label_processing_status_t4 = QLabel(" ", self)
        self.label_processing_status_t4.setFixedHeight(30)
        self.label_processing_status_t4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_processing_status_t4.setFont(QFont('Arial', 14))

        # Plot window DM vs Time
        self.figure_dm_vs_time_t4_l1 = plt.figure()
        self.canvas_dm_vs_time_t4_l1 = FigureCanvas(self.figure_dm_vs_time_t4_l1)  

        # Plot window Integrated amplitude vs. DM
        self.figure_amplitude_vs_dm_t4_l1 = plt.figure()
        self.canvas_amplitude_vs_dm_t4_l1 = FigureCanvas(self.figure_amplitude_vs_dm_t4_l1)  

        # Plot window integrated spectra over DMs
        self.figure_integrated_spectra_over_dms_t4_l2 = plt.figure()
        self.canvas_integrated_spectra_over_dms_t4_l2 = FigureCanvas(self.figure_integrated_spectra_over_dms_t4_l2)  

        # Plot window spectrum for particular DM
        self.figure_spectrum_for_dm_t4_l2 = plt.figure()
        self.canvas_spectrum_for_dm_t4_l2 = FigureCanvas(self.figure_spectrum_for_dm_t4_l2)  

        # Packing into layouts
        self.input_controls_layout_t4_l1.addWidget(self.button_plot_data_t4_l1)
        self.input_controls_layout_t4_l1.addWidget(self.label_dm_selection_t4l1)
        self.input_controls_layout_t4_l1.addWidget(self.slider_dm_selection_t4l1)
        self.input_controls_layout_t4_l1.addWidget(self.label_dm_selection_value_t4l1)
        self.input_controls_layout_t4_l1.addWidget(self.label_processing_status_t4)

        self.figures_layout_t4_l1.addWidget(self.canvas_dm_vs_time_t4_l1)
        self.figures_layout_t4_l1.addWidget(self.canvas_amplitude_vs_dm_t4_l1)
        
        self.figures_layout_t4_l2.addWidget(self.canvas_integrated_spectra_over_dms_t4_l2)
        self.figures_layout_t4_l2.addWidget(self.canvas_spectrum_for_dm_t4_l2)

        self.tab4.layout.addLayout(self.input_controls_layout_t4_l1)
        self.tab4.layout.addLayout(self.figures_layout_t4_l1)
        self.tab4.layout.addLayout(self.figures_layout_t4_l2)

        self.tab4.setLayout(self.tab4.layout)






        # ############################################################
        # #         Fifth tab - spectrum of spectrum                 #
        # ############################################################

        # Fifth tab
        self.tab5.layout = QVBoxLayout(self.tab5)
        self.input_controls_layout_t5_l1 = QHBoxLayout()
        self.figures_layout_t5_l2 = QHBoxLayout()
        self.figures_layout_t5_l3 = QHBoxLayout()

        # Button "Plot data"
        self.button_plot_data_t5_l1 = QPushButton('Plot data')
        self.button_plot_data_t5_l1.clicked.connect(self.thread_plot_or_update_figures_tab_5)  # adding action to the button
        self.button_plot_data_t5_l1.setFixedSize(QSize(250, 30))

        # Dummy label to align tab 5 line 1
        self.label_dummy_t5_l1 = QLabel('', self)
        self.label_dummy_t5_l1.setFixedHeight(30)
        self.label_dummy_t5_l1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dummy_t5_l1.setFont(QFont('Arial', 14))

        # Plot window spectrum for particular DM
        self.figure_spectrum_for_dm_t5_l2 = plt.figure()
        self.canvas_spectrum_for_dm_t5_l2 = FigureCanvas(self.figure_spectrum_for_dm_t5_l2)  

        # Plot window spectrum for particular DM
        self.figure_spectrum_of_spectrum_t5_l3 = plt.figure()
        self.canvas_spectrum_of_spectrum_t5_l3 = FigureCanvas(self.figure_spectrum_of_spectrum_t5_l3)  


        # Packing into layouts
        self.input_controls_layout_t5_l1.addWidget(self.button_plot_data_t5_l1)
        self.input_controls_layout_t5_l1.addWidget(self.label_dummy_t5_l1)

        self.figures_layout_t5_l2.addWidget(self.canvas_spectrum_for_dm_t5_l2)
        
        self.figures_layout_t5_l3.addWidget(self.canvas_spectrum_of_spectrum_t5_l3)

        self.tab5.layout.addLayout(self.input_controls_layout_t5_l1)
        self.tab5.layout.addLayout(self.figures_layout_t5_l2)
        self.tab5.layout.addLayout(self.figures_layout_t5_l3)

        self.tab5.setLayout(self.tab5.layout)








        ##############################
        #         Pack tabs          #
        ##############################

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    # action called by radio button switch txt
    def rb_txt_on_click(self):
        self.radioButton = self.sender()
        if self.radioButton.isChecked():
            # print("Process is %s" % (self.radioButton.process_type))
            self.label_vdm_file_selected.setEnabled(True)
            self.button_open_vdm.setEnabled(True)
            self.vdm_file_path_line.setEnabled(True)

            self.button_open_jds.setEnabled(False)
            self.button_select_result_path.setEnabled(False)
            self.button_process_jds.setEnabled(False)
            self.jds_file_path_line.setEnabled(False)
            self.result_path_line.setEnabled(False)

            self.label_dm_entry.setEnabled(False)
            self.line_dm_entry.setEnabled(False)
            self.label_dm_units.setEnabled(False)
            self.label_dm_range_entry.setEnabled(False)
            self.line_dm_range_entry.setEnabled(False)
            self.label_dm_range_units.setEnabled(False)
            self.label_dm_points_entry.setEnabled(False)
            self.line_dm_points_entry.setEnabled(False)
            self.button_calc_dm.setEnabled(False)
            self.label_dm_start.setEnabled(False)
            self.label_stert_dm_unit.setEnabled(False)
            self.label_dm_step_entry.setEnabled(False)
            self.label_dm_step_units.setEnabled(False)
            self.label_dm_stop_entry.setEnabled(False)
            self.label_dm_stop_units.setEnabled(False)

            self.label_data_channels_entry.setEnabled(False)
            self.channel_select_dropdown.setEnabled(False)
            self.label_no_of_processes_entry.setEnabled(False)
            self.process_no_select_dropdown.setEnabled(False)

            self.button_select_pairs_source_path.setEnabled(False)
            self.button_select_pairs_result_path.setEnabled(False)
            self.button_process_pairs_jds.setEnabled(False)
            self.source_pairs_path_line.setEnabled(False)
            self.result_pairs_path_line.setEnabled(False)
            self.line_pairs_dm_entry.setEnabled(False)
            self.label_pairs_dm_entry.setEnabled(False)
            self.label_pairs_dm_units.setEnabled(False)

    # action called by radio button switch jds
    def rb_jds_on_click(self):
        self.radioButton = self.sender()
        if self.radioButton.isChecked():
            # print("Process is %s" % (self.radioButton.process_type))
            self.label_vdm_file_selected.setEnabled(False)
            self.vdm_file_path_line.setEnabled(False)
            self.button_open_vdm.setEnabled(False)

            self.button_open_jds.setEnabled(True)
            self.button_select_result_path.setEnabled(True)
            # self.button_process_jds.setEnabled(True)
            self.jds_file_path_line.setEnabled(True)
            self.result_path_line.setEnabled(True)
            self.label_dm_entry.setEnabled(True)
            self.line_dm_entry.setEnabled(True)
            self.label_dm_units.setEnabled(True)
            self.label_dm_range_entry.setEnabled(True)
            self.line_dm_range_entry.setEnabled(True)
            self.label_dm_range_units.setEnabled(True)
            self.label_dm_points_entry.setEnabled(True)
            self.line_dm_points_entry.setEnabled(True)
            self.button_calc_dm.setEnabled(True)
            self.label_dm_start.setEnabled(True)
            self.label_stert_dm_unit.setEnabled(True)
            self.label_dm_step_entry.setEnabled(True)
            self.label_dm_step_units.setEnabled(True)
            self.label_dm_stop_entry.setEnabled(True)
            self.label_dm_stop_units.setEnabled(True)

            self.label_data_channels_entry.setEnabled(True)
            self.channel_select_dropdown.setEnabled(True)
            self.label_no_of_processes_entry.setEnabled(True)
            self.process_no_select_dropdown.setEnabled(True)

            self.button_select_pairs_source_path.setEnabled(False)
            self.button_select_pairs_result_path.setEnabled(False)
            self.button_process_pairs_jds.setEnabled(False)
            self.source_pairs_path_line.setEnabled(False)
            self.result_pairs_path_line.setEnabled(False)
            self.line_pairs_dm_entry.setEnabled(False)
            self.label_pairs_dm_entry.setEnabled(False)
            self.label_pairs_dm_units.setEnabled(False)

    def rb_pairs_on_click(self):
        self.radioButton = self.sender()
        if self.radioButton.isChecked():
            # print("Process is %s" % (self.radioButton.process_type))
            self.label_vdm_file_selected.setEnabled(False)
            self.vdm_file_path_line.setEnabled(False)
            self.button_open_vdm.setEnabled(False)

            self.button_open_jds.setEnabled(False)
            self.button_select_result_path.setEnabled(False)
            self.button_process_jds.setEnabled(False)
            self.jds_file_path_line.setEnabled(False)
            self.result_path_line.setEnabled(False)
            self.label_dm_entry.setEnabled(False)
            self.line_dm_entry.setEnabled(False)
            self.label_dm_units.setEnabled(False)
            self.label_dm_range_entry.setEnabled(False)
            self.line_dm_range_entry.setEnabled(False)
            self.label_dm_range_units.setEnabled(False)
            self.label_dm_points_entry.setEnabled(False)
            self.line_dm_points_entry.setEnabled(False)
            self.button_calc_dm.setEnabled(False)
            self.label_dm_start.setEnabled(False)
            self.label_stert_dm_unit.setEnabled(False)
            self.label_dm_step_entry.setEnabled(False)
            self.label_dm_step_units.setEnabled(False)
            self.label_dm_stop_entry.setEnabled(False)
            self.label_dm_stop_units.setEnabled(False)

            self.label_data_channels_entry.setEnabled(False)
            self.channel_select_dropdown.setEnabled(False)
            self.label_no_of_processes_entry.setEnabled(False)
            self.process_no_select_dropdown.setEnabled(False)

            self.button_select_pairs_source_path.setEnabled(True)
            self.button_select_pairs_result_path.setEnabled(True)
            self.button_process_pairs_jds.setEnabled(True)
            self.source_pairs_path_line.setEnabled(True)
            self.result_pairs_path_line.setEnabled(True)
            self.line_pairs_dm_entry.setEnabled(True)
            self.label_pairs_dm_entry.setEnabled(True)
            self.label_pairs_dm_units.setEnabled(True)




        ##############################
        #         Functions          #
        ##############################


    def one_vdm_file_dialog(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "VDM Files (*.vdm)")
        if check:
            [self.vdm_filepath, self.vdm_filename] = os.path.split(file)
            self.vdm_file_path_line.setText(file)


    def calculate_dm_values(self):
        self.central_dm = float(self.line_dm_entry.text().replace(',', '.'))
        self.dm_range = float(self.line_dm_range_entry.text().replace(',', '.'))
        self.dm_points = int(self.line_dm_points_entry.text().replace(',', '.'))

        # Calculating DM vector to display DM values
        self.dm_vector = np.linspace(self.central_dm - self.dm_range, self.central_dm + self.dm_range, num=self.dm_points)

        self.button_process_jds.setEnabled(True)
        self.line_start_dm_entry.setText(str(np.round(self.dm_vector[0], 6)))
        self.line_dm_step_entry.setText(str(np.round(self.dm_vector[1] - self.dm_vector[0], 6)))
        self.line_dm_stop_entry.setText(str(np.round(self.dm_vector[-1], 6)))



    def jds_files_open_dialog(self):
        files, check = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "", "JDS files (*.jds)")
        file_names = []
        self.jds_file_path_line.clear()  # Clear the text input to add new file paths
        if check:
            for i in range(len(files)):
                self.jds_file_path_line.appendPlainText(files[i])
                [directory, file_name] = os.path.split(files[i])
                file_names.append(file_name)
            self.jds_analysis_directory = directory
            self.jds_analysis_list = file_names


    def thread_preprocess_jds_files(self):
        t1 = Thread(target=self.preprocess_jds_files)
        t1.start()


    def specify_result_folder_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            self.path_to_result_folder = dir_name
            self.result_path_line.setText(str(dir_name))
        pass


    def preprocess_jds_files(self):
        try:
            self.source_dm = float(self.line_dm_entry.text().replace(',', '.'))
        except ValueError:
            print(' Wrong source DM value! Unable to convert into float number.')
            self.label_processing_status.setText("Wrong DM value!")
            self.label_processing_status.setStyleSheet("background-color: red;")
            return

        try:
            jds_result_folder = str(self.path_to_result_folder)
        except AttributeError:
            self.label_processing_status.setText("Wrong result directory specified!")
            self.label_processing_status.setStyleSheet("background-color: red;")
            return

        try:
            jds_analysis_files = self.jds_analysis_list
        except AttributeError:
            self.label_processing_status.setText("Wrong JDS files specified!")
            self.label_processing_status.setStyleSheet("background-color: red;")
            return

        # Typical time resolution
        time_res = (1 / 66000000) * 16384 * 32     # Time resolution, s  (0.007944 s)

        tmp = self.channel_select_dropdown.currentIndex()
        if tmp == "A":
            data_types = ['chA']
        elif tmp == "B":
            data_types = ['chB']
        elif tmp == "A & B":
            data_types = ['chA', 'chB']
        else:
            data_types = ['chA']
        
        n_proc = int(self.process_no_select_dropdown.currentIndex())

        # Only if parameters are good, run processing
        self.label_processing_status.setText("JDS data are being processed...")
        self.label_processing_status.setStyleSheet("background-color: yellow;")

        try:
            var_dm_file_path = make_var_dm_file_from_jds(self.jds_analysis_directory, 
                                                         jds_analysis_files, 
                                                         jds_result_folder,
                                                         self.dm_vector, 
                                                         time_res, 
                                                         data_types, 
                                                         n_proc)



        except:
            self.label_processing_status.setText("Something wrong happened during calculations!")
            self.label_processing_status.setStyleSheet("background-color: red;")
            return

        # After the processing is finished,
        self.txt_file_path_line.setText(var_dm_file_path)
        [self.txt_filepath, self.txt_filename] = os.path.split(var_dm_file_path)
        self.label_processing_status.setText("JDS preprocessing finished! "
                                             "You can now open next tab and process the profile")
        self.label_processing_status.setStyleSheet("background-color: lightgreen;")




    def preprocess_pairs_jds_files(self):
        try:
            self.source_pairs_dm = float(self.line_pairs_dm_entry.text().replace(',', '.'))
        except ValueError:
            print(' Wrong source DM value! Unable to convert into float number.')
            self.label_pairs_processing_status.setText("Wrong DM value!")
            self.label_pairs_processing_status.setStyleSheet("background-color: red;")
            return

        try:
            jds_pairs_source_folder = str(self.path_to_source_pairs_folder)
        except AttributeError:
            self.label_pairs_processing_status.setText("Wrong source directory specified!")
            self.label_pairs_processing_status.setStyleSheet("background-color: red;")
            return

        try:
            jds_pairs_result_folder = str(self.path_to_result_pairs_folder)
        except AttributeError:
            self.label_pairs_processing_status.setText("Wrong result directory specified!")
            self.label_pairs_processing_status.setStyleSheet("background-color: red;")
            return

        # Only if parameters are good, run processing
        self.label_pairs_processing_status.setText("JDS file pairs are being processed...")
        self.label_pairs_processing_status.setStyleSheet("background-color: yellow;")

        try:
            profile_txt_file_path = f_make_transient_profile_from_jds_file_pairs(jds_pairs_source_folder,
                                                                                 jds_pairs_result_folder,
                                                                                 self.source_pairs_dm)
        except:
            self.label_pairs_processing_status.setText("Something wrong happened during calculations!")
            self.label_pairs_processing_status.setStyleSheet("background-color: red;")
            return

        # After the processing is finished,
        self.label_pairs_processing_status.setText("JDS file pairs preprocessing finished! "
                                             "Please select the first option and pick a file to process the profile")
        self.label_pairs_processing_status.setStyleSheet("background-color: lightgreen;")






    def thread_preprocess_pairs_jds_files(self):
        t2 = Thread(target=self.preprocess_pairs_jds_files)
        t2.start()



    def specify_source_pairs_folder_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            self.path_to_source_pairs_folder = dir_name
            self.source_pairs_path_line.setText(str(dir_name))
        pass

    def specify_result_pairs_folder_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            self.path_to_result_pairs_folder = dir_name
            self.result_pairs_path_line.setText(str(dir_name))
        pass


    #
    #
    #
    #
    #


    #############################################################
    #              T A B    2    F U N C T I O N S              #
    #############################################################


    def slider_data_begins_at_value_changed(self):
        value = int(self.slider_data_begins_at.value())
        self.label_data_begins_at.setText(str(value))

    def slider_data_finishes_at_value_changed(self):
        value = int(self.slider_data_finishes_at.value())
        self.label_data_finishes_at.setText(str(value))

    # def slider_figure_color_amplitude_max_value_changed(self):
    #     value = int(self.slider_image_amplitude_color_max_t2.value())
    #     self.label_image_amplitude_color_max_t2.setText(str(np.round(value / 200, 3)))

    # def slider_figure_color_amplitude_min_value_changed(self):
    #     value = int(self.slider_image_amplitude_color_min_t2.value())
    #     self.label_image_amplitude_color_min_t2.setText(str(np.round(value / 200, 3)))



    # Thread called by the push button "Read data" on tab 2
    def thread_read_initial_data(self):


        # Reading the path fo VDM data file from GUI and normalizing it
        data_filepath = self.vdm_file_path_line.text()
        data_filepath = os.path.normpath(data_filepath)
        [directory, self.data_filename] = os.path.split(data_filepath)
        
        # Checking (.vdm) data file exists
        exists = os.path.isfile(os.path.join(directory, self.data_filename))
        # path.isfile(path)

        if exists:
            self.label_processing_status_t2.setText("Reading data...")
            self.label_processing_status_t2.setStyleSheet("background-color: yellow;")

            self.figure_time.clear()  # clearing figure
            ax0 = self.figure_time.add_subplot(111)
            ax0.remove() 
            self.figure_time.text(0.4, 0.5, "Reading data file...", color="C0", size=22)
            self.canvas_time.draw() 

            # Disabling next buttons
            self.button_filter_time.setEnabled(False)
            self.button_cut_data_time.setEnabled(False)
            self.button_apply_color_range_t2.setEnabled(False)
            self.button_apply_range.setEnabled(False)
            self.button_calc_fft.setEnabled(False)

            t0 = Thread(target=self.read_initial_data)
            t0.start()
        else:
            self.label_processing_status_t2.setText("No such file")
            self.label_processing_status_t2.setStyleSheet("background-color: red;")

            self.figure_time.clear()  # clearing figure
            ax0 = self.figure_time.add_subplot(111)
            ax0.remove() 
            self.figure_time.text(0.3, 0.5, "Error reading the file. Check if it exists.", color="C0", size=22)
            self.canvas_time.draw() 


    # Action called by the push button "Read data" on tab 2
    def read_initial_data(self):

        # Reading the path fo VDM data file from GUI and normalizing it
        data_filepath = self.vdm_file_path_line.text()
        data_filepath = os.path.normpath(data_filepath)
        [directory, self.data_filename] = os.path.split(data_filepath)
        
        # Reading (.vdm) data file
        data_file = open(os.path.join(directory, self.data_filename), 'rb')
        self.time_points_num = struct.unpack('q', data_file.read(8))[0]
        self.vdm_dm_points = struct.unpack('q', data_file.read(8))[0]
        self.vdm_central_dm = struct.unpack('d', data_file.read(8))[0]
        self.vdm_dm_range = struct.unpack('d', data_file.read(8))[0]
        initial_data_array = np.fromfile(data_file, dtype=np.float64, count=self.time_points_num * self.vdm_dm_points)
        self.vdm_data_array = np.reshape(initial_data_array, [self.vdm_dm_points, self.time_points_num])
        data_file.close()

        # self.vdm_data = initial_data_array

        # Set label with array dimensions        
        self.label_array_dimensions_t2.setText("DM:  " + str(self.vdm_dm_points) + "  pts,   time:  " + str(self.time_points_num) + "  pts")

        # Set median filter length to 1 for the case the filter has never called
        self.med_filter_length = 1

        # Calculating DM vector to have all DM values used
        self.vdm_dm_vector = np.linspace(self.vdm_central_dm - self.vdm_dm_range,  
                                         self.vdm_central_dm + self.vdm_dm_range, 
                                         num=self.vdm_dm_points)
        
        # Calculating time axis in seconds
        self.time_axis_sec = np.array([self.time_resolution * i for i in range(self.time_points_num)])
 
        # Normalizing data
        self.vdm_data_array = self.vdm_data_array - np.min(self.vdm_data_array)
        self.vdm_data_array = self.vdm_data_array / np.max(self.vdm_data_array)

        # Configure gui interface on tab 4
        self.slider_dm_selection_t4l1.setRange(0, len(self.vdm_dm_vector))
        self.slider_dm_selection_t4l1.setValue(0)
        self.label_dm_selection_value_t4l1.setText(str(np.round(self.vdm_dm_vector[0], 3)))

        # Making plot
        self.figure_time.clear()  # clearing figure
        ax0 = self.figure_time.add_subplot(111)
        plot = ax0.imshow(np.flipud(self.vdm_data_array), 
                          extent=[self.time_axis_sec[0],  self.time_axis_sec[-1], self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]], 
                          aspect='auto', cmap="Greys")

        #                 extent=[0,  self.time_points_num, self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]], 

        # ax0.axis([self.low_freq_limit_of_filter, self.high_frequency_limit,  self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]])
        # ax0.set_xlabel('Time, points', fontsize=12, fontweight='bold')
        ax0.set_xlabel('Time, seconds', fontsize=12, fontweight='bold')
        ax0.set_ylabel(f'DM, pc/cm\N{SUPERSCRIPT THREE}', fontsize=12, fontweight='bold')
        ax0.set_title('Time profiles vs. DM value', fontsize=10, fontweight='bold')
        self.figure_time.set_constrained_layout(True)
        self.figure_time.colorbar(plot, pad=0, aspect=50, label="Amplitude, AU")  # , orientation="horizontal"
        self.canvas_time.draw()  # refresh canvas

        # Enabling next buttons
        self.button_filter_time.setEnabled(True)
        self.button_cut_data_time.setEnabled(True)

        self.label_processing_status_t2.setText(" ")
        self.label_processing_status_t2.setStyleSheet("background-color: light grey;")

    #
    #
    #
    #
    #

    # Thread called by the push button "Subtract median" on tab 2
    def thread_subtract_median_in_time(self):

        self.label_processing_status_t2.setText("Subtracting...")
        self.label_processing_status_t2.setStyleSheet("background-color: yellow;")

        t0 = Thread(target=self.subtract_median_in_time)
        t0.start()
        # t0.join()



    # Action called by the push button "Subtract median" on tab 2
    def subtract_median_in_time(self):

        # Subtract median
        self.med_filter_length = int(self.filter_win_input.value())
        median = scipy.ndimage.median_filter(self.vdm_data_array, self.med_filter_length, axes=1)
        self.vdm_data_array = np.subtract(self.vdm_data_array, median)
        del median

        # Making copy of array to plot
        vdm_data_array_to_plot = self.vdm_data_array.copy()

        # Normalizing data to plot
        vdm_data_array_to_plot = vdm_data_array_to_plot - np.min(vdm_data_array_to_plot)
        vdm_data_array_to_plot = vdm_data_array_to_plot / np.max(vdm_data_array_to_plot)

        # Updating figure on tab 2
        self.figure_time.clear()  # clearing figure
        ax0 = self.figure_time.add_subplot(111)
        plot = ax0.imshow(vdm_data_array_to_plot, 
                          extent=[self.time_axis_sec[0],  self.time_axis_sec[-1], self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]], 
                          aspect='auto', cmap="Greys")
        
        # extent=[0, self.time_points_num, self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]], 
        # ax0.axis([self.low_freq_limit_of_filter, self.high_frequency_limit,  self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]])
        ax0.set_xlabel('Time, seconds', fontsize=12, fontweight='bold')
        ax0.set_ylabel(f'DM, pc/cm\N{SUPERSCRIPT THREE}', fontsize=12, fontweight='bold')
        ax0.set_title('Time profiles vs. DM value', fontsize=10, fontweight='bold')
        self.figure_time.set_constrained_layout(True)
        self.figure_time.colorbar(plot, pad=0, aspect=50, label="Amplitude, AU")
        self.canvas_time.draw()  # Refresh canvas
    
        self.label_processing_status_t2.setText(" ")
        self.label_processing_status_t2.setStyleSheet("background-color: light grey;")

        del vdm_data_array_to_plot

    #
    #
    #
    #
    #

    def thread_cut_initial_data_in_time(self):
        
        start_index = int(self.slider_data_begins_at.value())
        finish_index = int(self.slider_data_finishes_at.value())

        if start_index >= finish_index:

            self.label_cut_index_status_t2.setText("Wrong values")
            self.label_cut_index_status_t2.setStyleSheet("background-color: red;")
        else:
            
            self.label_cut_index_status_t2.setText(" ")
            self.label_cut_index_status_t2.setStyleSheet("background-color: light grey;")

            self.label_processing_status_t2.setText("Cutting data...")
            self.label_processing_status_t2.setStyleSheet("background-color: yellow;")

            t0 = Thread(target=self.cut_initial_data_in_time)
            t0.start()
            # t0.join()


    def cut_initial_data_in_time(self):
        
        try:
            start_index = int(self.slider_data_begins_at.value())
            finish_index = int(self.slider_data_finishes_at.value())
            total_time_points = self.vdm_data_array.shape[1]
            start_time_point_cut = int(start_index * total_time_points / 16)
            finish_time_point_cut = int(finish_index * total_time_points / 16)
            self.time_points_num = finish_time_point_cut - start_time_point_cut

            # Cutting data and time axis
            self.cut_vdm_data_array = self.vdm_data_array[:, start_time_point_cut: finish_time_point_cut].copy()
            self.cut_time_axis_sec = self.time_axis_sec[start_time_point_cut: finish_time_point_cut]

            # Set label with array dimensions        
            self.label_array_dimensions_t2.setText("DM:  " + str(self.vdm_dm_points) + "  pts,   time:  " + str(self.time_points_num) + "  pts")

            # Making copy of array to plot
            cut_vdm_data_array_to_plot = self.cut_vdm_data_array.copy()

            # Normalizing data to plot
            cut_vdm_data_array_to_plot = cut_vdm_data_array_to_plot - np.min(cut_vdm_data_array_to_plot)
            cut_vdm_data_array_to_plot = cut_vdm_data_array_to_plot / np.max(cut_vdm_data_array_to_plot)

            # Updating figure on tab 2
            self.figure_time.clear()  # clearing figure
            ax0 = self.figure_time.add_subplot(111)
            plot = ax0.imshow(cut_vdm_data_array_to_plot, 
                            extent=[self.cut_time_axis_sec[0],  self.cut_time_axis_sec[-1], self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]], 
                            aspect='auto', cmap="Greys")
            # ax0.axis([self.low_freq_limit_of_filter, self.high_frequency_limit,  self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]])
            ax0.set_xlabel('Time, points', fontsize=12, fontweight='bold')
            ax0.set_ylabel(f'DM, pc/cm\N{SUPERSCRIPT THREE}', fontsize=12, fontweight='bold')
            ax0.set_title('Time profiles vs. DM value', fontsize=10, fontweight='bold')
            self.figure_time.set_constrained_layout(True)
            self.figure_time.colorbar(plot, pad=0, aspect=50, label="Amplitude, AU")
            self.canvas_time.draw()  # Refresh canvas
        
            self.label_processing_status_t2.setText(" ")
            self.label_processing_status_t2.setStyleSheet("background-color: light grey;")

            self.button_apply_color_range_t2.setEnabled(True)
            self.button_calc_fft.setEnabled(True)

            del cut_vdm_data_array_to_plot
        
        except AttributeError:
        
            self.label_processing_status_t3.setText("Press 'Read data' button first!")
            self.label_processing_status_t3.setStyleSheet("background-color: red;")
    #
    #
    #
    #
    #
    def thread_update_cut_data_with_color_amplitude_value(self):
        
        v_min_man = self.spinbox_image_amplitude_color_min_t2.value()
        v_max_man = self.spinbox_image_amplitude_color_max_t2.value()

        # v_max_min = int(self.slider_image_amplitude_color_min_t2.value())
        # v_max_man = int(self.slider_image_amplitude_color_max_t2.value())


        if v_min_man >= v_max_man:

            self.label_processing_status_t2.setText("Wrong values")
            self.label_processing_status_t2.setStyleSheet("background-color: red;")
        
        else:
            
            self.label_processing_status_t2.setText("Applying limits...")
            self.label_processing_status_t2.setStyleSheet("background-color: yellow;")
        
            t0 = Thread(target=self.update_cut_data_with_color_amplitude_value)
            t0.start()
            # t0.join()



    def update_cut_data_with_color_amplitude_value(self):
        
        try:

            self.label_processing_status_t3.setText(" ")
            self.label_processing_status_t3.setStyleSheet("background-color: light grey;")


            # Making copy of array to plot
            cut_vdm_data_array_to_plot = self.cut_vdm_data_array.copy()

            # Normalizing data to plot
            cut_vdm_data_array_to_plot = np.subtract(cut_vdm_data_array_to_plot, np.min(cut_vdm_data_array_to_plot))
            cut_vdm_data_array_to_plot = np.divide(cut_vdm_data_array_to_plot, np.max(cut_vdm_data_array_to_plot))

            # Reading value
            v_min_man = float(self.spinbox_image_amplitude_color_min_t2.value())
            v_max_man = float(self.spinbox_image_amplitude_color_max_t2.value())

            self.max_points = np.argwhere(cut_vdm_data_array_to_plot >= v_max_man)

            # Updating figure on tab 2
            self.figure_time.clear()  # clearing figure
            ax0 = self.figure_time.add_subplot(111)
            plot = ax0.imshow(cut_vdm_data_array_to_plot, 
                            extent=[self.cut_time_axis_sec[0],  self.cut_time_axis_sec[-1], self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]],  
                            vmin = v_min_man, vmax = v_max_man, aspect='auto', cmap="Greys")

            # As we use np.flipud (flip up-down) the image to match the dm values vector, we also flip the points coordinates
            # by subtraction from the length of the DM vector length
            if self.checkbox_show_color_markers_t2.isChecked():
                for i in range(len(self.max_points)):
                    ax0.plot(self.cut_time_axis_sec[self.max_points[i,1]], self.vdm_dm_vector[int(len(self.vdm_dm_vector) - self.max_points[i,0]) - 1], marker='o', color="red") 

            # ax0.axis([self.low_freq_limit_of_filter, self.high_frequency_limit,  self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]])
            ax0.set_xlabel('Time, seconds', fontsize=12, fontweight='bold')
            ax0.set_ylabel(f'DM, pc/cm\N{SUPERSCRIPT THREE}', fontsize=12, fontweight='bold')
            ax0.set_title('Time profiles vs. DM value', fontsize=10, fontweight='bold')
            self.figure_time.set_constrained_layout(True)
            self.figure_time.colorbar(plot, pad=0, aspect=50, label="Amplitude, AU")
            self.canvas_time.draw()  # Refresh canvas
        
            self.label_processing_status_t2.setText(" ")
            self.label_processing_status_t2.setStyleSheet("background-color: light grey;")

            del cut_vdm_data_array_to_plot
        
        except AttributeError:
        
            self.label_processing_status_t3.setText("Press 'Cut data' button first!")
            self.label_processing_status_t3.setStyleSheet("background-color: red;")

    #
    #
    #
    #
    #

    #############################################################
    #              T A B    3    F U N C T I O N S              #
    #############################################################


    # Thread called by the push button "Calculate FFT"
    def thread_calculate_fft_of_data(self):
        
        # Check if values are correct
        v_max_min = self.spinbox_image_amplitude_color_min_t2.value()
        v_max_man = self.spinbox_image_amplitude_color_max_t2.value()

        if v_max_min >= v_max_man:

            self.label_processing_status_t3.setText("Wrong amplitude values")
            self.label_processing_status_t3.setStyleSheet("background-color: red;")
        
        else:
            
            self.label_processing_status_t3.setText(" ")
            self.label_processing_status_t3.setStyleSheet("background-color: light grey;")

            # Updating figure on tab 3 to indicate the FFT is being calculated
            self.figure_freq.clear()  # clearing old figure
            ax0 = self.figure_freq.add_subplot(111)
            ax0.remove() 
            self.figure_freq.text(0.39, 0.5, "Calculating FFT...", color="C0", size=22)
            self.canvas_freq.draw()  # refresh canvas

            self.label_processing_status_t3.setText("Processing...")
            self.label_processing_status_t3.setStyleSheet("background-color: yellow;")
        
            # Starting the thread of FFT calculation
            t0 = Thread(target=self.calculate_fft_of_data)
            t0.start()
            # t0.join()


    # Action called by the push button "Calculate FFT"
    def calculate_fft_of_data(self):

        
        if self.checkbox_cut_data_amp_with_limits_t3.isChecked():
            
            # Reading value
            v_min_man = float(self.spinbox_image_amplitude_color_min_t2.value())
            v_max_man = float(self.spinbox_image_amplitude_color_max_t2.value())

            # Here we unnormalize limits to apply them to non-normalized array
            arr_min = np.min(self.cut_vdm_data_array)
            arr_max = np.max(self.cut_vdm_data_array)

            v_max_man = v_max_man * arr_max + arr_min
            v_min_man = v_min_man * arr_max + arr_min

            # Here we apply unnormalized limits to non-normalized array
            self.cut_vdm_data_array[self.cut_vdm_data_array > v_max_man] = v_max_man
            self.cut_vdm_data_array[self.cut_vdm_data_array < v_min_man] = v_min_man

        
        # Calculating FFT
        self.vdm_spectra = np.power(np.real(np.fft.fft(self.cut_vdm_data_array[:])), 2)  # calculation of the spectrum
        self.vdm_spectra = self.vdm_spectra[:, 0 : int(self.vdm_spectra.shape[1]/2)]  # delete second part of the spectrum

        # Making local copy to plot
        vdm_spectra_to_plot = self.vdm_spectra.copy()
        
        # Normalizing spectrum
        vdm_spectra_to_plot = np.subtract(vdm_spectra_to_plot, np.min(vdm_spectra_to_plot))
        vdm_spectra_to_plot = np.divide(vdm_spectra_to_plot, np.max(vdm_spectra_to_plot))

        # Nulling of the first smaples of the spectra under median filter
        vdm_spectra_to_plot[:, :self.med_filter_length] = 0

        # Calculating the frequency resolution and low frequency (median) filter limit 
        self.frequency_resolution = 1 / (self.time_resolution * 2 * self.vdm_spectra.shape[1])  # frequency resolution, Hz   
        self.low_freq_limit_of_filter = self.med_filter_length * self.frequency_resolution
        self.frequency_axis = np.array([self.frequency_resolution * i for i in range(self.vdm_spectra.shape[1])])
        
        # Show max possible frequency of FFT
        self.label_max_frequency_t3.setText("Max frequency: {:8.2f}".format(np.round(self.frequency_axis[-1], 2)) + "  Hz")

        # Set maximal possible frequency in the spinbox to plot
        self.freq_limit_input.setValue(np.round(self.frequency_axis[-1], 2))

        # Taking the high limit of frequency scale from GUI
        self.high_frequency_limit = int(self.freq_limit_input.value())  # Hz

        # Update the plot
        rc('font', size=12, weight='bold')
        self.figure_freq.clear()  # clearing figure
        ax0 = self.figure_freq.add_subplot(111)
        
        # divider = make_axes_locatable(ax0)
        # cax = divider.append_axes('right', size='1%', pad=0)
        
        plot = ax0.imshow(np.flipud(vdm_spectra_to_plot), 
                          extent=[self.frequency_axis[0], self.frequency_axis[-1], self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]], 
                          aspect='auto', cmap="Greys")
        ax0.axis([self.low_freq_limit_of_filter, self.high_frequency_limit,  self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]])
        ax0.set_xlabel('Frequency, Hz', fontsize=12, fontweight='bold')
        ax0.set_ylabel(f'DM, pc/cm\N{SUPERSCRIPT THREE}', fontsize=12, fontweight='bold')
        ax0.set_title('Time series', fontsize=10, fontweight='bold')
        self.figure_freq.set_constrained_layout(True)
        self.figure_freq.colorbar(plot, pad=0, aspect=50, label="Amplitude, AU")
        # self.figure_freq.colorbar(plot, cax=cax, aspect=100, label="Amplitude, AU")
        self.canvas_freq.draw()  # refresh canvas

        self.button_apply_range.setEnabled(True)

        self.label_processing_status_t3.setText(" ")
        self.label_processing_status_t3.setStyleSheet("background-color: light grey;")



    def thread_button_action_apply_range_t3(self):
        
        value_l = float(self.spinbox_image_amplitude_color_min_t3.value())
        value_h = float(self.spinbox_image_amplitude_color_max_t3.value())

        if value_l >= value_h:

            self.label_processing_status_t3.setText("Wrong values")
            self.label_processing_status_t3.setStyleSheet("background-color: red;")
        
        else:
            
            self.label_processing_status_t3.setText("Applying limits...")
            self.label_processing_status_t3.setStyleSheet("background-color: yellow;")
        
            t0 = Thread(target=self.button_action_apply_range_t3)
            t0.start()
            #  t0.join()


    def button_action_apply_range_t3(self):
        

        v_min_man = float(self.spinbox_image_amplitude_color_min_t3.value())
        v_max_man = float(self.spinbox_image_amplitude_color_max_t3.value())

        # Taking the high limit of frequency scale from GUI
        self.high_frequency_limit = int(self.freq_limit_input.value())  # Hz

        # Making local copy to plot
        vdm_spectra_to_plot = self.vdm_spectra.copy()
        
        # Normalizing spectrum
        vdm_spectra_to_plot = np.subtract(vdm_spectra_to_plot, np.min(vdm_spectra_to_plot))
        vdm_spectra_to_plot = np.divide(vdm_spectra_to_plot, np.max(vdm_spectra_to_plot))

        # Nulling of the first smaples of the spectra under median filter
        vdm_spectra_to_plot[:, :self.med_filter_length] = 0

        # Update the plot
        rc('font', size=12, weight='bold')
        self.figure_freq.clear()  # clearing figure
        ax0 = self.figure_freq.add_subplot(111)

        # divider = make_axes_locatable(ax0)
        # cax = divider.append_axes('right', size='1%', pad=0)

        plot = ax0.imshow(np.flipud(vdm_spectra_to_plot), 
                          extent=[self.frequency_axis[0], self.frequency_axis[-1], self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]], 
                          vmin = v_min_man, vmax = v_max_man,
                          aspect='auto', cmap="Greys")
        ax0.axis([self.low_freq_limit_of_filter, self.high_frequency_limit,  self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]])
        ax0.set_xlabel('Frequency, Hz', fontsize=12, fontweight='bold')
        ax0.set_ylabel(f'DM, pc/cm\N{SUPERSCRIPT THREE}', fontsize=12, fontweight='bold')
        ax0.set_title('Time series', fontsize=10, fontweight='bold')
        self.figure_freq.set_constrained_layout(True)
        # self.figure_freq.colorbar(plot, cax=cax, pad=0, aspect=50, label="Amplitude, AU")
        self.figure_freq.colorbar(plot, pad=0, aspect=50, label="Amplitude, AU")
        self.canvas_freq.draw()  # refresh canvas

        del vdm_spectra_to_plot

        self.label_processing_status_t3.setText(" ")
        self.label_processing_status_t3.setStyleSheet("background-color: light grey;")









    #############################################################
    #              T A B    4    F U N C T I O N S              #
    #############################################################


    def slider_dm_selection_t4l1_changed(self):
        value = int(self.slider_dm_selection_t4l1.value())
        self.label_dm_selection_value_t4l1.setText(str(np.round(self.vdm_dm_vector[value], 3)))




    def thread_plot_or_update_figures_tab_4(self):
               
        try:
            # self.label_processing_status_t4.setText(" ")
            # self.label_processing_status_t4.setStyleSheet("background-color: light grey;")

            # Updating figure on tab 4
            self.figure_dm_vs_time_t4_l1.clear()  # clearing old figure
            ax0 = self.figure_dm_vs_time_t4_l1.add_subplot(111)
            ax0.remove() 
            self.canvas_dm_vs_time_t4_l1.draw()  # refresh canvas

            # Updating figure on tab 4
            self.figure_amplitude_vs_dm_t4_l1.clear()  # clearing old figure
            ax0 = self.figure_amplitude_vs_dm_t4_l1.add_subplot(111)
            ax0.remove() 
            self.canvas_amplitude_vs_dm_t4_l1.draw()  # refresh canvas

            # Updating figure on tab 4
            self.figure_spectrum_for_dm_t4_l2.clear()  # clearing old figure
            ax0 = self.figure_spectrum_for_dm_t4_l2.add_subplot(111)
            ax0.remove() 
            self.canvas_spectrum_for_dm_t4_l2.draw()  # refresh canvas


            self.label_processing_status_t4.setText("Updating plots...")
            self.label_processing_status_t4.setStyleSheet("background-color: yellow;")

            # Starting the thread of FFT calculation
            t0 = Thread(target=self.plot_or_update_figures_tab_4)
            t0.start()
            # t0.join()

        except AttributeError:
            self.label_processing_status_t4.setText("Something went wrong...")
            self.label_processing_status_t4.setStyleSheet("background-color: red;")




    def plot_or_update_figures_tab_4(self):
        
        # Taking the high limit of frequency scale from GUI
        self.high_frequency_limit = float(self.freq_limit_input.value())  # Hz

        # Finding index of the frequency axis where the value exceeds the limit for the first time
        try:
            max_idx = np.array([np.where(self.frequency_axis >= self.high_frequency_limit)]).min()
        except: 
            max_idx = int(len(self.frequency_axis) - 1)

        # Cutting frequencies above selected limit to obtain best S/N
        self.vdm_spectra_cut = self.vdm_spectra[:,:max_idx].copy()
        self.frequency_axis_cut = self.frequency_axis[0:max_idx].copy()

        # Making local copy to plot
        vdm_spectra_to_plot = self.vdm_spectra_cut.copy()
        
        # Normalizing spectrum
        vdm_spectra_to_plot = np.subtract(vdm_spectra_to_plot, np.min(vdm_spectra_to_plot))
        vdm_spectra_to_plot = np.divide(vdm_spectra_to_plot, np.max(vdm_spectra_to_plot))

        # Nulling of the first smaples of the spectra under median filter
        vdm_spectra_to_plot[:, :self.med_filter_length] = 0

        # Values of color amplitudes
        v_min_man = float(self.spinbox_image_amplitude_color_min_t3.value())
        v_max_man = float(self.spinbox_image_amplitude_color_max_t3.value())

        # Manually selected DM read from slider
        man_dm_index = int(self.slider_dm_selection_t4l1.value())

        # Update the plot 1
        rc('font', size=10, weight='bold')
        self.figure_dm_vs_time_t4_l1.clear()  # clearing figure
        ax0 = self.figure_dm_vs_time_t4_l1.add_subplot(111)
        ax0.axhline(y = self.vdm_dm_vector[man_dm_index], color = 'C1', alpha = 0.2)
        ax0.imshow(np.flipud(vdm_spectra_to_plot), 
                   extent=[self.frequency_axis_cut[0], self.frequency_axis_cut[-1], self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]], 
                   vmin = v_min_man, vmax = v_max_man, aspect='auto', cmap="Greys")
        ax0.axis([self.low_freq_limit_of_filter, self.high_frequency_limit,  self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]])
        ax0.set_xlabel('Frequency, Hz', fontsize=10, fontweight='bold')
        ax0.set_ylabel(f'DM, pc/cm\N{SUPERSCRIPT THREE}', fontsize=10, fontweight='bold')
        ax0.set_title('Spectra of time profiles vs. DM values', fontsize=8, fontweight='bold')
        self.figure_dm_vs_time_t4_l1.set_constrained_layout(True)
        self.canvas_dm_vs_time_t4_l1.draw()  # refresh canvas

        # Integrating spectry by all frequencies in selected range
        mean_amp_vs_dm = np.mean(self.vdm_spectra_cut, axis=1)
        
        # Normalizing mean for plot
        mean_amp_vs_dm = np.subtract(mean_amp_vs_dm, np.min(mean_amp_vs_dm))
        mean_amp_vs_dm = np.divide(mean_amp_vs_dm, np.max(mean_amp_vs_dm))

        # Update the plot 2
        self.figure_amplitude_vs_dm_t4_l1.clear()  # clearing figure
        ax0 = self.figure_amplitude_vs_dm_t4_l1.add_subplot(111)
        ax0.axvline(x = self.vdm_dm_vector[man_dm_index], color = 'C1')
        ax0.plot(self.vdm_dm_vector, mean_amp_vs_dm)
        
        ax0.plot(self.vdm_dm_vector[np.argmax(mean_amp_vs_dm)], np.max(mean_amp_vs_dm), 'o', color="C1", markersize=8.0)
        ax0.text(self.vdm_dm_vector[np.argmax(mean_amp_vs_dm)], np.max(mean_amp_vs_dm), 
                 f'  DM:  '  + str(np.round(self.vdm_dm_vector[np.argmax(mean_amp_vs_dm)], 4)) + 
                 f'  pc/cm\N{SUPERSCRIPT THREE}')  # $DM_{max}$

        if self.checkbox_show_color_markers_t2.isChecked():
            
            # Calculating number of occurances of the max points on time-DM array
            dm_occurances = np.zeros(len(self.vdm_dm_vector))
            for i in range(len(self.max_points)):
                for dm_point in range(len(self.vdm_dm_vector)):
                    if self.max_points[i,0] == dm_point:
                        dm_occurances[dm_point] +=1

            ax1 = ax0.twinx()
            ax1.plot(self.vdm_dm_vector, dm_occurances, 'o', color="C3", markersize=3.0)
            ax1.set_ylabel('Max points on time-DM plane', fontsize=10, fontweight='bold')
            
        ax0.set_xlabel(f'DM, pc/cm\N{SUPERSCRIPT THREE}', fontsize=10, fontweight='bold')
        ax0.set_ylabel('Amplitude, AU', fontsize=10, fontweight='bold')
        ax0.set_title('Integrated spectra vs. DM values', fontsize=8, fontweight='bold')
        self.figure_amplitude_vs_dm_t4_l1.set_constrained_layout(True)
        self.canvas_amplitude_vs_dm_t4_l1.draw()  # refresh canvas

        # Update the plot 3

        # mean_profile = np.mean(self.vdm_spectra_cut, axis=0)
        mean_profile = np.mean(vdm_spectra_to_plot, axis=0)
        self.figure_integrated_spectra_over_dms_t4_l2.clear()  # clearing figure
        ax0 = self.figure_integrated_spectra_over_dms_t4_l2.add_subplot(111)
        ax0.plot(self.frequency_axis_cut, mean_profile)
        ax0.set_xlim(self.low_freq_limit_of_filter, self.high_frequency_limit)
        ax0.set_ylim(0, 1.1 * np.max(mean_profile))
        ax0.set_xlabel('Frequency, Hz', fontsize=10, fontweight='bold')
        ax0.set_ylabel('Amplitude, AU', fontsize=10, fontweight='bold')
        ax0.set_title('Averaged spectra over all DMs', fontsize=8, fontweight='bold')
        self.figure_integrated_spectra_over_dms_t4_l2.set_constrained_layout(True)
        self.canvas_integrated_spectra_over_dms_t4_l2.draw()  # refresh canvas
        del mean_profile

        # Update the plot 4
        self.figure_spectrum_for_dm_t4_l2.clear()  # clearing figure
        ax0 = self.figure_spectrum_for_dm_t4_l2.add_subplot(111)
        # ax0.plot(self.frequency_axis_cut, self.vdm_spectra_cut[man_dm_index])
        ax0.plot(self.frequency_axis_cut, vdm_spectra_to_plot[man_dm_index])
        ax0.set_xlim(self.low_freq_limit_of_filter, self.high_frequency_limit)
        # ax0.set_ylim(0, 1.1 * np.max(self.vdm_spectra_cut[man_dm_index]))
        ax0.set_ylim(0, 1.1 * np.max(vdm_spectra_to_plot[man_dm_index]))
        ax0.set_xlabel('Frequency, Hz', fontsize=10, fontweight='bold')
        ax0.set_ylabel('Amplitude, AU', fontsize=10, fontweight='bold')
        ax0.set_title('Spectrum for DM = ' + str(np.round(self.vdm_dm_vector[man_dm_index], 3)) + f' pc/cm\N{SUPERSCRIPT THREE}', fontsize=8, fontweight='bold')
        self.figure_spectrum_for_dm_t4_l2.set_constrained_layout(True)
        self.canvas_spectrum_for_dm_t4_l2.draw()  # refresh canvas

        del vdm_spectra_to_plot







    #############################################################
    #              T A B    5    F U N C T I O N S              #
    #############################################################




    def thread_plot_or_update_figures_tab_5(self):
               

        # Starting the thread of FFT calculation
        t0 = Thread(target=self.plot_or_update_figures_tab_5)
        t0.start()
        # t0.join()


    def plot_or_update_figures_tab_5(self):
        
        # Manually selected DM read from slider
        man_dm_index = int(self.slider_dm_selection_t4l1.value())

        # Update the plot 1
        self.figure_spectrum_for_dm_t5_l2.clear()  # clearing figure
        ax0 = self.figure_spectrum_for_dm_t5_l2.add_subplot(111)
        ax0.plot(self.frequency_axis_cut, self.vdm_spectra_cut[man_dm_index])
        ax0.set_xlim(self.low_freq_limit_of_filter, self.high_frequency_limit)
        ax0.set_xlabel('Frequency, Hz', fontsize=10, fontweight='bold')
        ax0.set_ylabel('Amplitude, AU', fontsize=10, fontweight='bold')
        ax0.set_title('Spectrum for DM = ' + str(np.round(self.vdm_dm_vector[man_dm_index], 3)), fontsize=8, fontweight='bold')
        self.figure_spectrum_for_dm_t5_l2.set_constrained_layout(True)
        self.canvas_spectrum_for_dm_t5_l2.draw()  # refresh canvas


        self.vdm_spectra_target_cut = self.vdm_spectra_cut[man_dm_index]

        # Calculate FFT of spectrum
        self.vdm_spectra_2_cut = np.power(np.real(np.fft.fft(self.vdm_spectra_target_cut)), 2)  # calculation of the spectrum
        self.vdm_spectra_2_cut = self.vdm_spectra_2_cut[0 : int(self.vdm_spectra_2_cut.shape[0]/2)]  # delete second part of the spectrum

        # Normalizing spectrum
        self.vdm_spectra_2_cut = self.vdm_spectra_2_cut - np.min(self.vdm_spectra_2_cut)
        self.vdm_spectra_2_cut = self.vdm_spectra_2_cut / np.max(self.vdm_spectra_2_cut)
        self.vdm_spectra_2_cut[0:10] = 0.0

        # Update the plot 2
        self.figure_spectrum_of_spectrum_t5_l3.clear()  # clearing figure
        ax0 = self.figure_spectrum_of_spectrum_t5_l3.add_subplot(111)
        ax0.plot(self.vdm_spectra_2_cut)
        ax0.set_xlim(0, len(self.vdm_spectra_2_cut))
        ax0.set_xlabel('Frequency^2', fontsize=10, fontweight='bold')
        ax0.set_ylabel('Amplitude, AU', fontsize=10, fontweight='bold')
        ax0.set_title('Spectrum of spectrum for DM = ' + str(np.round(self.vdm_dm_vector[man_dm_index], 3)), fontsize=8, fontweight='bold')
        self.figure_spectrum_of_spectrum_t5_l3.set_constrained_layout(True)
        self.canvas_spectrum_of_spectrum_t5_l3.draw()  # refresh canvas



# Driver code
if __name__ == '__main__':
    app = QApplication(sys.argv)  # creating apyqt5 application
    main = Window()  # creating a window object
    main.show()  # showing the window

    sys.exit(app.exec_())  # loop
