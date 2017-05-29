import socket
import struct, sys

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

"asdfasfsadfasdf"
class Server(object):
    "asfddsfdf"

    def __init__(self):
        # Crea la conexion
        self.sock = socket.socket(socket.AF_INET,    # Internet
                                  socket.SOCK_DGRAM)  # UDP
        my_dir = (UDP_IP, UDP_PORT)
        self.sock.bind(my_dir)
        self.my_window_size = 500
        self.file = 0
        print("listening on", my_dir)

    def receive (self):
        "asdfasdfasdf"
        # while True:
        return 0

    def start(self):
        self.negotite_window()
        self.file = open("Output.txt", "w")
        self.receive_segments()
        self.file.close()


    def negotite_window(self):
        "negotite window"
        print("waiting for connection")
        data, addr = self.sock.recvfrom(100) # buffer size in bytes

        unpacked = struct.unpack("!ii11s", data) # https://docs.python.org/3/library/struct.html
        window_size_rcv, port, ip = unpacked
        ipcdd = ip.decode("utf-8")
        print("A connection from :", ipcdd,"port", port, "has been requested. It declares a windows size of:", window_size_rcv, "bytes")
        print("informing client that our max windows size is", self.my_window_size)
        if ( window_size_rcv < self.my_window_size ):
            print( "received window size is smaller than our window size" )
            self.my_window_size = window_size_rcv


        # sending syn-ack
        TARGET_IP =  str.encode(ipcdd.translate( dict.fromkeys(range(32)) )) # removing garbage from Sender ip and casting to bytes
        TARGET_PORT = port
        my_ip = str.encode(UDP_IP)
        data = struct.pack("!ii11s", self.my_window_size, UDP_PORT, my_ip)
        self.sock.sendto(data, (TARGET_IP, TARGET_PORT))

        # wait ack
        data, addr = self.sock.recvfrom(100) # buffer size in bytes
        unpacked = struct.unpack("!ii", data) # https://docs.python.org/3/library/struct.html
        ack, seq_num = unpacked
        print(ack, seq_num)
        return True

        # self.sock.sendto(str.encode('4096'), (UDP_IP, UDP_PORT))
        # tcp_header = struct.pack("!hH16s", seq_num, flags, digested)

    # sock.close()
    def receive_segments(self):
        print( "windows size of ",  self.my_window_size, "bytes" )
        while True:
            data  = self.sock.recv(    self.my_window_size ) # buffer size in bytes
            headersize = 33+16
            bodysize = self.my_window_size - headersize
            # print("size of data", sys.getsizeof(data))
            unpacked = struct.unpack("!iiii%ds"%bodysize, data) # https://docs.python.org/3/library/struct.html

            source_port, destination_port, seq_num, ack, data = unpacked
            print ("received segment %d"%seq_num)
            self.file.write(    data.decode("utf-8")    )
        # print ( sys.getsizeof( header ) )
        return


S = Server()
S.start()
