from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLabel
from PyQt5.QtWidgets import QTabWidget, QPushButton, QDoubleSpinBox, QAbstractSpinBox, QRadioButton, QLineEdit
from PyQt5.QtWidgets import QFileDialog, QPlainTextEdit
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import *

from threading import *
import matplotlib.pyplot as plt
from matplotlib import rc
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
from package_pulsar_profile_analysis_gui.f_make_transient_profile_from_jds import make_transient_profile_from_jds
from package_pulsar_profile_analysis_gui.f_make_transient_profile_from_jds_file_pairs import (
    f_make_transient_profile_from_jds_file_pairs)
from package_pulsar_profile_analysis_gui.f_time_profile_spectra_for_gui import time_profile_spectra_for_gui_1_8
from package_pulsar_profile_analysis_gui.f_time_profile_spectra_for_gui import time_profile_spectra_for_gui_16
from package_pulsar_profile_analysis_gui.f_xlsx_vvz_pulsar_sources_reader import xlsx_vvz_pulsar_sources_reader

from package_common_modules.text_manipulations import read_one_value_txt_file
from package_common_modules.text_manipulations import separate_filename_and_path
from package_ra_data_processing.filtering import median_filter


# Keep in mind that for Linux (Ubuntu 22.04) you may will need to use headless opencv:
# pip uninstall opencv-python
# pip install opencv-python-headless

software_version = '2024.07.21'


