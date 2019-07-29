import os

'''
'''

def find_files_in_folder(path, extension):
    '''
    Searching of files in the specified directory with specified file extension
    '''
    file_path_list = []
    file_name_list = []
    i = 0
    print ('  Directory: ', path, '\n')
    print ('  List of files found: ')
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                i = i + 1
                print ('         ', i, ') ', file)
                file_name_list.append(str(file))
                file_path_list.append(str(os.path.join(root, file)))
    return file_path_list, file_name_list


if __name__ == '__main__':

    path = 'DATA/'
    extension = '.adr'

    file_path_list, file_name_list = find_files_in_folder(path, extension)
