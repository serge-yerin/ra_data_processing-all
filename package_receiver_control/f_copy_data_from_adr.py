# Python3
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
from pexpect import pxssh

# *******************************************************************************
#                          M A I N    F U N C T I O N                           *
# *******************************************************************************


def f_copy_data_from_adr(receiver_ip, data_directory_name, dir_data_on_server, print_or_not):

    '''
    Function initializes ADR receiver if it was just turned on
    Input parameters:
        serversocket        - handle of socket to send and receive messages from server
        print_or_not        - to print the parameters to console (1) or not (0)
    Output parameters:
    '''

    # Copy data from receiver to server with SSH login on receiver and using rsync
    print('\n * Copying recorded data to server')

    receiver_file = open('service_data/receiver.txt', 'r')
    rec_user = receiver_file.readline()[:-1]
    password = receiver_file.readline()[:-1]
    receiver_file.close()

    this_pc_file = open('service_data/this_pc.txt', 'r')
    this_pc_ip = this_pc_file.readline()[:-1]
    this_pc_user = this_pc_file.readline()[:-1]
    this_pc_file.close()

    s = pxssh.pxssh(timeout=120000)
    #if not s.login(receiver_ip, 'root', 'ghbtvybr'):
    if not s.login(receiver_ip, rec_user, password):
        print('\n   ERROR! SSH session failed on login!')
        print(str(s))
    else:
        print('\n   SSH login successful, copying data to server...\n')
        #command = ('rsync -r ' + '/data/' + data_directory_name + '/' +
        #           ' gurt@192.168.1.150:'+ dir_data_on_server + data_directory_name + '/')
        command = ('rsync -r ' + '/data/' + data_directory_name + '/ ' + this_pc_user +'@' +
                   this_pc_ip + ':' + dir_data_on_server + data_directory_name + '/')
        #print(command)
        s.sendline(command)
        s.prompt()  # match the prompt
        if print_or_not > 0:
            print('\n   Answer: ', s.before)  # print everything before the prompt.
        s.logout()
    # To make this work properly one needs to pair receiver and server via SSH to not ask password each time
    # Execute commands directly on the receiver or via ssh:
    # ssh-keygen
    # ssh-copy-id -i /root/.ssh/id_rsa.pub gurt@192.168.1.150
    return 1

################################################################################

if __name__ == '__main__':

    receiver_ip = '192.168.1.171'
    port = 38386
    control = 1
    delay = 5

    ok = f_copy_data_from_adr(receiver_ip, data_directory_name, dir_data_on_server, print_or_not)