# Main window
class Window(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window geometry and hierarchy
        self.setWindowTitle('Pulsar & transient search    v.' + software_version + '    Serge Yerin @ IRA NASU')  # Win title
        self.setGeometry(100, 100, 800, 600)
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
        # self.tabs.addTab(self.tab4, "Analyze 16 parts")
        # self.tabs.addTab(self.tab5, "Process Excel DB")

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
        self.button_calc_dm.clicked.connect(self.calculate_dm_values)  # adding action to the button  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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


        # Button "Preprocess jds files"
        self.button_process_jds = QPushButton('Preprocess jds files')
        self.button_process_jds.clicked.connect(self.thread_preprocess_jds_files)  # adding action to the button
        self.button_process_jds.setEnabled(False)
        self.tab1.layout.addWidget(self.button_process_jds, 7, 1, Qt.AlignTop)

        # JDS processing status label
        self.label_processing_status = QLabel('', self)
        self.label_processing_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_processing_status.setFont(QFont('Arial', 14))
        self.tab1.layout.addWidget(self.label_processing_status, 8, 1)



        # First tab third part
        self.radiobutton_pairs = QRadioButton("Raw .jds pairs preprocess:")
        self.radiobutton_pairs.process_type = "raw jds pairs files"
        self.radiobutton_pairs.toggled.connect(self.rb_pairs_on_click)
        self.tab1.layout.addWidget(self.radiobutton_pairs, 9, 0)  # , Qt.AlignTop

        # Path to source folder line
        self.source_pairs_path_line = QLineEdit()
        self.source_pairs_path_line.setEnabled(False)
        self.tab1.layout.addWidget(self.source_pairs_path_line, 9, 1)

        # Button "Specify result folder"
        self.button_select_pairs_source_path = QPushButton('Specify source folder')
        self.button_select_pairs_source_path.clicked.connect(self.specify_source_pairs_folder_dialog)  # add new action!!!
        self.button_select_pairs_source_path.setFixedSize(QSize(150, 30))
        self.button_select_pairs_source_path.setEnabled(False)
        self.tab1.layout.addWidget(self.button_select_pairs_source_path, 9, 2)

        # Path to result folder line
        self.result_pairs_path_line = QLineEdit()
        self.result_pairs_path_line.setEnabled(False)
        self.tab1.layout.addWidget(self.result_pairs_path_line, 10, 1)

        # Button "Specify result folder"
        self.button_select_pairs_result_path = QPushButton('Specify result folder')
        self.button_select_pairs_result_path.clicked.connect(self.specify_result_pairs_folder_dialog)  # adding action
        self.button_select_pairs_result_path.setFixedSize(QSize(150, 30))
        self.button_select_pairs_result_path.setEnabled(False)
        self.tab1.layout.addWidget(self.button_select_pairs_result_path, 10, 2)

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
        self.tab1.layout.addLayout(self.pairs_dm_entry_layout, 11, 1)

        # Button "Preprocess pairs of jds files"
        self.button_process_pairs_jds = QPushButton('Preprocess pairs of jds files from specified folder')
        self.button_process_pairs_jds.clicked.connect(self.thread_preprocess_pairs_jds_files)  # adding action
        self.button_process_pairs_jds.setEnabled(False)
        self.tab1.layout.addWidget(self.button_process_pairs_jds, 12, 1, Qt.AlignTop)

        # JDS pairs processing status label
        self.label_pairs_processing_status = QLabel('', self)
        self.label_pairs_processing_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pairs_processing_status.setFont(QFont('Arial', 14))
        self.tab1.layout.addWidget(self.label_pairs_processing_status, 13, 1)



        # Adding stretch lines to get all elements pulled to top
        self.tab1.layout.setRowStretch(self.tab1.layout.rowCount(), 1)
        # self.tab1.layout.setColumnStretch(self.tab1.layout.columnCount(), 1)

        self.tab1.setLayout(self.tab1.layout)







        ##############################
        #         Second tab         #
        ##############################

        # Layouts in the second tab
        self.tab2.layout = QVBoxLayout(self.tab2)
        self.input_controls_layout_t2 = QHBoxLayout()

        # self.time_resolution = (1 / 66000000) * 16384 * 32  # Data time resolution, s   # 0.007944

        # Creating labels near spinboxes to describe the input
        self.label_median_win = QLabel("Median window:", self)
        self.label_median_win.setFixedSize(QSize(90, 30))
        self.label_median_win.setAlignment(QtCore.Qt.AlignCenter)

        # self.label_low_limit_input = QLabel("Lower limit", self)
        # self.label_low_limit_input.setFixedSize(QSize(70, 30))
        # self.label_low_limit_input.setWordWrap(True)  # making label multi line
        # self.label_low_limit_input.setAlignment(QtCore.Qt.AlignCenter)

        # self.label_high_limit_input = QLabel("Higher limit", self)
        # self.label_high_limit_input.setFixedSize(QSize(70, 30))
        # self.label_high_limit_input.setWordWrap(True)  # making label multi line
        # self.label_high_limit_input.setAlignment(QtCore.Qt.AlignCenter)

        # self.label_aver_const = QLabel("Average window", self)
        # self.label_aver_const.setFixedSize(QSize(90, 30))
        # self.label_aver_const.setWordWrap(True)  # making label multi line
        # self.label_aver_const.setAlignment(QtCore.Qt.AlignCenter)

        self.filter_win_input = QDoubleSpinBox()
        self.filter_win_input.setFixedSize(QSize(70, 30))
        self.filter_win_input.setMinimum(0)
        self.filter_win_input.setMaximum(100000)
        self.filter_win_input.setValue(100)

        # Main plot window
        self.figure_time = plt.figure()  # a figure instance to plot on
        self.canvas_time = FigureCanvas(self.figure_time)  # takes the 'figure' instance as a parameter to __init__

        # This is the Matplotlib Navigation widget it takes the Canvas widget and a parent
        self.toolbar_time = NavigationToolbar(self.canvas_time, self)

        # Button "Read data"
        self.button_read_time = QPushButton('Read data')
        self.button_read_time.clicked.connect(self.thread_read_initial_data)  # adding action to the button
        self.button_read_time.setFixedSize(QSize(100, 30))

        # Button "Subtract median"
        self.button_filter_time = QPushButton('Subtract median')
        self.button_filter_time.clicked.connect(self.thread_subtract_median_in_time)  # adding action to the button
        self.button_filter_time.setFixedSize(QSize(110, 30))

        # Work tatus label tab 2
        self.label_processing_status_t2 = QLabel('', self)
        self.label_processing_status_t2.setFixedSize(QSize(300, 30))
        self.label_processing_status_t2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_processing_status_t2.setFont(QFont('Arial', 14))

        # Packing layouts in the window
        self.input_controls_layout_t2.addWidget(self.button_read_time)
        self.input_controls_layout_t2.addWidget(self.label_median_win)
        self.input_controls_layout_t2.addWidget(self.filter_win_input)
        self.input_controls_layout_t2.addWidget(self.button_filter_time)
        self.input_controls_layout_t2.addWidget(self.label_processing_status_t2)
        # self.input_controls_layout.addWidget(self.label_aver_const)
        # self.input_controls_layout.addWidget(self.aver_const_input)
        # self.input_controls_layout.addWidget(self.button_average)
        # self.input_controls_layout.addWidget(self.label_low_limit_input)
        # self.input_controls_layout.addWidget(self.low_limit_input)
        # self.input_controls_layout.addWidget(self.label_high_limit_input)
        # self.input_controls_layout.addWidget(self.high_limit_input)
        # self.input_controls_layout.addWidget(self.button_crop)

        self.tab2.layout.addLayout(self.input_controls_layout_t2)
        
        self.toolbar_layout_t2 = QHBoxLayout()

        # # Creating labels to indicate the initial time resolution
        # label = "Initial time resolution assumed: {:8.4f}".format(np.round(self.time_resolution * 1000, 6)) + "  ms."
        # self.label_time_resolution = QLabel(label, self)
        # self.label_time_resolution.setFixedSize(QSize(300, 30))
        # self.label_time_resolution.setAlignment(QtCore.Qt.AlignCenter)

        # self.frequency_limit = 10  # Hz
        # self.label_freq_resolution = QLabel('Fig frequency limit:', self)
        # self.label_freq_resolution.setFixedSize(QSize(100, 30))
        # self.label_freq_resolution.setAlignment(QtCore.Qt.AlignCenter)

        # self.label_hz = QLabel('Hz', self)
        # self.label_hz.setFixedSize(QSize(15, 30))
        # self.label_hz.setAlignment(QtCore.Qt.AlignCenter)


        # self.freq_limit_input = QDoubleSpinBox()
        # self.freq_limit_input.setStepType(step_type)
        # self.freq_limit_input.setMinimum(0.0)
        # self.freq_limit_input.setFixedSize(QSize(60, 30))
        # self.freq_limit_input.setValue(self.frequency_limit)


        self.toolbar_layout_t2.addWidget(self.toolbar_time)
        # self.toolbar_layout_t2.addWidget(self.label_time_resolution)
        # self.toolbar_layout_t2.addWidget(self.label_freq_resolution)
        # self.toolbar_layout_t2.addWidget(self.freq_limit_input)
        # self.toolbar_layout_t2.addWidget(self.label_hz)
        
        self.tab2.layout.addLayout(self.toolbar_layout_t2)
        self.tab2.layout.addWidget(self.canvas_time)

        self.tab2.setLayout(self.tab2.layout)




        ##############################################
        #         Third tab - Spectral domain        #
        ##############################################

        # Layouts in the third tab
        self.tab3.layout = QVBoxLayout(self.tab3)
        self.input_controls_layout_t3 = QHBoxLayout()

        # # Creating labels near spinboxes to describe the input
        # self.label_median_win = QLabel("Median window:", self)
        # self.label_median_win.setFixedSize(QSize(90, 30))
        # self.label_median_win.setAlignment(QtCore.Qt.AlignCenter)

        # self.label_low_limit_input = QLabel("Lower limit", self)
        # self.label_low_limit_input.setFixedSize(QSize(70, 30))
        # self.label_low_limit_input.setWordWrap(True)  # making label multi line
        # self.label_low_limit_input.setAlignment(QtCore.Qt.AlignCenter)

        # self.label_high_limit_input = QLabel("Higher limit", self)
        # self.label_high_limit_input.setFixedSize(QSize(70, 30))
        # self.label_high_limit_input.setWordWrap(True)  # making label multi line
        # self.label_high_limit_input.setAlignment(QtCore.Qt.AlignCenter)

        # self.label_aver_const = QLabel("Average window", self)
        # self.label_aver_const.setFixedSize(QSize(90, 30))
        # self.label_aver_const.setWordWrap(True)  # making label multi line
        # self.label_aver_const.setAlignment(QtCore.Qt.AlignCenter)

        # # Selection of limits with spinboxes

        # self.filter_win_input = QDoubleSpinBox()
        # self.filter_win_input.setFixedSize(QSize(70, 30))
        # self.filter_win_input.setMinimum(0)
        # self.filter_win_input.setMaximum(100000)
        # self.filter_win_input.setValue(100)

        # self.aver_const_input = QDoubleSpinBox()
        # self.aver_const_input.setFixedSize(QSize(60, 30))
        # self.aver_const_input.setMinimum(1)
        # self.aver_const_input.setMaximum(300)
        # self.aver_const_input.setValue(1)


        # self.low_limit_input = QDoubleSpinBox()
        # self.low_limit_input.setStepType(step_type)
        # self.low_limit_input.setMinimum(-10.0)
        # self.low_limit_input.setFixedSize(QSize(60, 30))
        # self.low_limit_input.setValue(-3)

        # self.high_limit_input = QDoubleSpinBox()
        # self.high_limit_input.setStepType(step_type)
        # self.high_limit_input.setMinimum(-10.0)
        # self.high_limit_input.setFixedSize(QSize(60, 30))
        # self.high_limit_input.setValue(3)

        # Main plot window
        self.figure_freq = plt.figure()  # a figure instance to plot on
        self.canvas_freq = FigureCanvas(self.figure_freq)  # takes the 'figure' instance as a parameter to __init__

        # This is the Matplotlib Navigation widget it takes the Canvas widget and a parent
        self.toolbar_freq = NavigationToolbar(self.canvas_freq, self)

        # Button "Read data"
        self.button_calc_fft = QPushButton('Calculate FFT')
        self.button_calc_fft.clicked.connect(self.thread_calculate_fft_of_data)  # adding action to the button
        self.button_calc_fft.setFixedSize(QSize(100, 30))

        # # Button "Subtract median"
        # self.button_filter = QPushButton('Subtract median')
        # self.button_filter.clicked.connect(self.subtract_median)  # adding action to the button
        # self.button_filter.setFixedSize(QSize(110, 30))

        # # Button "Average data"
        # self.button_average = QPushButton('Moving average')
        # self.button_average.clicked.connect(self.average_time_data)  # adding action to the button
        # self.button_average.setFixedSize(QSize(110, 30))

        # # Button "Crop data"
        # self.button_crop = QPushButton('Crop data')
        # self.button_crop.clicked.connect(self.crop_and_show_spectrum)  # adding action to the button
        # self.button_crop.setFixedSize(QSize(100, 30))

        # Work status label tab 3 
        self.label_processing_status_t3 = QLabel('', self)
        self.label_processing_status_t3.setFixedSize(QSize(300, 30))
        self.label_processing_status_t3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_processing_status_t3.setFont(QFont('Arial', 14))

        # Packing layouts in the window
        # self.input_controls_layout.addWidget(self.label_median_win)
        # self.input_controls_layout.addWidget(self.filter_win_input)
        self.input_controls_layout_t3.addWidget(self.button_calc_fft)
        self.input_controls_layout_t3.addWidget(self.label_processing_status_t3)
        # self.input_controls_layout.addWidget(self.button_filter)
        # self.input_controls_layout.addWidget(self.label_aver_const)
        # self.input_controls_layout.addWidget(self.aver_const_input)
        # self.input_controls_layout.addWidget(self.button_average)
        # self.input_controls_layout.addWidget(self.label_low_limit_input)
        # self.input_controls_layout.addWidget(self.low_limit_input)
        # self.input_controls_layout.addWidget(self.label_high_limit_input)
        # self.input_controls_layout.addWidget(self.high_limit_input)
        # self.input_controls_layout.addWidget(self.button_crop)

        self.tab3.layout.addLayout(self.input_controls_layout_t3)
        
        self.toolbar_frequency_layout_t3 = QHBoxLayout()

        # Creating labels to indicate the initial time resolution
        label = "Initial time resolution assumed: {:8.4f}".format(np.round(self.time_resolution * 1000, 6)) + "  ms."
        self.label_time_resolution = QLabel(label, self)
        self.label_time_resolution.setFixedSize(QSize(300, 30))
        self.label_time_resolution.setAlignment(QtCore.Qt.AlignCenter)

        self.label_freq_limit = QLabel('Fig frequency limit:', self)
        self.label_freq_limit.setFixedSize(QSize(100, 30))
        self.label_freq_limit.setAlignment(QtCore.Qt.AlignCenter)

        self.label_hz = QLabel('Hz', self)
        self.label_hz.setFixedSize(QSize(15, 30))
        self.label_hz.setAlignment(QtCore.Qt.AlignCenter)

        frequency_limit_init = 10  # Hz
        step_type = QAbstractSpinBox.AdaptiveDecimalStepType  # step type

        self.freq_limit_input = QDoubleSpinBox()
        self.freq_limit_input.setStepType(step_type)
        self.freq_limit_input.setMinimum(0.0)
        self.freq_limit_input.setFixedSize(QSize(60, 30))
        self.freq_limit_input.setValue(frequency_limit_init)

        self.toolbar_frequency_layout_t3.addWidget(self.toolbar_freq)
        self.toolbar_frequency_layout_t3.addWidget(self.label_time_resolution)
        self.toolbar_frequency_layout_t3.addWidget(self.label_freq_limit)
        self.toolbar_frequency_layout_t3.addWidget(self.freq_limit_input)
        self.toolbar_frequency_layout_t3.addWidget(self.label_hz)
        
        self.tab3.layout.addLayout(self.toolbar_frequency_layout_t3)
        self.tab3.layout.addWidget(self.canvas_freq)

        self.tab3.setLayout(self.tab3.layout)




        # ##############################
        # #         Third tab         # 4
        # ##############################

        # # Third tab
        # self.tab3.layout = QVBoxLayout(self.tab3)
        # self.input_controls_layout_t3 = QHBoxLayout()

        # # Button "Plot data 1-8"
        # self.button_plot_1_8 = QPushButton('Plot parts of data from 1 to 8')
        # self.button_plot_1_8.clicked.connect(self.plot_spectra_1_8)  # adding action to the button
        # self.button_plot_1_8.setFixedSize(QSize(250, 30))
        # self.input_controls_layout_t3.addWidget(self.button_plot_1_8)

        # # Button "Save data 1-8"
        # self.button_save_1_8 = QPushButton('Save image of data from 1 to 8')
        # self.button_save_1_8.clicked.connect(self.save_spectra_1_8)  # adding action to the button
        # self.button_save_1_8.setFixedSize(QSize(250, 30))
        # self.input_controls_layout_t3.addWidget(self.button_save_1_8)

        # # Main plot window
        # self.figure_1_8 = plt.figure()  # a figure instance to plot on
        # self.canvas_1_8 = FigureCanvas(self.figure_1_8)  # takes the 'figure' instance as a parameter to __init__

        # # Packing into layouts
        # self.tab3.layout.addLayout(self.input_controls_layout_t3)
        # self.tab3.layout.addWidget(self.canvas_1_8)

        # self.tab3.setLayout(self.tab3.layout)






        # ##############################
        # #         Fourth tab         # 5
        # ##############################

        # # Fourth tab
        # self.tab4.layout = QVBoxLayout(self.tab4)
        # self.input_controls_layout_t4 = QHBoxLayout()

        # # Button "Plot data 16"
        # self.button_plot_16 = QPushButton('Plot parts of data 16 of 16')
        # self.button_plot_16.clicked.connect(self.plot_spectra_16)  # adding action to the button
        # self.button_plot_16.setFixedSize(QSize(250, 30))
        # self.input_controls_layout_t4.addWidget(self.button_plot_16)

        # # Button "Save data 16"
        # self.button_save_16 = QPushButton('Save image of data 16 of 16')
        # self.button_save_16.clicked.connect(self.save_spectra_16)  # adding action to the button
        # self.button_save_16.setFixedSize(QSize(250, 30))
        # self.input_controls_layout_t4.addWidget(self.button_save_16)

        # # Main plot window
        # self.figure_16 = plt.figure()  # a figure instance to plot on
        # self.canvas_16 = FigureCanvas(self.figure_16)  # takes the 'figure' instance as a parameter to __init__

        # # Packing into layouts
        # self.tab4.layout.addLayout(self.input_controls_layout_t4)
        # self.tab4.layout.addWidget(self.canvas_16)
        # self.tab4.setLayout(self.tab4.layout)




        # ##############################
        # #         Fifth tab          #
        # ##############################

        # self.tab5.layout = QVBoxLayout(self.tab5) 
        # self.tab_5_folder_selection_layout = QGridLayout() 

        # # Label of path to xlsx file
        # self.label_txt_file_selected = QLabel('Path to XLS file: ', self)
        # self.tab_5_folder_selection_layout.addWidget(self.label_txt_file_selected, 0, 0)

        # # Path to excel DB file line
        # self.xlsx_file_path_line = QLineEdit()  
        # excel_file_path = 'TP_corrected_for_VV_2017_June27.xlsx'
        # self.xlsx_file_path_line.setText(excel_file_path)
        # self.tab_5_folder_selection_layout.addWidget(self.xlsx_file_path_line, 0, 1)

        # # Button "Open excel file"
        # self.button_open_xlsx = QPushButton('Open xls file')
        # self.button_open_xlsx.clicked.connect(self.one_xls_file_open_dialog)
        # self.button_open_xlsx.setFixedSize(QSize(150, 30))
        # self.tab_5_folder_selection_layout.addWidget(self.button_open_xlsx, 0, 2)

        # # Label of path to data to process
        # self.label_data_path_replace = QLabel('Path to data folder (to replace): ', self)
        # self.tab_5_folder_selection_layout.addWidget(self.label_data_path_replace, 1, 0)

        # # Path to excel DB file line
        # self.data_path_replace_line = QLineEdit()  
        # self.data_path_replace_line.setText('E:/data/')
        # self.tab_5_folder_selection_layout.addWidget(self.data_path_replace_line, 1, 1)

        # # Button "Specify data folder to replace"
        # self.button_data_path_replace = QPushButton('Specify folder')
        # self.button_data_path_replace.clicked.connect(self.specify_db_data_folder_dialog)  # add new action!!!
        # self.button_data_path_replace.setFixedSize(QSize(150, 30))
        # self.tab_5_folder_selection_layout.addWidget(self.button_data_path_replace, 1, 2)




        # # Label of path big folder with intermediate data
        # self.big_temp_data_path_label = QLabel('Path to big temp folder: ', self)
        # self.tab_5_folder_selection_layout.addWidget(self.big_temp_data_path_label, 2, 0)

        # # Path to excel DB file line
        # self.big_temp_data_path_line = QLineEdit()  
        # self.big_temp_data_path_line.setText('E:/temp/')
        # self.tab_5_folder_selection_layout.addWidget(self.big_temp_data_path_line, 2, 1)

        # # Button "Specify data folder to replace"
        # self.button_big_temp_data_path = QPushButton('Specify folder')
        # self.button_big_temp_data_path.clicked.connect(self.specify_big_temp_data_path_dialog)  
        # self.button_big_temp_data_path.setFixedSize(QSize(150, 30))
        # self.tab_5_folder_selection_layout.addWidget(self.button_big_temp_data_path, 2, 2)






        # self.tab_5_input_controls_layout = QGridLayout()

        # # Creating labels near spinboxes to describe the input
        # self.t5_label_median_win = QLabel("Median window:", self)
        # self.t5_label_median_win.setFixedSize(QSize(100, 30))
        # self.t5_label_median_win.setAlignment(QtCore.Qt.AlignCenter)

        # self.t5_label_low_limit_input = QLabel("Lower limit", self)
        # self.t5_label_low_limit_input.setFixedSize(QSize(100, 30))
        # self.t5_label_low_limit_input.setWordWrap(True)  # making label multi line
        # self.t5_label_low_limit_input.setAlignment(QtCore.Qt.AlignCenter)

        # self.t5_label_high_limit_input = QLabel("Higher limit", self)
        # self.t5_label_high_limit_input.setFixedSize(QSize(100, 30))
        # self.t5_label_high_limit_input.setWordWrap(True)  # making label multi line
        # self.t5_label_high_limit_input.setAlignment(QtCore.Qt.AlignCenter)

        # # Selection of limits with spinboxes

        # self.t5_filter_win_input = QDoubleSpinBox()
        # self.t5_filter_win_input.setFixedSize(QSize(100, 30))
        # self.t5_filter_win_input.setMinimum(0)
        # self.t5_filter_win_input.setMaximum(100000)
        # self.t5_filter_win_input.setValue(300)

        # step_type = QAbstractSpinBox.AdaptiveDecimalStepType  # step type

        # self.t5_low_limit_input = QDoubleSpinBox()
        # self.t5_low_limit_input.setStepType(step_type)
        # self.t5_low_limit_input.setMinimum(-10.0)
        # self.t5_low_limit_input.setFixedSize(QSize(100, 30))
        # self.t5_low_limit_input.setValue(-3)

        # self.t5_high_limit_input = QDoubleSpinBox()
        # self.t5_high_limit_input.setStepType(step_type)
        # self.t5_high_limit_input.setMinimum(-10.0)
        # self.t5_high_limit_input.setFixedSize(QSize(100, 30))
        # self.t5_high_limit_input.setValue(3)

        # # *** Middle nested layout ***
        # self.tab_5_process_start_layout = QVBoxLayout()

        # # Button "Start data processing"
        # self.t5_button_process = QPushButton('Start data processing')
        # self.t5_button_process.clicked.connect(self.thread_t5_start_processing)  # adding action to the button !!!!!!!!!!!!!!!!!!!!

        # # Processing status label
        # self.t5_label_processing_status = QLabel('Waiting to enter data and start processing', self)
        # self.t5_label_processing_status.setAlignment(QtCore.Qt.AlignCenter)
        # self.t5_label_processing_status.setFont(QFont('Arial', 14))
        
        # # *** Lower nested layouts ***
        # self.tab_5_two_column_layout = QVBoxLayout()
        # self.tab_5_additional_parameters_layout = QGridLayout()
        # self.tab_5_text_field_layout = QVBoxLayout()

		# # Text field
        # self.t5_text_field = QPlainTextEdit()

        # # Packing widgets to the layouts
        # self.tab_5_input_controls_layout.addWidget(self.t5_label_median_win, 0, 0)
        # self.tab_5_input_controls_layout.addWidget(self.t5_filter_win_input, 0, 1)
        # self.tab_5_input_controls_layout.addWidget(self.t5_label_low_limit_input, 0, 2)
        # self.tab_5_input_controls_layout.addWidget(self.t5_low_limit_input, 0, 3)
        # self.tab_5_input_controls_layout.addWidget(self.t5_label_high_limit_input, 0, 4)
        # self.tab_5_input_controls_layout.addWidget(self.t5_high_limit_input, 0, 5)
        # self.tab_5_process_start_layout.addWidget(self.t5_button_process)
        # self.tab_5_process_start_layout.addWidget(self.t5_label_processing_status)
        # self.tab_5_text_field_layout.addWidget(self.t5_text_field)

        # # Packing all layouts in the tab
        # self.tab5.layout.addLayout(self.tab_5_folder_selection_layout)
        # self.tab5.layout.addLayout(self.tab_5_input_controls_layout)
        # self.tab5.layout.addLayout(self.tab_5_process_start_layout)
        # self.tab5.layout.addLayout(self.tab_5_two_column_layout)
        # self.tab_5_two_column_layout.addLayout(self.tab_5_additional_parameters_layout)
        # self.tab_5_two_column_layout.addLayout(self.tab_5_text_field_layout)

        # # Modifying layouts
        # self.tab_5_folder_selection_layout.setRowStretch(self.tab_5_folder_selection_layout.rowCount(), 1)
        # self.tab_5_input_controls_layout.setRowStretch(self.tab_5_input_controls_layout.rowCount(), 1)
        # # self.tab_5_process_start_layout.setStretch(self.tab_5_process_start_layout.rowCount(), 1)
        # self.tab5.setLayout(self.tab5.layout)
        




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
            self.button_process_jds.setEnabled(True)
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
            self.vdm_filepath, self.vdm_filename = separate_filename_and_path(file)
            self.vdm_file_path_line.setText(file)


    def calculate_dm_values(self):
        self.central_dm = float(self.line_dm_entry.text().replace(',', '.'))
        self.dm_range = float(self.line_dm_range_entry.text().replace(',', '.'))
        self.dm_points = int(self.line_dm_points_entry.text().replace(',', '.'))

        # Calculating DM vector to display DM values
        self.dm_vector = np.linspace(self.central_dm - self.dm_range, self.central_dm + self.dm_range, num=self.dm_points)

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
                directory, file_name = separate_filename_and_path(files[i])
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

        # Only if parameters are good, run processing
        self.label_processing_status.setText("JDS data are being processed...")
        self.label_processing_status.setStyleSheet("background-color: yellow;")

        try:
            profile_txt_file_path = make_transient_profile_from_jds(self.jds_analysis_directory,
                                                                    jds_analysis_files,
                                                                    jds_result_folder,
                                                                    self.source_dm)
        except:
            self.label_processing_status.setText("Something wrong happened during calculations!")
            self.label_processing_status.setStyleSheet("background-color: red;")
            return

        # After the processing is finished,
        self.txt_file_path_line.setText(profile_txt_file_path)
        self.txt_filepath, self.txt_filename = separate_filename_and_path(profile_txt_file_path)
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

    # Thread called by the push button "Read data" on tab 2
    def thread_read_initial_data(self):
        
        self.figure_time.clear()  # clearing figure
        ax0 = self.figure_time.add_subplot(111)
        ax0.remove() 
        self.figure_time.text(0.4, 0.5, "Reading data file...", color="C0", size=22)
        self.canvas_time.draw()  # refresh canvas

        self.label_processing_status_t2.setText("Processing...")
        self.label_processing_status_t2.setStyleSheet("background-color: yellow;")
        
        t0 = Thread(target=self.read_initial_data)
        t0.start()


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

        # Calculating DM vector to have all DM values used
        self.vdm_dm_vector = np.linspace( self.vdm_central_dm - self.vdm_dm_range,  
                                         self.vdm_central_dm + self.vdm_dm_range, 
                                         num=self.vdm_dm_points)

        self.figure_time.clear()  # clearing figure
        ax0 = self.figure_time.add_subplot(111)
        plot = ax0.imshow(self.vdm_data_array, 
                          extent=[0,  self.time_points_num, self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]], 
                          aspect='auto', cmap="Greys")
        # ax0.axis([self.low_freq_limit_of_filter, self.high_frequency_limit,  self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]])
        ax0.set_xlabel('Time, points', fontsize=12, fontweight='bold')
        ax0.set_ylabel('DM, pc * cm-3', fontsize=12, fontweight='bold')
        ax0.set_title('Time profiles vs. DM value', fontsize=10, fontweight='bold')
        self.figure_time.set_constrained_layout(True)
        self.figure_time.colorbar(plot, pad=0, aspect=50, label="Amplitude, AU")  # , orientation="horizontal"
        self.canvas_time.draw()  # refresh canvas

        self.label_processing_status_t2.setText(" ")
        self.label_processing_status_t2.setStyleSheet("background-color: light grey;")


    #
    #
    #
    #
    #

    # Thread called by the push button "Subtract median" on tab 2
    def thread_subtract_median_in_time(self):

        self.label_processing_status_t2.setText("Processing...")
        self.label_processing_status_t2.setStyleSheet("background-color: yellow;")

        t0 = Thread(target=self.subtract_median_in_time)
        t0.start()


    # Action called by the push button "Subtract median" on tab 2
    def subtract_median_in_time(self):

        # Subtract median
        self.med_filter_length = int(self.filter_win_input.value())
        median = scipy.ndimage.median_filter(self.vdm_data_array, self.med_filter_length, axes=1)
        self.vdm_data_array = self.vdm_data_array - median

        # Updating figure on tab 2
        self.figure_time.clear()  # clearing figure
        ax0 = self.figure_time.add_subplot(111)
        plot = ax0.imshow(self.vdm_data_array, 
                          extent=[0, self.time_points_num, self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]], 
                          aspect='auto', cmap="Greys")
        # ax0.axis([self.low_freq_limit_of_filter, self.high_frequency_limit,  self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]])
        ax0.set_xlabel('Time, points', fontsize=12, fontweight='bold')
        ax0.set_ylabel('DM, pc * cm-3', fontsize=12, fontweight='bold')
        ax0.set_title('Time profiles vs. DM value', fontsize=10, fontweight='bold')
        self.figure_time.set_constrained_layout(True)
        self.figure_time.colorbar(plot, pad=0, aspect=50, label="Amplitude, AU")  # , orientation="horizontal"
        self.canvas_time.draw()  # Refresh canvas
    
        self.label_processing_status_t2.setText(" ")
        self.label_processing_status_t2.setStyleSheet("background-color: light grey;")

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


    # Action called by the push button "Calculate FFT"
    def calculate_fft_of_data(self):

        # Calculating FFT
        self.vdm_spectra = np.power(np.real(np.fft.fft(self.vdm_data_array[:])), 2)  # calculation of the spectrum
        self.vdm_spectra = self.vdm_spectra[:, 0 : int(self.vdm_spectra.shape[1]/2)]  # delete second part of the spectrum

        # Calculating the frequency resolution and low frequency (median) filter limit 
        self.frequency_resolution = 1 / (self.time_resolution * 2 * self.vdm_spectra.shape[1])  # frequency resolution, Hz   
        self.low_freq_limit_of_filter = self.med_filter_length * self.frequency_resolution
        frequency_axis = [self.frequency_resolution * i for i in range(self.vdm_spectra.shape[1])]

        # Taking the high limit of frequency scale from GUI
        self.high_frequency_limit = int(self.freq_limit_input.value())  # Hz

        # Update the plot
        rc('font', size=12, weight='bold')
        self.figure_freq.clear()  # clearing figure
        ax0 = self.figure_freq.add_subplot(111)
        plot = ax0.imshow(self.vdm_spectra, 
                          extent=[frequency_axis[0], frequency_axis[-1], self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]], 
                          aspect='auto', cmap="Greys")
        ax0.axis([self.low_freq_limit_of_filter, self.high_frequency_limit,  self.vdm_dm_vector[0],  self.vdm_dm_vector[-1]])
        ax0.set_xlabel('Frequency, Hz', fontsize=12, fontweight='bold')
        ax0.set_ylabel('DM, pc * cm-3', fontsize=12, fontweight='bold')
        ax0.set_title('Time series', fontsize=10, fontweight='bold')
        self.figure_freq.set_constrained_layout(True)
        self.figure_freq.colorbar(plot, pad=0, aspect=50, label="Amplitude, AU")  # , orientation="horizontal"
        self.canvas_freq.draw()  # refresh canvas

        self.label_processing_status_t3.setText(" ")
        self.label_processing_status_t3.setStyleSheet("background-color: light grey;")
















    # action called by the push button Average data
    def average_time_data(self):

        pulsar_data_in_time = np.array(self.filtered_data_in_time)

        # Read the average value from the input
        average_const = int(self.aver_const_input.value())
        self.frequency_limit = float(self.freq_limit_input.value())
        
        # Make sure the length of the array is divisible by average constant
        # points_limit = (len(pulsar_data_in_time) // average_const) * average_const
        # pulsar_data_in_time = pulsar_data_in_time[:points_limit]
        print(len(pulsar_data_in_time))
        # Calculate the average and new time resolution
        # pulsar_data_in_time = np.average(pulsar_data_in_time.reshape(-1, average_const ), axis=1)
        pulsar_data_in_time = np.convolve(pulsar_data_in_time, np.ones(average_const), 'valid') / average_const
        self.filtered_data_in_time = pulsar_data_in_time / np.std(pulsar_data_in_time)
        # self.time_resolution = self.time_resolution * average_const
        print(len(pulsar_data_in_time))
        
        # Calculating the spectrum
        frequency_axis, pulses_spectra, spectrum_max = \
            calculate_spectrum_of_profile(self.filtered_data_in_time, self.time_resolution)

        # Update the plot
        self.figure.clear()  # clearing old figure
        ax0 = self.figure.add_subplot(211)
        ax0.plot(self.filtered_data_in_time)
        ax0.set_xlim([0, len(self.filtered_data_in_time)])
        ax0.set_ylim([-5.0, 5.0])
        ax0.set_title('Time series', fontsize=10, fontweight='bold')
        ax1 = self.figure.add_subplot(212)
        ax1.plot(frequency_axis, pulses_spectra)
        ax1.axis([0, self.frequency_limit, 0, 1.1 * spectrum_max])
        ax1.set_xlabel('Frequency, Hz', fontsize=10, fontweight='bold')
        self.figure.subplots_adjust(hspace=0.25, top=0.945)
        ax1.set_title('Spectrum', fontsize=10, fontweight='bold')
        self.canvas.draw()  # refresh canvas


    def crop_and_show_spectrum(self):

        # Getting current values from spinboxes
        min_limit = self.low_limit_input.value()
        max_limit = self.high_limit_input.value()
        self.frequency_limit = float(self.freq_limit_input.value())

        # Clip data
        self.cropped_data_in_time = np.clip(self.filtered_data_in_time, min_limit, max_limit)

        # Calculating the spectrum
        frequency_axis, pulses_spectra, spectrum_max = \
            calculate_spectrum_of_profile(self.cropped_data_in_time, self.time_resolution)

        self.harmonics_highlight = None

        def mouse_event(event):
            x = event.xdata
            self.harmonics_highlight = [0.5*x, x, 2*x, 3*x, 4*x, 5*x, 6*x, 7*x, 8*x, 9*x, 10*x,
                                        11*x, 12*x, 13*x, 14*x, 15*x, 16*x, 17*x, 18*x, 19*x, 20*x,
                                        21*x, 22*x, 23*x, 24*x, 25*x, 26*x, 27*x, 28*x, 29*x, 30*x]

            self.figure.clear()  # clearing old figure
            ax0 = self.figure.add_subplot(211)
            ax0.plot(self.cropped_data_in_time)
            ax0.set_xlim([0, len(self.cropped_data_in_time)])
            ax0.set_ylim([-5.0, 5.0])
            ax0.set_title('Time series', fontsize=10, fontweight='bold')
            ax1 = self.figure.add_subplot(212)
            plt.text(x, 0.8 * spectrum_max, ' $f$ = ' + str(np.round(x, 3)) + ' $Hz$ $or$ $P$ = ' +
                     str(np.round(1/x, 3)) + ' $s$', fontsize=14, color='C3')
            for harmonic in self.harmonics_highlight:
                ax1.axvline(x=harmonic, color='C1', linestyle='-', linewidth=2.0, alpha=0.2)
            ax1.plot(frequency_axis, pulses_spectra)
            ax1.axis([0, self.frequency_limit, 0, 1.1 * spectrum_max])
            ax1.set_xlabel('Frequency, Hz', fontsize=10, fontweight='bold')
            self.figure.subplots_adjust(hspace=0.25, top=0.945)
            ax1.set_title('Spectrum', fontsize=10, fontweight='bold')
            self.canvas.draw()  # refresh canvas

        # Update the plot
        cid = self.figure.canvas.mpl_connect('button_press_event', mouse_event)
        self.figure.clear()  # clearing old figure
        ax0 = self.figure.add_subplot(211)
        ax0.plot(self.cropped_data_in_time)
        ax0.set_xlim([0, len(self.cropped_data_in_time)])
        ax0.set_ylim([-5.0, 5.0])
        ax0.set_title('Time series', fontsize=10, fontweight='bold')
        ax1 = self.figure.add_subplot(212)
        # Adding the plots for parts of data to the big result picture
        ax1.plot(frequency_axis, pulses_spectra)
        ax1.axis([0, self.frequency_limit, 0, 1.1 * spectrum_max])
        ax1.set_xlabel('Frequency, Hz', fontsize=10, fontweight='bold')
        self.figure.subplots_adjust(hspace=0.25, top=0.945)
        ax1.set_title('Spectrum', fontsize=10, fontweight='bold')
        self.canvas.draw()  # refresh canvas


    def thread_t5_start_processing(self):
        self.t5_text_field.appendPlainText('Reading database...')
        t1 = Thread(target=self.t5_start_processing)
        t1.start()

    # action called by the push button
    def t5_start_processing(self):

        self.t5_label_processing_status.setText('Excel database file reading')
        self.t5_label_processing_status.setStyleSheet("background-color: lightgreen;")
        
        # Reading profile data from txt file
        try:
            excel_filepath = self.xlsx_file_path_line.text()
            db_data_path = self.data_path_replace_line.text()
            temp_big_folder = self.big_temp_data_path_line.text()
            excel_filepath = os.path.normpath(excel_filepath)
            db_data_path = os.path.normpath(db_data_path)
            temp_big_folder = os.path.normpath(temp_big_folder)
            [self.excel_directory, self.excel_filename] = os.path.split(excel_filepath)
            [code_date, beam, source_dm, file_paths] = xlsx_vvz_pulsar_sources_reader(self.excel_directory, self.excel_filename, 
                                                                                      'Лист1', db_data_path)

        except:
            self.t5_label_processing_status.setText('Error reading Excel database or data finding')
            self.t5_label_processing_status.setStyleSheet("background-color: red;")

        pairs_number = len(code_date)
        
        self.t5_text_field.clear()  # Cleat the text input to add new file paths
        
        obs_names = []
        for pair in range(pairs_number):
            tmp_filepath = file_paths[pair][0].split(os.sep)
            numbers = tmp_filepath[-2].split(' ')
            data_file_name = tmp_filepath[-1][:-4]

            obs_name = code_date[pair].replace('/','_') + '_{:0>2d}'.format(int(numbers[0])) + '_{:0>2d}'.format(int(numbers[1])) + \
                       '  beam ' + beam[pair] + '  DM={: >6}'.format(str(np.round(source_dm[pair], 4))) + '  ' + data_file_name

            obs_names.append(obs_name)
            print(obs_name)

            # self.t5_text_field.appendPlainText(code_date[pair] + '_' + beam[pair] + '  ' + str(source_dm[pair]) + '   ' + file_paths[pair][0])
            # self.t5_text_field.appendPlainText('Text')
        
        for pair in range(pairs_number):

            print('\n* Processing pair # ' + str(pair + 1) + ' out of ' + str(pairs_number))
            self.t5_label_processing_status.setText('Processing raw data pair #  ' + str(pair + 1) + '  out of  ' + str(pairs_number))
            self.t5_label_processing_status.setStyleSheet("background-color: lightgreen;")

            try:            
                [jds_pair_directory, jds_file_1] = os.path.split(file_paths[pair][0])
                [jds_pair_directory, jds_file_2] = os.path.split(file_paths[pair][1])

                profile_txt_file_path = make_transient_profile_from_jds(jds_pair_directory,
                                                                        [jds_file_1, jds_file_2],
                                                                        temp_big_folder,
                                                                        source_dm[pair])
                # profile_txt_file_path = os.path.normpath('e:/temp/Transient_search_1 10/Transient_DM_21.022_A240311_160000.jds_Data_chA_time_profile.txt')
            
            except:
                print('Error making transient profile #  ' + str(pair + 1) + '  out of  ' + str(pairs_number))
                self.t5_label_processing_status.setText('Error making transient profile #  ' + str(pair + 1) + '  out of  ' + str(pairs_number))
                self.t5_label_processing_status.setStyleSheet("background-color: red;")

            try:
                # Copy result profile and timeline into initial data folder
                [txt_file_path, txt_file_name] = os.path.split(profile_txt_file_path)
                tl_file_name = txt_file_name.split('_Data_')[0] + '_Timeline.txt'
                shutil.copy(profile_txt_file_path, os.path.join(jds_pair_directory, txt_file_name))
                shutil.copy(os.path.join(txt_file_path, tl_file_name), os.path.join(jds_pair_directory, tl_file_name))
                
                # Make new directory in the big temp folder and copy profile there
                new_obs_folder = os.path.join(temp_big_folder, obs_names[pair].replace(' ', '_'))
                os.mkdir(new_obs_folder) 
                
                shutil.copy(profile_txt_file_path, os.path.join(new_obs_folder, txt_file_name))
                shutil.copy(os.path.join(txt_file_path, tl_file_name), os.path.join(new_obs_folder, tl_file_name))

                # Delete the temporary data folder
                shutil.rmtree(txt_file_path)
            except:
                print('Error copying profile #  ' + str(pair + 1) + '  out of  ' + str(pairs_number))
                self.t5_label_processing_status.setText('Error copying profile #  ' + str(pair + 1) + '  out of  ' + str(pairs_number))
                self.t5_label_processing_status.setStyleSheet("background-color: red;")

            try:
                print('Processing spectra of pair #  ' + str(pair + 1) + '  out of  ' + str(pairs_number))
                self.t5_label_processing_status.setText('Processing spectra of pair #  ' + str(pair + 1) + '  out of  ' + str(pairs_number))
                self.t5_label_processing_status.setStyleSheet("background-color: lightgreen;")
                
                # Reading profile data from txt file
                profile_filepath = os.path.join(new_obs_folder, txt_file_name)
                pulsar_data_in_time = read_one_value_txt_file(profile_filepath)

                # Calculating the spectrum
                frequency_axis, pulses_spectra, spectrum_max = \
                    calculate_spectrum_of_profile(pulsar_data_in_time, self.time_resolution)
                
                fig, [ax0, ax1] = plt.subplots(2, 1, figsize=(16.0, 7.0))
                ax0.plot(pulsar_data_in_time)
                ax0.set_xlim([0, len(pulsar_data_in_time)])
                # ax0.set_ylim([-5.0, 5.0])
                ax0.set_title('Time series', fontsize=10, fontweight='bold')
                ax1.plot(frequency_axis, pulses_spectra)
                ax1.axis([0, self.frequency_limit, 0, 1.1 * spectrum_max])
                ax1.set_xlabel('Frequency, Hz', fontsize=10, fontweight='bold')
                fig.subplots_adjust(hspace=0.25, top=0.945)
                ax1.set_title('Spectrum', fontsize=10, fontweight='bold')
                pylab.savefig(os.path.join(new_obs_folder, txt_file_name[0:-4] + ' profile and spectrum before filtering.png'), 
                              bbox_inches='tight', dpi=300)
                plt.close('all')


                # Subtract median and normalize data
                median = median_filter(pulsar_data_in_time, int(self.t5_filter_win_input.value()))
                pulsar_data_in_time = pulsar_data_in_time - median
                pulsar_data_in_time = pulsar_data_in_time / np.std(pulsar_data_in_time)

                # Getting current values from spinboxes
                min_limit = self.t5_low_limit_input.value()
                max_limit = self.t5_high_limit_input.value()

                # Clip data
                cropped_data_in_time = np.clip(pulsar_data_in_time, min_limit, max_limit)

                # Calculating the spectrum
                frequency_axis, pulses_spectra, spectrum_max = \
                    calculate_spectrum_of_profile(cropped_data_in_time, self.time_resolution)
                
                fig, [ax0, ax1] = plt.subplots(2, 1, figsize=(16.0, 7.0))
                ax0.plot(cropped_data_in_time)
                ax0.set_xlim([0, len(cropped_data_in_time)])
                # ax0.set_ylim([-5.0, 5.0])
                ax0.set_title('Time series', fontsize=10, fontweight='bold')
                ax1.plot(frequency_axis, pulses_spectra)
                ax1.axis([0, self.frequency_limit, 0, 1.1 * spectrum_max])
                ax1.set_xlabel('Frequency, Hz', fontsize=10, fontweight='bold')
                fig.subplots_adjust(hspace=0.25, top=0.945)
                ax1.set_title('Spectrum', fontsize=10, fontweight='bold')
                pylab.savefig(os.path.join(new_obs_folder, txt_file_name[0:-4] + ' profile and spectrum after filtering.png'), 
                              bbox_inches='tight', dpi=300)
                plt.close('all')

                harmonics_highlight = None
                # Run function to make and save bit plot
                time_profile_spectra_for_gui_16(cropped_data_in_time, self.time_resolution, harmonics_highlight,
                                                self.frequency_limit, new_obs_folder, txt_file_name,
                                                software_version, 300)
										
                # Run function to make and save bit plot
                time_profile_spectra_for_gui_1_8(cropped_data_in_time, self.time_resolution, harmonics_highlight,
                                                 self.frequency_limit, new_obs_folder, txt_file_name,
                                                 software_version, 300)
                
                # Copy the plots to source folder as well
                shutil.copy(os.path.join(new_obs_folder, txt_file_name[0:-4] + ' profile and spectrum before filtering.png'), 
                            os.path.join(jds_pair_directory, txt_file_name[0:-4] + ' profile and spectrum before filtering.png'))
                shutil.copy(os.path.join(new_obs_folder, txt_file_name[0:-4] + ' profile and spectrum after filtering.png'), 
                            os.path.join(jds_pair_directory, txt_file_name[0:-4] + ' profile and spectrum after filtering.png'))
                shutil.copy(os.path.join(new_obs_folder, txt_file_name[0:-4] + ' big picture up to 8 parts.png'), 
                            os.path.join(jds_pair_directory, txt_file_name[0:-4] + ' big picture up to 8 parts.png'))
                shutil.copy(os.path.join(new_obs_folder, txt_file_name[0:-4] + ' big picture 16 parts.png'), 
                            os.path.join(jds_pair_directory, txt_file_name[0:-4] + ' big picture 16 parts.png'))


            except:
                print('Error processing profile #  ' + str(pair + 1) + '  out of  ' + str(pairs_number))
                self.t5_label_processing_status.setText('Error processing profile #  ' + str(pair + 1) + '  out of  ' + str(pairs_number))
                self.t5_label_processing_status.setStyleSheet("background-color: red;")



        self.t5_label_processing_status.setText('Program finished work, check the data.')
        self.t5_label_processing_status.setStyleSheet("background-color: lightblue;")

        return

    def specify_db_data_folder_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            # self.path_to_result_folder = dir_name
            self.data_path_replace_line.setText(str(dir_name))


    def specify_big_temp_data_path_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            # self.path_to_result_folder = dir_name
            self.big_temp_data_path_line.setText(str(dir_name))


    def one_xls_file_open_dialog(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "Excel Files (*.xls, *.xlsx)")
        if check:
            self.xlsx_file_path_line.setText(file)


# Driver code
if __name__ == '__main__':
    app = QApplication(sys.argv)  # creating apyqt5 application
    main = Window()  # creating a window object
    main.show()  # showing the window

    sys.exit(app.exec_())  # loop
