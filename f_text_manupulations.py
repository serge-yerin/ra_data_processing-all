'''
'''


# Searching of a line part between quotes (or any other symbols)
def find_between(string, start, stop):
    '''
    Finds a text between two characters (symbols)
    '''
    try:
        begin = string.index(start) + len(start)
        end = string.index(stop, begin)
        return string[begin:end]
    except ValueError:
        return "Error!"
        
