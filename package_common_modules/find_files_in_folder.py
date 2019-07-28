import os

'''
'''

def find_files_in_folder(directory, extension):
    '''
    Searching of files in the specified directory with specified file extension
    '''
    fileList=[]
    i = 0
    print ('  Directory: ', directory, '\n')
    print ('  List of files found: ')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                i = i + 1
                print ('         ', i, ') ', file)
                fileList.append(str(os.path.join(root, file)))
    return fileList


if __name__ == '__main__':

    directory = 'DATA/'
    extension = '.adr'

    fileList = find_files_in_folder(directory, extension)
