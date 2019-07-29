# Python3
Software_version = '2019.07.30'
# Script intended to read, show and analyze data from

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
common_path =  'DATA/' # 'e:/PYTHON/ra_data_processing-all/DAT_Results/'
folder_to_sort = 'TEST_DATA'
extension = '.adr' # '.jds'

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
import os
import time
import shutil

from package_common_modules.find_files_in_folder import find_files_in_folder
################################################################################
#*******************************************************************************
#                          M A I N    P R O G R A M                            *
#*******************************************************************************
print ('\n\n\n\n\n\n\n\n   ***********************************************************')
print ('   *    Sort files to folders by date in their name  v1.0    *      (c) YeS 2019')
print ('   ***********************************************************      \n\n\n')

startTime = time.time()
currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime, '\n')

path = common_path + folder_to_sort

# Search needed files in the directory and subdirectories
file_path_list, file_name_list = find_files_in_folder(path, extension)

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
    new_folder_names.append('20'+unique_dates[i][1:3]+'.'+unique_dates[i][3:5]+'.'+unique_dates[i][5:7]+'_GURT_'+unique_dates[i][0]+'_/')

print('\n  List of prepared names of new folders: \n')

for i in range (len(unique_dates)):
    print('         ',  i+1 ,') ', new_folder_names[i])

# Creating folders
for i in range (len(unique_dates)):
    newpath = common_path + new_folder_names[i]
    if not os.path.exists(newpath):
        os.makedirs(newpath)

print('\n  List of what to move and where: \n')

# Moving files
for file in range (len(file_name_list)):
    for date in range (len(unique_dates)):
        if file_name_list[file][:7] == unique_dates[date]:
            destiantion = new_folder_names[date] + file_name_list[file]
            print(' - ', file_name_list[file], '\n    from ', file_path_list[file], ' to ', destiantion, '\n')
            #shutil.move(file_path_list[file], destiantion)







endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program TXT reader has finished! *** \n\n\n')
