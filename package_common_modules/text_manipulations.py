'''
'''


def find_between(string, start, stop):
    '''
    Searching of a line part between quotes (or any other symbols)
    '''
    try:
        begin = string.index(start) + len(start)
        end = string.index(stop, begin)
        return string[begin:end]
    except ValueError:
        return "Error!"


def read_date_time_and_one_value_txt (filenamelist):
    '''
    Reading txt files with time and date and one column data
    '''
    x_value = []
    y_value = []

    for file in range (len(filenamelist)):
        file = open(filenamelist[file], 'r')
        x_val = []
        y_val = []
        for line in file:
            words = line.rstrip().split()
            x_val.append(words[0] + ' ' + words[1])
            y_val.append(float(words[2]))
        file.close()

        x_value.append(x_val)
        y_value.append(y_val)
    return x_value, y_value




def read_frequency_and_two_values_txt(filenamelist):
    '''
    Reading txt files with frequecy and two value column data
    '''
    x_value = []
    y1_value = []
    y2_value = []

    for file in range (len(filenamelist)):
        file = open(filenamelist[file], 'r')
        x_val = []
        y1_val = []
        y2_val = []
        for line in file:
            words = line.rstrip().split()
            x_val.append(float(words[0]))
            y1_val.append(float(words[1]))
            y2_val.append(float(words[2]))
        file.close()

        x_value.append(x_val)
        y1_value.append(y1_val)
        y2_value.append(y2_val)
    return x_value, y1_value, y2_value
