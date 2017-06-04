"""
    TCP  implementation over udp connection
    Jason Anchia   -- Esteban Castillo

"""

import socket
import sys  # used to read the file to send
import struct
import math
import time
import threading
# Variables --------------------------------------------------------------

# TARGET_IP = "10.0.0.2"
TARGET_IP = "localhost"
TARGET_PORT = 5005

print("UDP target IP:", TARGET_IP)
print("UDP target port:", TARGET_PORT)

# UDP_IP = "10.0.0.1"
UDP_IP = "localhost"
UDP_PORT = 5006

class Sender(object):
    "Emisor"

    def ackupdater(self):
        "Updates the value of sequence as new acks arrive**********************"
        self.fin = False
        print("*** hilo ack ***")
        while True:
            if self.fin:
                print('fin ---------')
                sys.exit(0)
            try:
                rcvack, addr = self.sock.recvfrom( 500 )
            except socket.timeout:
                print("ack timed out")
                return

            unpacked = struct.unpack("!ii", rcvack)
            ack, win = unpacked
            if self.ack < ack:
                self.ack = ack
                self.window_size = win
                print("received [ACK] Seq=_  Ack={} Win={} Len=_".format(self.ack, win))

    def __init__(self):
        "**********************************************************************"
        self.data = ""  # we will store here the data to be sent
        # Crea la conexion
        self.sock = socket.socket(socket.AF_INET,    # Internet
                                  socket.SOCK_DGRAM)  # UDP
        my_dir = (UDP_IP, UDP_PORT)
        print("listening on", my_dir)
        self.sock.bind(my_dir)
        self.sock.settimeout(1) # timeout in seconds
        self.window_size = 16000
        self.mss = 1460 # max segment size
        self.ack = 0
        self.ackr = threading.Thread(target=self.ackupdater)
        self.start()
        self.ackr.start()
        self.sendSeg()
        self.fin = False
        sys.exit(0)
        # EO Variables ---------------------------------------------------------


    # Methods ----------------------------------------------------------------

    def read_input_file(self):
        "Reads the input file specified as the argument 1**********************"
        if len(sys.argv) != 2:
            print('[Error]:\n\tNo file or more than 1 file specified\n')
            exit(1)
        with open(sys.argv[1], 'rb') as my_file: # b: binary mode
            self.data = my_file.read() # it is read as bytes
            # self.data = str.encode(file)

            # print( sys.getsizeof(  file ) )
            size_in_bytes = sys.getsizeof(self.data)
            print("transmitting", size_in_bytes, type(self.data).__name__, "(",
                  size_in_bytes / 1000, "kb)", "of data"
                 )

        # send()

    def start(self):
        "starts the negotiation of the window size*****************************"

        # send SYN
        self.read_input_file()
        ipcdd = str.encode(UDP_IP)
        # "https://docs.python.org/3/library/struct.html"
        data = struct.pack("!iii11s", self.mss, self.window_size, UDP_PORT, ipcdd)
        self.sock.sendto(data, (TARGET_IP, TARGET_PORT))

        # wait for syn-ack
        data, addr = self.sock.recvfrom(100) # buffer size in bytes

        # https://docs.python.org/3/library/struct.html
        unpacked = struct.unpack("!ii11s", data)
        window_size_rcv, port, ip = unpacked
        ipcdd = ip.decode("utf-8")
        print(
              "Machine {}:{} has accepted the synchronization request.".format(ipcdd, port),
              "Its windows size is {} bytes".format(window_size_rcv)
             )
        if window_size_rcv < self.window_size:
            self.window_size = window_size_rcv

        # send ack
        data = struct.pack("!ii", 0, 0)
        self.sock.sendto(data, (TARGET_IP, TARGET_PORT))

    def sendSeg(self):
        "send segments of the message to the receiver**************************"

        n = self.mss # divide the file in segments
        sgmts = [self.data[i:i+n] for i in range(0, len(self.data), n )]

        numbsegments = len(sgmts)
        print( "Prepairing to send", numbsegments, "segments" )
        print( "size (in bytes) of each segment is ", sys.getsizeof( sgmts[0] ) )

        segment_format = "%ds"%len(sgmts[0]) # format example: '11s'
        print ("--------------------------------", len(sgmts[0]))
        ack = 0
        seq_num = 0
        
        start = time.time()
        idx = 0
        while idx < numbsegments:
            if seq_num <= self.window_size:
                length = len( sgmts[idx] )
                print ("\tseq={} ack={} len={} ".format(seq_num, 1, length))
                # Header:
                header = struct.pack ("!?iii", False, seq_num, ack, length)
                headersize = sys.getsizeof( header )

                if headersize != 33+(3*4) + 1: # 2 ints * 4 bytes
                    print("header size mismatch")
                    exit(23)
                # pack the segment data
                sgdata = struct.pack ( segment_format, sgmts[idx]  )
                segmnt = header + sgdata
                # print ( segmnt )
                # print ( sys.getsizeof( segmnt ) )
                self.sock.sendto(segmnt, (TARGET_IP, TARGET_PORT))
                seq_num += length
                idx += 1
        end = time.time()
        print("\n\nenviados {} kb en {} segundos".format( str(round(seq_num/1024, 2)) , str(round(end - start, 2))))
        print("({} segmentos)".format(numbsegments))

        # send FIN flag ********************************************************
        header = struct.pack ("!?iii", True, 0, 0, 0)
        # pack the segment data
        sgdata = struct.pack ( segment_format, str.encode('')  )
        fin = header + sgdata
        self.fin = True
        self.sock.sendto(fin, (TARGET_IP, TARGET_PORT))
        # self.sock.shutdown(socket.SHUT_RDWR)
        # self.sock.close()
        # **********************************************************************
        return

    # EO Methods ---------------------------------------------------------------


SNDR = Sender()


# sock.sendto(MESSAGE_as_bytes, (UDP_IP, UDP_PORT))
