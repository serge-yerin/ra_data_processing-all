
from datetime import datetime


def time_line_file_reader(time_line_file_name):
    """
    Reading timeline file and store data in lists of text and datetime data formats
    """
    # Reading text timeline data from file
    tl_file = open(time_line_file_name, 'r')
    time_line_f = []
    for line in tl_file:
        time_line_f.append(str(line))
    tl_file.close()

    # Converting text to ".datetime" data format
    dt_time_line_f = []
    for i in range(len(time_line_f)):
        # Check is the uS field is empty. If so it means it is equal to '000000'
        u_second = time_line_f[i][20:26]
        if len(u_second) < 2:
            u_second = '000000'

        dt_time_line_f.append(
            datetime(int(time_line_f[i][0:4]),   int(time_line_f[i][5:7]),   int(time_line_f[i][8:10]), int(time_line_f[i][11:13]),
                     int(time_line_f[i][14:16]), int(time_line_f[i][17:19]), int(u_second)))

    return time_line_f, dt_time_line_f


if __name__ == '__main__':

    fname = 'E220213_201439.jds_Timeline.txt'

    print('\n\n File: ', fname)

    timeline, dt_timeline = time_line_file_reader(fname)

    print(' Time: ', timeline[0], ' - ', timeline[-1], ', number of points: ', len(timeline))