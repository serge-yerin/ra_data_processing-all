import datetime
import time
from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage

def f_wait_predefined_time_connected(time_to_start, serversocket, synchro):  #
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
    f_read_adr_meassage(serversocket, 0)
    #'''
    now = datetime.datetime.now()
    diff = int((time_to_start - now).total_seconds())
    if diff > 0:
        result = True
        diff_hours = int(diff / 3600)
        diff_min = int((diff - diff_hours*3600) / 60)
        diff_sec = diff % 60
        print("\n   {:02d}:{:02d}:{:02d}  Wait for: {:02d} hr {:02d} min {:02d} sec...".format(now.hour, now.minute, now.second, diff_hours, diff_min, diff_sec))
        # Wait minutes
        if int(diff / 60) > 0:
            while True:
                time.sleep(60)
                #'''
                serversocket.send(('get prc/srv/ctl/pth\0').encode())
                f_read_adr_meassage(serversocket, 0)
                #'''
                now = datetime.datetime.now()
                diff = int((time_to_start - now).total_seconds())
                if int(diff / 60) <= 1:
                    break
        if synchro > 0:
            pass

        now = datetime.datetime.now()
        diff = int((time_to_start - now).total_seconds())
        print("   {:02d}:{:02d}:{:02d}  Wait for: {} min {:02d} sec...".format(now.hour, now.minute, now.second, int(diff / 60), diff % 60))

        # Wait seconds
        while True:
            time.sleep(1)
            now = datetime.datetime.now()
            diff = int((time_to_start - now).total_seconds())
            if diff < 1:
                print("   {:02d}:{:02d}:{:02d}  It's time!".format(now.hour, now.minute, now.second))
                break
    else:
        print('\n ERROR! Time has passed!')
        result = False
    return result

################################################################################

if __name__ == '__main__':

    time_to_start = datetime.datetime(2020, 4, 12, 23, 58, 00)
    precision = 1 # in seconds
    #f_wait_predefined_time_connected(serversocket, time_to_start)
    f_wait_predefined_time_connected(time_to_start)
