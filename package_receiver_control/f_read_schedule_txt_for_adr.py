# Python 3
import sys
from os import path
from datetime import datetime
from package_common_modules.text_manipulations import find_between

# *************************************************************
#                        MAIN FUNCTION                        *
# *************************************************************


def f_read_schedule_txt_for_adr(schedule_txt_file):
    '''
    Function reads a message from ADR radio astronomy receiver
    Input parameters:
        schedule_txt_file        - name of txt file with observation schedule
    Output parameters:
    '''
    # print('\n * Reading observation schedule...')
    schedule = []
    file = open(schedule_txt_file, "r")
    for line in file:
        if line.strip().startswith('#'):
            pass
        elif line.strip().startswith('START:'):
            line = line.replace(' ', '').rstrip('\n')
            start_time =       find_parameter_value(line, 'START:')
            fft_size =         find_parameter_value(line, 'FFT:')
            time_resolution =  find_parameter_value(line, 'DT:')
            start_frequency =  find_parameter_value(line, 'FSTART:')
            stop_frequency =   find_parameter_value(line, 'FSTOP:')
            data_directory =   find_parameter_value(line, 'NAME:')
            file_description = find_parameter_value(line, 'DESCR:')
            param_file_name =  find_parameter_value(line, 'PARAM:')
        elif line.strip().startswith('STOP:'):
            line = line.replace(' ', '').rstrip('\n')
            stop_time =      find_parameter_value(line, 'STOP:')
            copy_or_not =    int(find_parameter_value(line, 'COPY:'))
            process_or_not = int(find_parameter_value(line, 'PROC:'))

            # The condition: to process you must copy data
            if process_or_not > 0:
                copy_or_not = 1

            # Adding parameters to list
            schedule.append([start_time[:10]+' '+start_time[10:], stop_time[:10]+' '+stop_time[10:], fft_size,
                             time_resolution, start_frequency, stop_frequency, data_directory, file_description,
                             copy_or_not, process_or_not, param_file_name])
        else:
            pass

    # Check time correctness (later then now, start is before stop): storing them in datetime format in one list
    time_line = []
    for item in range(len(schedule)):
        time_point = schedule[item][0]
        dt_time = datetime(int(time_point[0:4]), int(time_point[5:7]), int(time_point[8:10]),
                           int(time_point[11:13]), int(time_point[14:16]), int(time_point[17:19]), 0)
        time_line.append(dt_time)
        time_point = schedule[item][1]
        dt_time = datetime(int(time_point[0:4]), int(time_point[5:7]), int(time_point[8:10]),
                           int(time_point[11:13]), int(time_point[14:16]), int(time_point[17:19]), 0)
        time_line.append(dt_time)

    # Verifying that time limits in list go one after another
    for item in range(2 * len(schedule) - 1):
        if time_line[item+1] > time_line[item]:
            pass
        else:
            print('\n  ERROR! Time is not in right order!!! \n\n')
            sys.exit('         Program stopped')

    # Check if the first time in the list is in future
    now = datetime.now()
    diff = int((time_line[0] - now).total_seconds())
    if diff <= 0:
        print('\n  ERROR! Time is in the past!!! \n\n')
        sys.exit('         Program stopped')

    # check FFT value correctness

    print('\n * Number of observations found: ', len(schedule))

    return schedule


def find_parameter_value(line, string_name):
    if string_name in line:
        value = (find_between(line, string_name, ','))
        if value == 'Error!':
            begin = line.index(string_name) + len(string_name)
            value = line[begin:]
    else:
        value = None
    return value

################################################################################


if __name__ == '__main__':

    # To change system path to main directory of the project:
    if __package__ is None:
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    schedule_txt_file = 'Observations.txt'

    schedule = f_read_schedule_txt_for_adr(schedule_txt_file)
    for i in range(len(schedule)):
        print(schedule[i])

