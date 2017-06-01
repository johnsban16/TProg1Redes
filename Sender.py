"""
    TCP reno implementation asfd asdfdf
    Jason Anchia   -- Esteban Castillo


"""

import socket
import sys  # used to read the file to send
import struct
import math
import threading
# Variables --------------------------------------------------------------

TARGET_IP = "127.0.0.1"
TARGET_PORT = 5005

print("UDP target IP:", TARGET_IP)
print("UDP target port:", TARGET_PORT)

UDP_IP = "127.0.0.1"
UDP_PORT = 5006

class Sender(object):
    "sadfdafsfasdfasdadf"

    def ackupdater(self):
        "sdfghj TODO"
        self.ack = 0
        print("*** hilo ack ***")
        while True:
            rcvack, addr = self.sock.recvfrom( 500 )
            unpacked = struct.unpack("!ii", rcvack)
            seq, rcvack = unpacked
            if self.ack <= rcvack:
                self.ack = rcvack+1
                print("received ack %d"%self.ack)

    def __init__(self):
        self.data = ""  # we will store here the data to be sent
        # Crea la conexion
        self.sock = socket.socket(socket.AF_INET,    # Internet
                                  socket.SOCK_DGRAM)  # UDP

        my_dir = (UDP_IP, UDP_PORT)
        self.sock.bind(my_dir)
        self.window_size = 4096
        self.ack = 0
        print("listening on", my_dir)
        self.ackr = threading.Thread(target=self.ackupdater)
        self.start()
        self.ackr.start()
        self.sendSeg()
        sys.exit(0)


    header_size = 20
    mss = 1480 - header_size  # > https://en.wikipedia.org/wiki/Maximum_segment_size
    # MSS specifies the largest amount of data, specified in bytes, that a computer
    # or communications device can receive in a single TCP segment"""

    # EO Variables -----------------------------------------------------------


    # Methods ----------------------------------------------------------------

    def read_input_file(self):
        "asfsdafasadf"
        if len(sys.argv) != 2:
            print('[Error]:\n\tNo file or more than 1 file specified\n')
            exit(1)
        with open(sys.argv[1], 'r') as my_file:
            file = my_file.read()
            self.data = str.encode(file)

            # print( sys.getsizeof(  file ) )
            size_in_bytes = sys.getsizeof(self.data)
            print("transmitting", size_in_bytes, type(self.data).__name__, "(",
                  size_in_bytes / 1000, "kb)", "of data"
                 )

        # send()

    def start(self):
        "start negotiting the window size"

        # send syn
        self.read_input_file()
        ipcdd = str.encode(UDP_IP)
        # "https://docs.python.org/3/library/struct.html"
        data = struct.pack("!ii11s", self.window_size, UDP_PORT, ipcdd)
        self.sock.sendto(data, (TARGET_IP, TARGET_PORT))

        # wait for syn-ack
        data, addr = self.sock.recvfrom(100) # buffer size in bytes

        # https://docs.python.org/3/library/struct.html
        unpacked = struct.unpack("!ii11s", data)
        window_size_svr, port, ip = unpacked
        ipcdd = ip.decode("utf-8")
        print("A connection from :", ipcdd,"port", port,
              "has been requested. It requests a windows size of:", window_size_svr, "bytes")
        self.window_size = window_size_svr

        # send ack
        data = struct.pack("!ii", 0, 0)
        self.sock.sendto(data, (TARGET_IP, TARGET_PORT))

    def sendSeg(self):
        "send segments of the message to the receiver"

        # window_size - headersize
        n = self.window_size - (33+(3*4))
        sgmts = [self.data[i:i+n] for i in range(0, len(self.data), n )]

        numbsegments = len(sgmts)
        print( "Prepairing to send", numbsegments, "segments" )
        print( "size (in bytes) of each segment is ", sys.getsizeof( sgmts[0] ) )

        # print(sgmts[0])

        # source_ip = str.encode(UDP_IP)
        # destination_ip = str.encode(TARGET_IP)


        segment_format = "%ds"%len(sgmts[0])
		# ack = math.ceil(sys.getsizeof(self.data)/self.window_size)
        ack = 0
        seq_num = 0
        while seq_num < numbsegments:
            if seq_num <= self.ack:
                print("sending segment %d"%seq_num)
                # Header:
                # source_port     destination_port    seq_num     ack
                lenght = sys.getsizeof( sgmts[seq_num] )
                header = struct.pack ("!iii", seq_num, ack, lenght)
                headersize = sys.getsizeof( header )

                if headersize != 33+(3*4) : # 2 ints * 4 bytes
                    print("header size mismatch")
                    exit(23)
                sgdata = struct.pack ( segment_format, sgmts[seq_num]  ) # pack the segment data
                segmnt = header + sgdata
                # print ( segmnt )
                # print ( sys.getsizeof( segmnt ) )
                self.sock.sendto(segmnt, (TARGET_IP, TARGET_PORT))
                seq_num += 1
        print('File sent')

    # EO Methods -------------------------------------------------------------


SNDR = Sender()


# sock.sendto(MESSAGE_as_bytes, (UDP_IP, UDP_PORT))
