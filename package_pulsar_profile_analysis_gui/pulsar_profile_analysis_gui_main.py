import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QDoubleSpinBox
from PyQt5.QtWidgets import QAbstractSpinBox, QLabel
from PyQt5.QtCore import QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np

from package_pulsar_profile_analysis_gui.f_read_initial_data import calculate_spectrum_of_profile
from package_pulsar_profile_analysis_gui.f_subtract_median_from_data import subtract_median_from_data
from package_common_modules.text_manipulations import read_one_value_txt_file


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

        # Layouts in the main window
        page_layout = QVBoxLayout()
        input_controls_layout = QHBoxLayout()

        # Creating labels for spinboxes
        self.label_low_limit_input = QLabel("Lower limit", self)
        self.label_low_limit_input.setFixedSize(QSize(100, 30))
        self.label_low_limit_input.setWordWrap(True)  # making label multi line

        self.label_high_limit_input = QLabel("Higher limit", self)
        self.label_high_limit_input.setFixedSize(QSize(100, 30))
        self.label_high_limit_input.setWordWrap(True)  # making label multi line

        # Selection of limits with spinboxes
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
        self.canvas = FigureCanvas(self.figure) # takes the 'figure' instance as a parameter to __init__

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
        input_controls_layout.addWidget(self.button_read)
        input_controls_layout.addWidget(self.button_filter)
        input_controls_layout.addWidget(self.label_low_limit_input)
        input_controls_layout.addWidget(self.low_limit_input)
        input_controls_layout.addWidget(self.label_high_limit_input)
        input_controls_layout.addWidget(self.high_limit_input)
        input_controls_layout.addWidget(self.button_crop)

        page_layout.addLayout(input_controls_layout)
        page_layout.addWidget(self.toolbar)
        page_layout.addWidget(self.canvas)

        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)  # Set the central widget of the Window.

    # action called by the push button
    def read_initial_data(self):

        # Reading profile data from txt file
        data_filename = common_path + filename
        pulsar_data_in_time = read_one_value_txt_file(data_filename)
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
        ax0.set_title('Time series')
        ax1 = self.figure.add_subplot(212)
        # Adding the plots for parts of data to the big result picture
        ax1.plot(frequency_axis, pulses_spectra)
        ax1.axis([0, frequency_limit, 0, 1.1 * spectrum_max])
        self.figure.subplots_adjust(hspace=0.25, top=0.945)
        ax1.set_title('Spectrum')
        self.canvas.draw()  # refresh canvas

    # action called by the push button
    def subtract_median(self):

        # Subtract median and normalize data
        pulsar_data_in_time = subtract_median_from_data(self.p_data_in_time)
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
        ax0.set_title('Time series')
        ax1 = self.figure.add_subplot(212)
        ax1.plot(frequency_axis, pulses_spectra)
        ax1.axis([0, frequency_limit, 0, 1.1 * spectrum_max])
        self.figure.subplots_adjust(hspace=0.25, top=0.945)
        ax1.set_title('Spectrum')
        self.canvas.draw()  # refresh canvas

    def crop_and_show_spectrum(self):

        # Getting current values from spinboxes
        min_limit = self.low_limit_input.value()
        max_limit = self.high_limit_input.value()

        # Clip data
        cropped_data_in_time = np.clip(self.prepared_data_in_time, min_limit, max_limit)

        # Calculating the spectrum
        frequency_axis, pulses_spectra, spectrum_max = \
            calculate_spectrum_of_profile(cropped_data_in_time, time_resolution)

        def mouse_event(event):
            x = event.xdata
            self.harmonics_highlight = [0.5*x, x, 2*x, 3*x, 4*x, 5*x, 6*x, 7*x, 8*x, 9*x, 10*x, 11*x,
                                        12*x, 13*x, 14*x, 15*x, 16*x, 17*x, 18*x]

            self.figure.clear()  # clearing old figure
            ax0 = self.figure.add_subplot(211)
            ax0.plot(cropped_data_in_time)
            ax0.set_xlim([0, len(cropped_data_in_time)])
            ax0.set_ylim([-5.0, 5.0])
            ax0.set_title('Time series')
            ax1 = self.figure.add_subplot(212)
            plt.text(x, spectrum_max, ' $f$ = ' + str(np.round(x, 3)) + '  $Hz$  $or$ $P$ = ' +
                     str(np.round(1/x, 3)) + ' $s$', fontsize=14, color='C3')
            for harmonic in self.harmonics_highlight:
                ax1.axvline(x=harmonic, color='C1', linestyle='-', linewidth=2.0, alpha=0.2)
            ax1.plot(frequency_axis, pulses_spectra)
            ax1.axis([0, frequency_limit, 0, 1.1 * spectrum_max])
            self.figure.subplots_adjust(hspace=0.25, top=0.945)
            ax1.set_title('Spectrum')
            self.canvas.draw()  # refresh canvas

        # Update the plot
        cid = self.figure.canvas.mpl_connect('button_press_event', mouse_event)
        self.figure.clear()  # clearing old figure
        ax0 = self.figure.add_subplot(211)
        ax0.plot(cropped_data_in_time)
        ax0.set_xlim([0, len(cropped_data_in_time)])
        ax0.set_ylim([-5.0, 5.0])
        ax0.set_title('Time series')
        ax1 = self.figure.add_subplot(212)
        # Adding the plots for parts of data to the big result picture
        ax1.plot(frequency_axis, pulses_spectra)
        ax1.axis([0, frequency_limit, 0, 1.1 * spectrum_max])
        self.figure.subplots_adjust(hspace=0.25, top=0.945)
        ax1.set_title('Spectrum')
        self.canvas.draw()  # refresh canvas


# Driver code
if __name__ == '__main__':
    app = QApplication(sys.argv)  # creating apyqt5 application
    main = Window()  # creating a window object
    main.show()  # showing the window

    # Parameters
    common_path = '../../../RA_DATA_ARCHIVE/ADDITIONAL_pulses_profiles/'

    filename = 'B0329+54_DM_26.78_C240122_152201.jds_Data_chA_time_profile.txt'
    # filename = 'B0809+74_DM_5.755_P130422_121607.jds_Data_chA_time_profile.txt'
    # filename = 'B0950+08_DM_2.972_C250122_214003.jds_Data_chA_time_profile.txt'
    # filename = 'B1919+21_DM_12.4449_C040420_020109.jds_Data_chA_time_profile.txt'

    frequency_limit = 10
    time_resolution = (1 / 66000000) * 16384 * 32  # Data time resolution, s   # 0.007944

    sys.exit(app.exec_())  # loop
