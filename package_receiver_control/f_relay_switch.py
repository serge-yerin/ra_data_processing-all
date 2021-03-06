# Python3
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import socket
import time

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************


def read_relay_output(serversocket):
    byte = b'a'
    message = bytearray([])
    byte = serversocket.recv(8)
    message.extend(byte)
    message = bytes(message).decode()
    print('\n  Relays status: ', message[0:2])
    return message


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
    if str(command).lower() == 'on_on-off':    # Press ON button (and release it in 0.4 s)
        print('\n  Pressing ON-OFF button (to switch on the computer) on relay ', relay_no_str)
        send_command = '1' + relay_no_str
        serversocket.send(send_command.encode())
        message = read_relay_output(serversocket)
        time.sleep(0.5)
        send_command = '2' + relay_no_str
        serversocket.send(send_command.encode())
        message = read_relay_output(serversocket)
    elif str(command).lower() == 'off_on-off':    # Press OFF button (and release it in 10 s)
        print('\n  Long pressing ON-OFF button (to switch off the computer) on relay ', relay_no_str)
        send_command = '1' + relay_no_str
        serversocket.send(send_command.encode())
        message = read_relay_output(serversocket)
        time.sleep(5)
        send_command = '2' + relay_no_str
        serversocket.send(send_command.encode())
        message = read_relay_output(serversocket)
    else:
        if str(command).lower() == 'on':        # ON and keep state
            print('\n  Short (1) the relay input ', relay_no_str)
            command = '1'
        elif str(command).lower() == '0':       # Check state
            command = '0'
        else:                                   # OFF and keep state
            print('\n  Release (0) the relay input ', relay_no_str)
            command = '2'
        send_command = command + relay_no_str
        serversocket.send(send_command.encode())
        message = read_relay_output(serversocket)
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

    # Check the relay current state
    f_send_command_to_relay(serversocket, 0, 0)

    # Wait some time till the next command
    time.sleep(15)

    # Turn OFF the ADR #1
    # f_send_command_to_relay(serversocket, 1, 'OFF_ON-OFF')

    # time.sleep(45)

    # Turn ON the ADR #1
    # f_send_command_to_relay(serversocket, 1, 'ON_ON-OFF')

    # Turn OFF GURT central control unit
    # f_send_command_to_relay(serversocket, 2, 'OFF')

    # time.sleep(45)

    # Turn ON GURT central control unit
    f_send_command_to_relay(serversocket, 2, 'ON')

    # Wait some time till the next command
    time.sleep(15)

    # Check the relay current state
    f_send_command_to_relay(serversocket, 0, 0)

    print('\n  Relay control program finished!')

    return


################################################################################


if __name__ == '__main__':
    host = '192.168.1.170'
    # host = '10.0.15.170'
    port = 6722

    print('\n\n * Connecting to the SR-201 relay... \n')

    f_relay_control(host, port)
