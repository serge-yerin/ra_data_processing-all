# Python 3
#*************************************************************
#                       MAIN FUNCTION                        *
#*************************************************************
def f_read_adr_meassage(serversocket, print_or_not):
    '''
    Function reads a message from ADR radio astronomy receiver
    Input parameters:
        print_or_not   - to print (1) or not (0) the message to terminal
    Output parameters:
        message        - string message
    '''
    byte = b'a'
    message = bytearray([])
    while byte != b'\0':
        byte = serversocket.recv(1)
        message.extend(byte)
    message = bytes(message).decode()
    if print_or_not == 1:
        print('\n Length: ', len(message))
        print('\n Received long message: ', message)
    return message 


################################################################################

if __name__ == '__main__':

    print('\n\n * Reading message from the ADR receiver... \n')

    f_read_adr_meassage(1)

