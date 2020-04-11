import datetime
import time
from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage

def f_wait_predefined_time_connected(time_to_start, serversocket):
    '''
    Function waits the predefined time and once a minute reads something from ADR receiver to
    save connection to ADR server
    Input parameters:
        time_to_start       - datetime variable with time to continue the script
        serversocket        - socket handle to keep the connection alive
    Output parameter:
        result              - boolean variable (1) if time was chosen correctly (0) if not
    '''
    #'''
    serversocket.send(('get prc/srv/ctl/pth\0').encode())
    f_read_adr_meassage(0)
    #'''
    now = datetime.datetime.now()
    diff = int((time_to_start - now).total_seconds())
    if diff > 0:
        result = True
        print("\n {:02d}:{:02d}:{:02d}  Wait for: {:02d} hour {:02d} min {:02d} sec...".format(now.hour, now.minute, now.second, int(diff / 3600), int(diff / 60), diff % 60))
        # Wait minutes
        if int(diff / 60) > 0:
            while True:
                time.sleep(60)
                #'''
                serversocket.send(('get prc/srv/ctl/pth\0').encode())
                f_read_adr_meassage(0)
                #'''
                now = datetime.datetime.now()
                diff = int((time_to_start - now).total_seconds())
                if int(diff / 60) <= 1:
                    break

        now = datetime.datetime.now()
        diff = int((time_to_start - now).total_seconds())
        print(" {:02d}:{:02d}:{:02d}  Starting in: {} min {:02d} sec...".format(now.hour, now.minute, now.second, int(diff / 60), diff % 60))

        # Wait seconds
        while True:
            time.sleep(1)
            now = datetime.datetime.now()
            diff = int((time_to_start - now).total_seconds())
            if diff <= 0:
                print(" {:02d}:{:02d}:{:02d}  Starting!".format(now.hour, now.minute, now.second))
                break
    else:
        print('\n ERROR! Time has passed!')
        result = False
    return result

################################################################################

if __name__ == '__main__':

    time_to_start = datetime.datetime(2020, 4, 11, 22, 20, 10)
    precision = 1 # in seconds
    f_wait_predefined_time_connected(time_to_start)
