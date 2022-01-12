
from datetime import datetime

# *******************************************************************************
#                FUNCTIONS TO CONVERT TIME TO VARIOUS FORMATS                   *
# *******************************************************************************


def str_date_and_time_to_datetime(str_date_time):
    """
    Converts string notation of date and time to datetime object
    : str_date_time : date and time in string format 'YYYY-MM-DD HH:MM:SS'
    : return : datetime object
    """
    datetime_date_time = datetime(int(str_date_time[0:4]), int(str_date_time[5:7]), int(str_date_time[8:10]),
                                  int(str_date_time[11:13]), int(str_date_time[14:16]), int(str_date_time[17:19]), 0)
    return datetime_date_time


# *******************************************************************************
#                           M A I N    P R O G R A M                            *
# *******************************************************************************


if __name__ == '__main__':

    str_time = '2021.01.01 12:00:00'

    dt_object = str_date_and_time_to_datetime(str_time)

    print('Result: ', dt_object)
