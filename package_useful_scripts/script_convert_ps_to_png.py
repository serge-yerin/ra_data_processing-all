# Python3
Software_version = '2019.07.30'
Software_name = 'Sort files to folders by date in their name'
# Script intended to read, show and analyze data from

#*******************************************************************************
#                             P A R A M E T E R S                              *
#*******************************************************************************
# Path to data files
common_path =  'DATA/' # 'e:/PYTHON/ra_data_processing-all/DAT_Results/'
extension = '.ps' # '.jds' or '.adr'

################################################################################
#*******************************************************************************
#                    I M P O R T    L I B R A R I E S                          *
#*******************************************************************************
import os
from os import path
import sys
import time
from PIL import Image



# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from package_common_modules.find_all_files_in_folder_and_subfolders import find_all_files_in_folder_and_subfolders


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

file_path_list, file_name_list = find_all_files_in_folder_and_subfolders(common_path, extension, 1)

for file_no in range(len(file_name_list)):
    out = file_name_list[file_no].replace(extension,'.png')
    img = Image.open(file_path_list[file_no])
    img.load(scale=4)
    #img.rotate(90).show()
    img.show()
    img.save(out)





endTime = time.time()
print ('\n\n\n  The program execution lasted for ', round((endTime - startTime), 2), 'seconds (',
                                                round((endTime - startTime)/60, 2), 'min. ) \n')
print ('\n           *** Program TXT reader has finished! *** \n\n\n')
