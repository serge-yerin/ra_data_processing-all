import os

'''
'''

def find_files_only_in_current_folder(path, extension, print_or_not):
    '''
    Searching of files in the specified directory with specified file extension
    '''
    file_path_list = []
    file_name_list = []
    i = 0
    if print_or_not == 1: print ('  Directory: ', path, '\n')
    if print_or_not == 1: print ('  List of files found: ')
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file in files:
        if file.endswith(extension):
            i = i + 1
            if print_or_not == 1:  print ('         ', i, ') ', file)
            file_name_list.append(str(file))
    file_name_list.sort()
    return file_name_list


if __name__ == '__main__':

    path = 'DATA/'
    extension = '.adr'

    file_name_list = find_files_only_in_current_folder(path, extension, 1)
