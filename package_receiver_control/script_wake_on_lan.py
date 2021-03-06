# Python3
Software_version = '2020.12.25'  # !!! Not finished !!!
Software_name = 'Wake on LAN'

# *******************************************************************************
#                              P A R A M E T E R S                              *
# *******************************************************************************

# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import time
from wakeonlan import send_magic_packet

# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************
print('\n\n\n\n\n\n\n\n   ****************************************************')
print('   *   ', Software_name, '  v.', Software_version, '    *      (c) YeS 2020')
print('   **************************************************** \n\n\n')

start_time = time.time()
current_time = time.strftime("%H:%M:%S")
current_date = time.strftime("%d.%m.%Y")
print('   Today is ', current_date, ' time is ', current_time, '\n')


send_magic_packet('74.d0.2b.28.5f.c8')


endTime = time.time()
print('\n\n\n  The program execution lasted for ',
      round((endTime - start_time), 2), 'seconds (', round((endTime - start_time)/60, 2), 'min. ) \n')
print('\n           *** Program ', Software_name, ' has finished! *** \n\n\n')
