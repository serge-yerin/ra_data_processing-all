
from datetime import datetime

def time_line_file_reader(time_line_file_name):
    '''
    Reading timeline file and store data in text and datetime data format
    '''
    # Reading text timeline data from file
    tl_file = open(time_line_file_name, 'r')
    timeline = []
    for line in tl_file:
        timeline.append(str(line))
    tl_file.close()

    # Converting text to ".datetime" data format
    dt_timeline = []
    for i in range(len(timeline)):
        # Check is the uS field is empty. If so it means it is equal to '000000'
        uSecond = timeline[i][20:26]
        if len(uSecond) < 2: uSecond = '000000'

        dt_timeline.append(
            datetime(int(timeline[i][0:4]),   int(timeline[i][5:7]),   int(timeline[i][8:10]), int(timeline[i][11:13]),
                     int(timeline[i][14:16]), int(timeline[i][17:19]), int(uSecond)))

    return timeline, dt_timeline





if __name__ == '__main__':

    fname = 'E220213_201439.jds_Timeline.txt'

    print('\n\n File: ', fname)

    timeline, dt_timeline = time_line_file_reader(fname)

    print(' Time: ', timeline[0], ' - ', timeline[-1], ', number of points: ', len(timeline))