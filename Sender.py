"""
    TCP reno implementation asfd asdfdf
    Jason Anchia   -- Esteban Castillo


"""

import socket
import sys # used to read the file to send

# Variables --------------------------------------------------------------------------------

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
data = "" # we will store here the data to be sent

# EO Variables -----------------------------------------------------------------------------


print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)

#Crea la conexion
sock = socket.socket(socket.AF_INET,    # Internet
                     socket.SOCK_DGRAM) # UDP
                     
# Methods --------------------------------------------------------------------------------
def read_input():
    if len(sys.argv) != 2:
        print('[Error]:\n\tNo file or more than 1 file specified\n')
        return
    with open(sys.argv[1], 'r') as my_file:
        data = str.encode(    my_file.read()  )


    # send()
# EO Methods -----------------------------------------------------------------------------


read_input()
sys.exit(0)

                     
# sock.sendto(MESSAGE_as_bytes, (UDP_IP, UDP_PORT))
