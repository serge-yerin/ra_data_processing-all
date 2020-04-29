import sys
from package_common_modules.check_if_all_files_of_same_size import check_if_all_files_of_same_size
from package_common_modules.find_files_only_in_current_folder import find_files_only_in_current_folder
from package_ra_data_files_formats.check_if_JDS_files_of_equal_parameters import check_if_JDS_files_of_equal_parameters
from package_ra_data_files_formats.check_if_ADR_files_of_equal_parameters import check_if_ADR_files_of_equal_parameters

'''
'''

def find_and_check_files_in_current_folder(source_directory, extension):
    '''
    Searching of files in the specified directory with specified file extension
    '''
    fileList = find_files_only_in_current_folder(source_directory, extension, 1)
    print('')

    if len(fileList) > 1:  # Check if files have same parameters if there are more then one file in list
        # Check if all files (except the last) have same size
        same_or_not = check_if_all_files_of_same_size(source_directory, fileList, 1)

        # Check if all files in this folder have the same parameters in headers
        if extension == '.jds':
            equal_or_not = check_if_JDS_files_of_equal_parameters(source_directory, fileList)
        if extension == '.adr':
            equal_or_not = check_if_ADR_files_of_equal_parameters(source_directory, fileList)

        if same_or_not and equal_or_not:
            #print('\n\n\n        :-)  All files seem to be of the same parameters!  :-) \n\n\n')
            decision = 1
        else:
            print(
                '\n\n\n ************************************************************************************* \n *                                                                                   *')
            print(' *   Seems files in folders are different check the errors and restart the script!   *')
            print(' *                                                                                   *  '
                  '\n ************************************************************************************* \n\n\n')

            decision = int(input('* Enter "1" to start processing, or "0" to stop the script:     '))
        if decision != 1:
            sys.exit('\n\n\n              ***  Program stopped! *** \n\n\n')

    return fileList



if __name__ == '__main__':

    path = 'DATA/'
    extension = '.jds'
    file_name_list = find_and_check_files_in_current_folder(path, extension)
