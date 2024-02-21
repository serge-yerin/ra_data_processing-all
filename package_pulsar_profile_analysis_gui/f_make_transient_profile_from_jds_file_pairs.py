import os
import sys
from os import path

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_pulsar_profile_analysis_gui.f_make_transient_profile_from_jds import make_transient_profile_from_jds


def f_make_transient_profile_from_jds_file_pairs(source_directory, result_directory, source_dm):

    # Checking if the paths end with slash
    # if source_directory[-1] != '/':
    #     source_directory = source_directory + '/'
    # if result_directory[-1] != '/':
    #     result_directory = result_directory + '/'

    # Normalizing input paths
    source_directory = os.path.normpath(source_directory)
    result_directory = os.path.normpath(result_directory)

    # Finding a list of jds files in the folder (output is sorted by name)
    file_list = find_files_only_in_current_folder(source_directory, '.jds', True)

    # Creating pairs and run the processing pipeline part
    for pair in range(len(file_list) - 1):

        file_name_list_current = [file_list[pair], file_list[pair + 1]]
        print('\n\n Pair of files #', pair + 1)

        make_transient_profile_from_jds(source_directory, file_name_list_current, result_directory, source_dm)

    return


if __name__ == '__main__':
    source_directory = 'E:/RA_DATA_ARCHIVE/DSP_spectra_pulsar_UTR2_B1919+21/'
    result_directory = 'E:/RA_DATA_RESULTS/Results/'
    source_dm = 12.4449

    f_make_transient_profile_from_jds_file_pairs(source_directory, result_directory, source_dm)
