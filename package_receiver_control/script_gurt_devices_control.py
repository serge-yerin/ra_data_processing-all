# Python3
# The script sends one command to run RT-32 observations an keep server connected (each 90 secs sends '\0')
# *******************************************************************************
#                     I M P O R T    L I B R A R I E S                          *
# *******************************************************************************
import sys
from os import path
import socket
import time
from time import gmtime, strftime
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

# To change system path to main directory of the project:
if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# *******************************************************************************
#                              V A R I A B L E S                                *
# *******************************************************************************
hosts = ['192.168.1.11', '192.168.1.12', '192.168.1.169', '192.168.1.170', '192.168.1.171', '192.168.1.172', '8.8.8.8']

# *******************************************************************************
#                                F U N C T I O N S                              *
# *******************************************************************************


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0


def check_if_host_on_net(hosts):

    answers = []
    for host in hosts:
        answer = ping(host)
        answers.append(answer)

    t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print('\n\n\n ', t, 'GMT:  The results of check: ')
    for i in range(len(hosts)):
        print(' ', hosts[i], ' - ', answers[i])

    # # Keep connection live with sending /0 each 90 seconds
    # while True:
    #     time.sleep(90)
    #     t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #     print('\n ', t, 'GMT:  Sent command to keep connection')


# *******************************************************************************
#                           M A I N     P R O G R A M                           *
# *******************************************************************************

if __name__ == '__main__':
    check_if_host_on_net(hosts)




