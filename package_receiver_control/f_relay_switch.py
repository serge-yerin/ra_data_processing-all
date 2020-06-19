# Python3
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import socket
import time

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************

def f_send_command_to_relay(serversocket, relay_no, command):
    '''
    Function sends commands to the SR-201 relay block and shows the relay status
    Input parameters:
        serversocket        - socket of the relay to communicate
        relay_no            - number of the relay on the board
        command             - command 'ON' or 'OFF'
    Output parameters:

    '''

    relay_no_str = str(relay_no)
    if str(command).lower() == 'on':
        command = '1'
    elif str(command).lower() == '0':
        command = '0'
    else:
        command = '2'
    send_command = command + relay_no_str
    serversocket.send(send_command.encode())
    byte = b'a'
    message = bytearray([])
    byte = serversocket.recv(8)
    message.extend(byte)
    message = bytes(message).decode()
    print('\n Relays status: ', message[0:2])

    return

def f_relay_control(host, port):
    '''
    Function connects to the SR-201 relay block and controls the relays
    Input parameters:
        host                - IP address to connect
        port                - port to connect
    Output parameters:

    '''
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.connect((host, port))

    f_send_command_to_relay(serversocket, 0, 0) # Check status

    time.sleep(3)

    f_send_command_to_relay(serversocket, 1, 'ON')

    time.sleep(1)

    f_send_command_to_relay(serversocket, 2, 'ON')

    time.sleep(3)

    f_send_command_to_relay(serversocket, 1, 'OFF')

    time.sleep(1)

    f_send_command_to_relay(serversocket, 2, 'OFF')

    return



################################################################################

if __name__ == '__main__':

    host = '10.0.15.170'
    port = 6722

    print('\n\n * Connecting to the SR-201 relay... \n')

    f_relay_control(host, port)
