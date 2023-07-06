import os
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random

from package_astronomy.catalogue_pulsar import catalogue_pulsar
from package_common_modules.text_manipulations import read_one_value_txt_file


def read_and_prepare_data(common_path, filename):
    data_filename = common_path + filename

    new_folder_name = filename[:-4] + "_analysis"
    if not os.path.exists(common_path + new_folder_name):
        os.makedirs(common_path + new_folder_name)

    # Reading profile data from txt file
    profile_data = read_one_value_txt_file(data_filename)
    print('\n  Number of samples in text file:  ', len(profile_data))

    return profile_data


# main window which inherits QDialog
class Window(QDialog):

    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setWindowTitle('Application')  # Window title
        self.figure = plt.figure()  # a figure instance to plot on

        # this is the Canvas Widget that displays the 'figure' it takes the 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to 'plot' method
        self.button = QPushButton('Plot')

        # adding action to the button
        self.button.clicked.connect(self.plot)

        # Just some button connected to 'Calc' method
        self.button2 = QPushButton('Calc')

        # creating a Vertical Box layout
        layout = QVBoxLayout()

        # adding tool bar to the layout
        layout.addWidget(self.toolbar)

        # adding canvas to the layout
        layout.addWidget(self.canvas)

        # adding push button to the layout
        layout.addWidget(self.button)
        layout.addWidget(self.button2)

        # setting layout to the main window
        self.setLayout(layout)

    # action called by the push button
    def plot(self):
        # random data
        data_0 = read_and_prepare_data(common_path, filename)
        data_1 = [random.random() for i in range(100)]

        self.figure.clear()  # clearing old figure
        ax0 = self.figure.add_subplot(211)
        ax0.plot(data_0, 'o-')
        ax0.set_ylim([-0.2, 0.2])
        ax0.set_title('Title')
        ax1 = self.figure.add_subplot(212)
        ax1.plot(data_1, 'o-')
        ax1.set_ylim([0, 1])
        ax1.set_title('Title')
        self.canvas.draw()  # refresh canvas


# driver code
if __name__ == '__main__':
    app = QApplication(sys.argv)  # creating apyqt5 application
    main = Window()  # creating a window object
    main.show()  # showing the window

    common_path = '../../../RA_DATA_ARCHIVE/ADDITIONAL_pulses_profiles/'
    filename = 'B0329+54_DM_26.78_C240122_152201.jds_Data_chA_time_profile.txt'

    sys.exit(app.exec_())  # loop
