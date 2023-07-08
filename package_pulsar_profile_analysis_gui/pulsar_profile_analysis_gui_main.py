import os
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QDoubleSpinBox
from PyQt5.QtWidgets import QAbstractSpinBox, QLabel
from PyQt5.QtCore import QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma

from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_common_modules.text_manipulations import read_one_value_txt_file
from package_ra_data_processing.filtering import median_filter


def read_and_prepare_data(common_path, filename):
    data_filename = common_path + filename

    new_folder_name = filename[:-4] + "_analysis"
    if not os.path.exists(common_path + new_folder_name):
        os.makedirs(common_path + new_folder_name)

    # Reading profile data from txt file
    profile_data = read_one_value_txt_file(data_filename)
    print('\n  Number of samples in text file:  ', len(profile_data))

    median = median_filter(profile_data, 100)
    profile_data = profile_data - median

    # Getting pulsar parameters from catalogue
    pulsar_ra, pulsar_dec, source_dm, pulsar_period = catalogue_pulsar(pulsar_name)

    # Data frequency resolution, Hz
    frequency_resolution = 1 / (time_resolution * len(profile_data))

    # Calculate pulsar harmonics frequency
    pulsar_frequency = 1 / pulsar_period  # frequency of pulses, Hz

    frequency_limit = (harmonics_to_show + 1.5) * pulsar_frequency

    freq_points_per_harmonic = np.ceil(pulsar_frequency / frequency_resolution).astype(int)
    # n_harmonics = int(np.floor(len(profile_data) / (2 * freq_points_per_harmonic)))
    n_harmonics = harmonics_to_show + 1

    pulsar_harmonics = pulsar_frequency * np.linspace(1, n_harmonics, num=n_harmonics)
    pulsar_harmonics_points = np.ceil(pulsar_harmonics / frequency_resolution).astype(int)
    max_interval = int(freq_points_per_harmonic / 4)

    print('  Pulsar frequency: ', pulsar_frequency, ' Hz')
    print('  Frequency resolution: ', frequency_resolution, ' s')
    print('  Time resolution: ', time_resolution, ' s')
    print('  Number of points per harmonic: ', freq_points_per_harmonic)
    print('  Number harmonics to highlight: ', n_harmonics)
    print('  Interval to search the harmonic: ', max_interval, ' points')

    # Calculating the spectrum
    profile_spectrum = np.power(np.real(np.fft.fft(profile_data[:])), 2)  # calculation of the spectrum
    profile_spectrum = profile_spectrum[0:int(len(profile_spectrum) / 2)]  # delete second part of the spectrum

    frequency_axis = [frequency_resolution * i for i in range(len(profile_spectrum))]

    # Finding the maximal spectrum amplitudes near expected harmonics
    max_harmonics = []
    noise_mean = []
    noise_std = []
    signal_to_noise = []
    for i in range(n_harmonics):
        # Maximal points near expected harmonics
        data_bunch_near_harmonic = profile_spectrum[pulsar_harmonics_points[i] - max_interval:
                                                    pulsar_harmonics_points[i] + max_interval].copy()

        max_near_harmonic = np.max(data_bunch_near_harmonic)
        max_harmonics.append(max_near_harmonic)

        # Masking the maximal value
        data_bunch_near_harmonic_masked = ma.masked_values(data_bunch_near_harmonic, max_near_harmonic, copy=True)

        # Calculating mean and std of noise around harmonic but without it
        current_noise_mean = np.mean(data_bunch_near_harmonic_masked)
        current_noise_std = np.std(data_bunch_near_harmonic_masked)

        noise_mean.append(current_noise_mean)
        noise_std.append(3 * current_noise_std)
        signal_to_noise.append(max_near_harmonic / (current_noise_mean + 3 * current_noise_std))

    # Calculating the limit o vertical axis of the spectrum plot
    spectrum_max = np.max(max_harmonics)

    return profile_data,  frequency_axis, profile_spectrum, spectrum_max, frequency_limit


# main window which inherits QDialog
class Window(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setGeometry(100, 100, 800, 600)
        # menu_bar = self.menuBar()
        # file_menu = menu_bar.addMenu('&File')

        self.setWindowTitle('Pulsar profiles analysis')  # Window title

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
        self.low_limit_input.setMinimum(-3.0)
        self.low_limit_input.setFixedSize(QSize(100, 30))

        self.high_limit_input = QDoubleSpinBox()
        self.high_limit_input.setStepType(step_type)
        self.high_limit_input.setMinimum(-3.0)
        self.high_limit_input.setFixedSize(QSize(100, 30))

        self.figure = plt.figure()  # a figure instance to plot on

        # this is the Canvas Widget that displays the 'figure' it takes the 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to 'plot' method
        self.button = QPushButton('Read data')
        self.button.clicked.connect(self.read_initial_data)  # adding action to the button
        self.button.setFixedSize(QSize(100, 30))

        # Packing layouts in the window
        input_controls_layout.addWidget(self.button)
        input_controls_layout.addWidget(self.label_low_limit_input)
        input_controls_layout.addWidget(self.low_limit_input)
        input_controls_layout.addWidget(self.label_high_limit_input)
        input_controls_layout.addWidget(self.high_limit_input)

        page_layout.addLayout(input_controls_layout)
        page_layout.addWidget(self.toolbar)
        page_layout.addWidget(self.canvas)

        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)  # Set the central widget of the Window.

    # action called by the push button
    def read_initial_data(self):
        # random data
        data_0, x_line_1, data_1, spectrum_max, frequency_limit = read_and_prepare_data(common_path, filename)

        self.figure.clear()  # clearing old figure
        ax0 = self.figure.add_subplot(211)
        ax0.plot(data_0)
        ax0.set_xlim([0, len(data_0)])
        ax0.set_ylim([-0.2, 0.2])
        ax0.set_title('Time series')
        ax1 = self.figure.add_subplot(212)
        # Adding the plots for parts of data to the big result picture
        ax1.plot(x_line_1, data_1)
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
    pulsar_name = 'B0329+54'
    harmonics_to_show = 15  # Figure upper frequency (x-axis) limit in number of pulse harmonics to show
    time_resolution = (1 / 66000000) * 16384 * 32  # Data time resolution, s   # 0.007944

    sys.exit(app.exec_())  # loop
