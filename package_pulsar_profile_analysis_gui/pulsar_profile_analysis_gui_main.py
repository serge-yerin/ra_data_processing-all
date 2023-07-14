from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLabel
from PyQt5.QtWidgets import QTabWidget, QPushButton, QDoubleSpinBox, QAbstractSpinBox, QRadioButton, QLineEdit
from PyQt5.QtWidgets import QFileDialog, QPlainTextEdit
from PyQt5.QtCore import QSize, Qt, QObject, QThread, pyqtSignal
from PyQt5 import QtCore  # , QtGui

from os import path
import matplotlib.pyplot as plt
from matplotlib import rc
import pylab
import numpy as np
import sys
import time

from package_pulsar_profile_analysis_gui.f_calculate_spectrum_of_profile import calculate_spectrum_of_profile
from package_pulsar_profile_analysis_gui.f_make_transient_profile_from_jds import make_transient_profile_from_jds
from package_common_modules.text_manipulations import read_one_value_txt_file
from package_ra_data_processing.filtering import median_filter
from package_common_modules.text_manipulations import separate_filename_and_path

# To change system path to the directory where script is running:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# Keep in mind that for Linux (Ubuntu 22.04) you may will need to ise headless opncv:
# pip uninstall opencv-python
# pip install opencv-python-headless

# https://realpython.com/python-pyqt-qthread/
# # Step 1: Create a worker class
# class Worker(QObject):
#     finished = pyqtSignal()
#     progress = pyqtSignal(int)
#
#     def run(self):
#         """Long-running task."""
#         # for i in range(5):
#         #     sleep(1)
#         #     self.progress.emit(i + 1)
#         # self.finished.emit()
#         profile_txt_file_path = make_transient_profile_from_jds(self.jds_analysis_directory,
#                                                                 self.jds_analysis_list,
#                                                                 self.path_to_result_folder,
#                                                                 self.source_dm)
#         self.txt_file_path_line.setText(profile_txt_file_path)


