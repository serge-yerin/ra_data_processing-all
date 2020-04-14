import datetime
import time
from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage
from package_receiver_control.f_synchronize_adr import f_synchronize_adr

def f_wait_predefined_time_connected(time_to_start, serversocket, synchro = 0, host = '192.168.1.171'):  #
    '''
    Function waits the predefined time and once a minute reads something from ADR receiver to
    save connection to ADR server
    Input parameters:
        time_to_start       - datetime variable with time to continue the script
        serversocket        - socket handle to keep the connection alive
        synchro             - to synchronize the receiver before timer end (1 - yes, 0 - no)
    Output parameter:
        result              - boolean variable (1) if time was chosen correctly (0) if not
    '''
    #'''
    # Keeping connection active
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
                # Keeping connection active
                serversocket.send(('get prc/srv/ctl/pth\0').encode())
                f_read_adr_meassage(serversocket, 0)
                #'''
                now = datetime.datetime.now()
                diff = int((time_to_start - now).total_seconds())
                if int(diff / 60) <= 1:
                    break
        if synchro > 0:
            # Update synchronization of PC and ADR
            f_synchronize_adr(serversocket, host)
            print('') # To make empty line after synchro info

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
    f_wait_predefined_time_connected(time_to_start, serversocket, 1)
