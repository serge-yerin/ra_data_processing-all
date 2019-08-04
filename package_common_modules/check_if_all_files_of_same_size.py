import os
import numpy as np
from package_common_modules.find_unique_strings_in_list import find_unique_strings_in_list

'''
'''

def check_if_all_files_of_same_size(folder_path, file_name_list, one_but_last):
    '''
    Checking if iles are of the same size. It is useful for check if the data files
    in the folder are from one continous observation, or there were stops of recording.
    The check for this purpose a list of all but last file should be analyzed
    one_but_last = 0 - Analyze all files
    one_but_last = 1 - Analyze all but last file
    '''
    if len(file_name_list) > 1:
        filesize = np.zeros(len(file_name_list) - one_but_last)
        filesize_text = [''] * (len(file_name_list) - one_but_last)
        for i in range(len(file_name_list) - one_but_last):
            filepath = folder_path + file_name_list[i]
            filesize[i] = (os.stat(filepath).st_size)
            filesize_text[i] = str(filesize[i])

        unique = find_unique_strings_in_list(filesize_text)


    if len(file_name_list) == 1 or len(unique) == 1:
        equal_or_not = 1
        print('\n OK! All files have the same size')
    else:
        equal_or_not = 0
        print('\n **********************************************************\n !!!      WARNING: Sizes of files in folder differ      !!! \n **********************************************************')
        print('\n   * Check the size of each file in list: \n')
        print('   No       Size in bits       File name \n')
        for file_no in range (len(file_name_list) - one_but_last):
            print('  {:0>4d}'.format(file_no+1), '   {:15.0f}     '.format(filesize[file_no]), file_name_list[file_no])
        print('  * Last file was not taken into account!')

    return equal_or_not


if __name__ == '__main__':

    file_name_list = check_if_all_files_of_same_size(path, file_name_list, one_but_last)