# Main window
class Window(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window geometry and hierarchy
        self.setWindowTitle('Pulsar profiles analysis')  # Window title
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

        # Add tabs
        self.tabs.addTab(self.tab1, "Process DSP data")
        self.tabs.addTab(self.tab2, "Analyze profile")
        self.tabs.addTab(self.tab3, "Analyze parts 1-8")
        self.tabs.addTab(self.tab4, "Analyze parts 16")

        ##############################
        #         First tab          #
        ##############################

        # First tab
        self.tab1.layout = QGridLayout(self)  # QVBoxLayout

        # First tab raw one
        self.radiobutton_txt = QRadioButton("Ready profile .txt file: ")
        self.radiobutton_txt.setChecked(True)
        self.radiobutton_txt.process_type = "txt file only"
        self.radiobutton_txt.toggled.connect(self.rb_txt_on_click)
        self.tab1.layout.addWidget(self.radiobutton_txt, 0, 0)

        # Path to txt file line
        self.txt_file_path_line = QLineEdit()  # self, placeholderText='Enter a keyword to search...'
        # self.txt_file_path_line.setFixedSize(QSize(400, 30))

        common_path = '../../../RA_DATA_ARCHIVE/ADDITIONAL_pulses_profiles/'
        filename = 'B0329+54_DM_26.78_C240122_152201.jds_Data_chA_time_profile.txt'
        # filename = 'B0809+74_DM_5.755_P130422_121607.jds_Data_chA_time_profile.txt'
        # filename = 'B0950+08_DM_2.972_C250122_214003.jds_Data_chA_time_profile.txt'
        # filename = 'B1919+21_DM_12.4449_C040420_020109.jds_Data_chA_time_profile.txt'

        self.txt_file_path_line.setText(common_path + filename)
        self.tab1.layout.addWidget(self.txt_file_path_line, 0, 1)

        # Button "Open txt file"
        self.button_open_txt = QPushButton('Open txt file')
        self.button_open_txt.clicked.connect(self.one_txt_file_dialog)  # adding action to the button
        self.button_open_txt.setFixedSize(QSize(150, 30))
        self.tab1.layout.addWidget(self.button_open_txt, 0, 2)

        self.label_txt_file_selected = QLabel('After selecting correct txt file, you can switch to ' +
                                              'the second tab "Analyze profile" and begin analysis', self)
        self.tab1.layout.addWidget(self.label_txt_file_selected, 1, 1)

        # Added empty label to separate workflows
        self.label_txt_file_selected = QLabel(' ', self)
        self.tab1.layout.addWidget(self.label_txt_file_selected, 2, 1)

        # First tab second part
        self.radiobutton_jds = QRadioButton("Raw .jds files preprocess:")
        self.radiobutton_jds.process_type = "raw jds files"
        self.radiobutton_jds.toggled.connect(self.rb_jds_on_click)
        self.tab1.layout.addWidget(self.radiobutton_jds, 3, 0, Qt.AlignTop)

        self.jds_file_path_line = QPlainTextEdit()  # self, placeholderText='Enter a keyword to search...'
        # self.jds_file_path_line.setReadOnly(read only)
        self.tab1.layout.addWidget(self.jds_file_path_line, 3, 1)

        # Button "Open jds file"
        self.button_open_jds = QPushButton('Open jds files to preprocess')
        self.button_open_jds.clicked.connect(self.jds_files_open_dialog)  # adding action to the button
        self.button_open_jds.setFixedSize(QSize(150, 30))
        self.button_open_jds.setEnabled(False)
        self.tab1.layout.addWidget(self.button_open_jds, 3, 2, Qt.AlignTop)

        # Path to result folder line
        self.result_path_line = QLineEdit()
        self.tab1.layout.addWidget(self.result_path_line, 4, 1)

        # Button "Specify result folder"
        self.button_select_result_path = QPushButton('Specify result folder')
        self.button_select_result_path.clicked.connect(self.specify_result_folder_dialog)  # adding action to the button
        self.button_select_result_path.setFixedSize(QSize(150, 30))
        self.button_select_result_path.setEnabled(False)
        self.tab1.layout.addWidget(self.button_select_result_path, 4, 2)

        # Nested horizontal layout for DM entry
        self.dm_entry_layout = QHBoxLayout()

        self.label_dm_entry = QLabel("Source dispersion measure (DM):", self)
        self.label_dm_entry.setFixedSize(QSize(160, 30))
        self.dm_entry_layout.addWidget(self.label_dm_entry)

        # Path to txt file line
        self.line_dm_entry = QLineEdit()  # self, placeholderText='Enter a keyword to search...'
        # self.line_dm_entry.setFixedSize(QSize(400, 30))
        self.line_dm_entry.setText('5.755')
        self.dm_entry_layout.addWidget(self.line_dm_entry)

        self.label_dm_units = QLabel("pc * cm^-3", self)
        self.label_dm_units.setFixedSize(QSize(490, 30))
        self.dm_entry_layout.addWidget(self.label_dm_units)

        # Add nested horizontal layout to the main one
        self.tab1.layout.addLayout(self.dm_entry_layout, 5, 1)

        # Button "Preprocess jds files"
        self.button_process_jds = QPushButton('Preprocess jds files')
        self.button_process_jds.clicked.connect(self.preprocess_jds_files)  # adding action to the button
        self.button_process_jds.setEnabled(False)
        self.tab1.layout.addWidget(self.button_process_jds, 6, 1, Qt.AlignTop)

        # JDS processing status label
        self.label_processing_status = QLabel('', self)
        self.tab1.layout.addWidget(self.label_processing_status, 7, 1)

        # Adding stretch lines to get all elements magnetted to top
        self.tab1.layout.setRowStretch(self.tab1.layout.rowCount(), 1)
        # self.tab1.layout.setColumnStretch(self.tab1.layout.columnCount(), 1)

        self.tab1.setLayout(self.tab1.layout)

        ##############################
        #         Second tab         #
        ##############################

        # Layouts in the second tab
        self.tab2.layout = QVBoxLayout(self)
        self.input_controls_layout = QHBoxLayout()

        # Creating labels near spinboxes to describe the input
        self.label_median_win = QLabel("Median window:", self)
        self.label_median_win.setFixedSize(QSize(100, 30))
        self.label_median_win.setAlignment(QtCore.Qt.AlignCenter)

        self.label_low_limit_input = QLabel("Lower limit", self)
        self.label_low_limit_input.setFixedSize(QSize(100, 30))
        self.label_low_limit_input.setWordWrap(True)  # making label multi line
        self.label_low_limit_input.setAlignment(QtCore.Qt.AlignCenter)

        self.label_high_limit_input = QLabel("Higher limit", self)
        self.label_high_limit_input.setFixedSize(QSize(100, 30))
        self.label_high_limit_input.setWordWrap(True)  # making label multi line
        self.label_high_limit_input.setAlignment(QtCore.Qt.AlignCenter)

        # Selection of limits with spinboxes

        self.filter_win_input = QDoubleSpinBox()
        self.filter_win_input.setFixedSize(QSize(100, 30))
        self.filter_win_input.setMinimum(0)
        self.filter_win_input.setMaximum(100000)
        self.filter_win_input.setValue(100)

        step_type = QAbstractSpinBox.AdaptiveDecimalStepType  # step type

        self.low_limit_input = QDoubleSpinBox()
        self.low_limit_input.setStepType(step_type)
        self.low_limit_input.setMinimum(-10.0)
        self.low_limit_input.setFixedSize(QSize(100, 30))
        self.low_limit_input.setValue(-3)

        self.high_limit_input = QDoubleSpinBox()
        self.high_limit_input.setStepType(step_type)
        self.high_limit_input.setMinimum(-10.0)
        self.high_limit_input.setFixedSize(QSize(100, 30))
        self.high_limit_input.setValue(3)

        # Main plot window
        self.figure = plt.figure()  # a figure instance to plot on
        self.canvas = FigureCanvas(self.figure)  # takes the 'figure' instance as a parameter to __init__

        # This is the Matplotlib Navigation widget it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Button "Read data"
        self.button_read = QPushButton('Read data')
        self.button_read.clicked.connect(self.read_initial_data)  # adding action to the button
        self.button_read.setFixedSize(QSize(100, 30))

        # Button "Subtract median"
        self.button_filter = QPushButton('Subtract median')
        self.button_filter.clicked.connect(self.subtract_median)  # adding action to the button
        self.button_filter.setFixedSize(QSize(140, 30))

        # Button "Crop data"
        self.button_crop = QPushButton('Crop data')
        self.button_crop.clicked.connect(self.crop_and_show_spectrum)  # adding action to the button
        self.button_crop.setFixedSize(QSize(140, 30))

        # Packing layouts in the window
        self.input_controls_layout.addWidget(self.button_read)
        self.input_controls_layout.addWidget(self.label_median_win)
        self.input_controls_layout.addWidget(self.filter_win_input)
        self.input_controls_layout.addWidget(self.button_filter)
        self.input_controls_layout.addWidget(self.label_low_limit_input)
        self.input_controls_layout.addWidget(self.low_limit_input)
        self.input_controls_layout.addWidget(self.label_high_limit_input)
        self.input_controls_layout.addWidget(self.high_limit_input)
        self.input_controls_layout.addWidget(self.button_crop)

        self.tab2.layout.addLayout(self.input_controls_layout)
        self.tab2.layout.addWidget(self.toolbar)
        self.tab2.layout.addWidget(self.canvas)

        self.tab2.setLayout(self.tab2.layout)

        ##############################
        #         Third tab         #
        ##############################

        # Third tab
        self.tab3.layout = QVBoxLayout(self)

        # Button "Read data"
        self.button_plot_1_8 = QPushButton('Plot parts of data from 1 to 8')
        self.button_plot_1_8.clicked.connect(self.plot_spectra_1_8)  # adding action to the button
        self.button_plot_1_8.setFixedSize(QSize(250, 30))
        self.tab3.layout.addWidget(self.button_plot_1_8)

        # Main plot window
        self.figure_1_8 = plt.figure()  # a figure instance to plot on
        self.canvas_1_8 = FigureCanvas(self.figure_1_8)  # takes the 'figure' instance as a parameter to __init__
        self.tab3.layout.addWidget(self.canvas_1_8)

        self.tab3.setLayout(self.tab3.layout)

        ##############################
        #         Fourth tab         #
        ##############################

        # Third tab
        self.tab4.layout = QVBoxLayout(self)

        self.tab4.setLayout(self.tab4.layout)

        ##############################
        #         Pack tabs          #
        ##############################

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def plot_spectra_1_8(self):

        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%d.%m.%Y")

        pulsar_data_in_time = self.cropped_data_in_time
        # Calculating the spectrum
        frequency_axis, profile_spectrum, spectrum_max = \
            calculate_spectrum_of_profile(pulsar_data_in_time, time_resolution)

        # Update the plot
        self.figure_1_8.clear()  # clearing old figure
        rc('font', size=6, weight='bold')

        # Adding the plot # 1 of 16
        ax1 = self.figure_1_8.add_subplot(4, 4, 1)
        ax1.plot(frequency_axis, profile_spectrum, color=u'#1f77b4', linestyle='-', alpha=1.0,
                 linewidth='0.60', label='Time series spectrum')
        ax1.axis([0, frequency_limit, 0, 1.1 * spectrum_max])
        ax1.legend(loc='upper right', fontsize=5)
        ax1.set_ylabel('Amplitude, AU', fontsize=6, fontweight='bold')
        ax1.set_title('Full data length', fontsize=5, fontweight='bold')

        # Analyze only parts of the time profile (Creating indexes for plots positioning on the big result figure)
        v_ind = [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
        h_ind = [1, 2, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
        fig_num = [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        index = 0

        full_data_length = len(pulsar_data_in_time)

        for step in range(3):
            parts_num = 2 ** (step + 1)

            for part in range(parts_num):
                start = int((full_data_length / parts_num) * part)
                stop = int((full_data_length / parts_num) * (part + 1))
                add_text = ' Part ' + str(part + 1) + ' of ' + str(parts_num)
                new_profile_data = pulsar_data_in_time[start:stop]

                # Calculating the spectrum
                frequency_axis, profile_spectrum, spectrum_max = \
                    calculate_spectrum_of_profile(new_profile_data, time_resolution)

                ax = self.figure_1_8.add_subplot(4, 4, fig_num[index])
                ax.plot(frequency_axis, profile_spectrum, color=u'#1f77b4', linestyle='-', alpha=1.0,
                        linewidth='0.60', label='Time series spectrum')
                ax.axis([0, frequency_limit, 0, 1.1 * spectrum_max])
                ax.legend(loc='upper right', fontsize=5)
                if v_ind[index] == 3:
                    ax.set_xlabel('Frequency, Hz', fontsize=7, fontweight='bold')
                if h_ind[index] == 0:
                    ax.set_ylabel('Amplitude, AU', fontsize=7, fontweight='bold')
                ax.set_title(add_text, fontsize=7, fontweight='bold')
                index += 1
            # Adding empty place on 4,4 position
            ax = self.figure_1_8.add_subplot(4, 4, 4)
            ax.axis('off')

            # Finishing and saving the big results figure with 15 plots
            self.figure_1_8.subplots_adjust(hspace=0.25, top=0.930)
            self.figure_1_8.suptitle('Time profile in frequency domain from file: ',
                                     fontsize=10, fontweight='bold')
            self.figure_1_8.text(0.82, 0.06, 'Processed ' + current_date + ' at ' + current_time,
                                 fontsize=5, transform=plt.gcf().transFigure)
            software_version = '1'
            self.figure_1_8.text(0.11, 0.06, 'Software version: ' + software_version +
                                 ', yerin.serge@gmail.com, IRA NASU', fontsize=5, transform=plt.gcf().transFigure)
            # pylab.savefig(common_path + new_folder_name + '/' + filename[0:-4] + ' big picture up to 8 parts.png',
            #               bbox_inches='tight', dpi=custom_dpi)
            # plt.close('all')

        self.canvas_1_8.draw()  # refresh canvas

    def preprocess_jds_files(self):
        try:
            self.source_dm = float(self.line_dm_entry.text().replace(',', '.'))
        except ValueError:
            print(' Wrong source DM value! Unable to convert into float number.')

        self.label_processing_status.setText("Processing")
        # self.label_processing_status.setFont(QtGui.QFont(self, 20))  # "Sanserif"
        # self.label_processing_status.setStyleSheet('color:red')

        # # Step 2: Create a QThread object
        # self.thread = QThread()
        # # Step 3: Create a worker object
        # self.worker = Worker()
        # # Step 4: Move worker to the thread
        # self.worker.moveToThread(self.thread)
        # # Step 5: Connect signals and slots
        # self.thread.started.connect(self.worker.run)
        # self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.reportProgress)
        # # Step 6: Start the thread
        # self.thread.start()

        profile_txt_file_path = make_transient_profile_from_jds(self.jds_analysis_directory,
                                                                self.jds_analysis_list,
                                                                self.path_to_result_folder,
                                                                self.source_dm)
        self.txt_file_path_line.setText(profile_txt_file_path)
        self.label_processing_status.setText("Processing finished")

    def specify_result_folder_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            self.path_to_result_folder = dir_name     # Path(dir_name)
            self.result_path_line.setText(str(dir_name))
        pass

    def jds_files_open_dialog(self):
        files, check = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()",
                                                    "", "JDS files (*.jds)")
        file_names = []
        self.jds_file_path_line.clear()  # Cleat the text input to add new file paths
        if check:
            for i in range(len(files)):
                self.jds_file_path_line.appendPlainText(files[i])
                directory, file_name = separate_filename_and_path(files[i])
                file_names.append(file_name)
            self.jds_analysis_directory = directory
            self.jds_analysis_list = file_names

    def one_txt_file_dialog(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "Text Files (*.txt)")
        if check:
            self.txt_file_path_line.setText(file)

    # action called by radio button switch txt
    def rb_txt_on_click(self):
        self.radioButton = self.sender()
        if self.radioButton.isChecked():
            # print("Process is %s" % (self.radioButton.process_type))
            self.button_open_txt.setEnabled(True)
            self.button_open_jds.setEnabled(False)
            self.button_select_result_path.setEnabled(False)
            self.button_process_jds.setEnabled(False)

    # action called by radio button switch jds
    def rb_jds_on_click(self):
        self.radioButton = self.sender()
        if self.radioButton.isChecked():
            # print("Process is %s" % (self.radioButton.process_type))
            self.button_open_txt.setEnabled(False)
            self.button_open_jds.setEnabled(True)
            self.button_select_result_path.setEnabled(True)
            self.button_process_jds.setEnabled(True)

    # action called by the push button
    def read_initial_data(self):

        # Reading profile data from txt file
        data_filepath = self.txt_file_path_line.text()
        pulsar_data_in_time = read_one_value_txt_file(data_filepath)
        self.p_data_in_time = pulsar_data_in_time

        # Calculating the spectrum
        frequency_axis, pulses_spectra, spectrum_max = \
            calculate_spectrum_of_profile(pulsar_data_in_time, time_resolution)

        # Update the plot
        self.figure.clear()  # clearing old figure
        ax0 = self.figure.add_subplot(211)
        ax0.plot(pulsar_data_in_time)
        ax0.set_xlim([0, len(pulsar_data_in_time)])
        ax0.set_ylim([-0.2, 0.2])
        ax0.set_title('Time series', fontsize=10, fontweight='bold')
        ax1 = self.figure.add_subplot(212)
        # Adding the plots for parts of data to the big result picture
        ax1.plot(frequency_axis, pulses_spectra)
        ax1.axis([0, frequency_limit, 0, 1.1 * spectrum_max])
        ax1.set_xlabel('Frequency, Hz', fontsize=10, fontweight='bold')
        self.figure.subplots_adjust(hspace=0.25, top=0.945)
        ax1.set_title('Spectrum', fontsize=10, fontweight='bold')
        self.canvas.draw()  # refresh canvas

    # action called by the push button
    def subtract_median(self):

        # Subtract median and normalize data
        median = median_filter(self.p_data_in_time, int(self.filter_win_input.value()))
        pulsar_data_in_time = self.p_data_in_time - median
        pulsar_data_in_time = pulsar_data_in_time / np.std(pulsar_data_in_time)
        self.prepared_data_in_time = pulsar_data_in_time

        # Calculating the spectrum
        frequency_axis, pulses_spectra, spectrum_max = \
            calculate_spectrum_of_profile(pulsar_data_in_time, time_resolution)  #pulsar_data_in_time

        # Update the plot
        self.figure.clear()  # clearing old figure
        ax0 = self.figure.add_subplot(211)
        ax0.plot(pulsar_data_in_time)
        ax0.set_xlim([0, len(pulsar_data_in_time)])
        ax0.set_ylim([-5.0, 5.0])
        ax0.set_title('Time series', fontsize=10, fontweight='bold')
        ax1 = self.figure.add_subplot(212)
        ax1.plot(frequency_axis, pulses_spectra)
        ax1.axis([0, frequency_limit, 0, 1.1 * spectrum_max])
        ax1.set_xlabel('Frequency, Hz', fontsize=10, fontweight='bold')
        self.figure.subplots_adjust(hspace=0.25, top=0.945)
        ax1.set_title('Spectrum', fontsize=10, fontweight='bold')
        self.canvas.draw()  # refresh canvas

    def crop_and_show_spectrum(self):

        # Getting current values from spinboxes
        min_limit = self.low_limit_input.value()
        max_limit = self.high_limit_input.value()

        # Clip data
        self.cropped_data_in_time = np.clip(self.prepared_data_in_time, min_limit, max_limit)

        # Calculating the spectrum
        frequency_axis, pulses_spectra, spectrum_max = \
            calculate_spectrum_of_profile(self.cropped_data_in_time, time_resolution)

        def mouse_event(event):
            x = event.xdata
            self.harmonics_highlight = [0.5*x, x, 2*x, 3*x, 4*x, 5*x, 6*x, 7*x, 8*x, 9*x, 10*x, 11*x,
                                        12*x, 13*x, 14*x, 15*x, 16*x, 17*x, 18*x]

            self.figure.clear()  # clearing old figure
            ax0 = self.figure.add_subplot(211)
            ax0.plot(self.cropped_data_in_time)
            ax0.set_xlim([0, len(self.cropped_data_in_time)])
            ax0.set_ylim([-5.0, 5.0])
            ax0.set_title('Time series', fontsize=10, fontweight='bold')
            ax1 = self.figure.add_subplot(212)
            plt.text(x, spectrum_max, ' $f$ = ' + str(np.round(x, 3)) + ' $Hz$ $or$ $P$ = ' +
                     str(np.round(1/x, 3)) + ' $s$', fontsize=14, color='C3')
            for harmonic in self.harmonics_highlight:
                ax1.axvline(x=harmonic, color='C1', linestyle='-', linewidth=2.0, alpha=0.2)
            ax1.plot(frequency_axis, pulses_spectra)
            ax1.axis([0, frequency_limit, 0, 1.1 * spectrum_max])
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
        ax1.axis([0, frequency_limit, 0, 1.1 * spectrum_max])
        ax1.set_xlabel('Frequency, Hz', fontsize=10, fontweight='bold')
        self.figure.subplots_adjust(hspace=0.25, top=0.945)
        ax1.set_title('Spectrum', fontsize=10, fontweight='bold')
        self.canvas.draw()  # refresh canvas


# Driver code
if __name__ == '__main__':
    app = QApplication(sys.argv)  # creating apyqt5 application
    main = Window()  # creating a window object
    main.show()  # showing the window

    frequency_limit = 10
    time_resolution = (1 / 66000000) * 16384 * 32  # Data time resolution, s   # 0.007944

    sys.exit(app.exec_())  # loop
