import os

'''
'''

def find_subfolders_in_folder(directory, print_or_not):
    '''
    Searching of subdirectories in the specified directory
    '''
    folder_list = [x[0] for x in os.walk(directory)]
    folder_list = folder_list[1:]
    if print_or_not == 1:
        for i in range (len(folder_list)):
            print ('         ', i+1, ') ', folder_list[i])
        if len(folder_list) == 0: print('  The directory does not have subdirectories!')
    return folder_list


if __name__ == '__main__':

    path = 'DATA/'

    file_name_list = find_subfolders_in_folder(path, 1)
