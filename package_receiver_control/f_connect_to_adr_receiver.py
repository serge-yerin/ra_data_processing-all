# Python3
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import socket
import time
from package_receiver_control.f_read_adr_meassage import f_read_adr_meassage

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************
def f_connect_to_adr_receiver(host, port, control, delay):
    '''
    Function connects to the ADR receiver via specified socket
    Input parameters:
        host                - IP address to connect
        port                - port to connect
        control             - to control (1) or to view (0) possibility
        delay               - delay in seconds to wait after connection
    Output parameters:
        serversocket        - handle of socket to send and receive messages from server
        input_parameters_s  - long string with all receiver parameters at the moment of connection
    '''
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.connect((host, port))
    print('\n * Connected to host: ', host, ' port: ', port, '\n')
    serversocket.send('ADRSCTRL'.encode())
    register_cc_msg = bytearray([108,0,0,0])
    register_cc_msg.extend(b'YeS\0                                                            ')  # Name 64 bytes
    register_cc_msg.extend(b'adrs\0                           ')                          # Password 32 bytes
    register_cc_msg.extend([0, 0, 0, control])                                                         # Priv 4 bytes
    register_cc_msg.extend([0, 0, 0, control])                                                      # CTRL 4 bytes
    register_cc_msg = bytes(register_cc_msg)
    #print('\n Length: ', len(register_cc_msg))
    #print('\n Sent message: ', register_cc_msg)
    serversocket.send(register_cc_msg)

    data = f_read_adr_meassage(1)

    data = serversocket.recv(108)
    #print ('\n Returned register_cc_msg: ', data)
    print ('\n Control bit: ', data[-1])
    if data[-1] == 1:
        print (' * Control accepted')
    else:
        print(' * Control denied, view only!!!')

    # Reading all parameters valid now
    input_parameters_str = ''
    for i in range(23):
        input_parameters_str.append(f_read_adr_meassage(0))

    # Making pause to read the printed data
    time.sleep(delay)

    return serversocket, input_parameters_str


################################################################################

if __name__ == '__main__':

    host = '192.168.1.171'
    port = 38386
    control = 1
    delay = 5

    print('\n\n * Connecting to the ADR receiver... \n')

    f_connect_to_adr_receiver(host, port, control, delay)
