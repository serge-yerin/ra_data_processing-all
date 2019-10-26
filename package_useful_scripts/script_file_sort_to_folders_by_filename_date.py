# Python3
Software_version = '2019.07.30'
Software_name = 'Sort files to folders by date in their name'
# Script intended to read, show and analyze data from

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
common_path =  'DATA/' # 'e:/PYTHON/ra_data_processing-all/DAT_Results/'
folder_to_sort = 'TEST_DATA'
extension = '.jds' # '.jds' or '.adr'

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
import os
from os import path
import sys
import time
import shutil

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_common_modules.find_files_in_folder import find_files_in_folder
################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************
print ('\n\n\n\n\n\n\n\n   ********************************************************************')
print ('   *  ',Software_name,' v.', Software_version,'    *      (c) YeS 2019')
print ('   ********************************************************************      \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, '\n')

path = common_path + folder_to_sort

# Search needed files in the directory and subdirectories
file_path_list, file_name_list = find_files_in_folder(path, extension)

for i in range (len(file_path_list)):
    file_path_list[i] = file_path_list[i].replace('\\','/')

print('\n  List of paths found: \n')

for i in range (len(file_path_list)):
    print('         ',  i+1 ,') ', file_path_list[i])

# Search the unique dates in filenames to make folder for each unique date
seen = set()
unique_dates = []
for file in range (len(file_name_list)):
    file_name_part = file_name_list[file][:7]
    if file_name_part not in seen:
        unique_dates.append(file_name_part)
        seen.add(file_name_part)

# Creating folders names according to unique filenames
new_folder_names = []
for i in range (len(unique_dates)):
    if extension == '.adr':
        new_folder_names.append('20'+unique_dates[i][1:3]+'.'+unique_dates[i][3:5]+'.'+unique_dates[i][5:7]+'_GURT_'+unique_dates[i][0]+'_/')
    if extension == '.jds':
        new_folder_names.append('20'+unique_dates[i][5:7]+'.'+unique_dates[i][3:5]+'.'+unique_dates[i][1:3]+'_UTR2_'+unique_dates[i][0]+'_/')
print('\n  List of prepared names of new folders: \n')

for i in range (len(unique_dates)):
    print('         ',  i+1 ,') ', new_folder_names[i])


print('\n  List of what to move and where: \n')

# Moving files
destination = ["" for x in range(len(file_name_list))]

for file in range (len(file_name_list)):
    for date in range (len(unique_dates)):
        if file_name_list[file][:7] == unique_dates[date]:
            destination[file] = common_path + new_folder_names[date] + file_name_list[file]
            print(' * from ', file_path_list[file], ' to ', destination[file], '\n')

move_or_not  = int(input('\n\n  Enter "1" if you want to move files, "0" otherwise:   '))

if (move_or_not == 1):

    # Creating folders
    for i in range (len(unique_dates)):
        newpath = common_path + new_folder_names[i]
        if not os.path.exists(newpath):
            os.makedirs(newpath)

    # Moving files
    for file in range (len(file_name_list)):
        shutil.move(file_path_list[file], destination[file])


print('\n\n\n             *** Files were moved! ***\n')


endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program TXT reader has finished! *** \n\n\n')
