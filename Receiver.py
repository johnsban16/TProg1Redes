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
        self.target_ip   = 0
        self.target_port = 0
        print("listening on", my_dir)
        self.start()

    def receive (self):
        "asdfasdfasdf"
        # while True:
        return 0

    def start(self):
        "asadfs TODO"
        self.negotite_window()
        self.file = open("Output.txt", "w")
        self.receive_segments()
        self.file.close()


    def negotite_window(self):
        "negotite window"
        print("waiting for connection")
        data, addr = self.sock.recvfrom(100) # buffer size in bytes

        print('***************************************************************')
        unpacked = struct.unpack("!ii11s", data) # https://docs.python.org/3/library/struct.html
        window_size_rcv, port, ip = unpacked
        ipcdd = ip.decode("utf-8")
        print("A connection from :", ipcdd,"port", port,
              "has been received.\n It declares a windows size of:", window_size_rcv, "bytes")
        print("informing client that our initial max window size is", self.my_window_size)
        if window_size_rcv < self.my_window_size:
            print( "received window size is smaller than our window size" )
            self.my_window_size = window_size_rcv


        # sending syn-ack
        "removing garbage from Sender ip and casting to bytes"
        self.target_ip  =  str.encode(ipcdd.translate( dict.fromkeys(range(32)) ))
        self.target_port = port
        my_ip = str.encode(UDP_IP)
        data = struct.pack("!ii11s", self.my_window_size, UDP_PORT, my_ip)
        self.sock.sendto(data, (self.target_ip, self.target_port))

        # wait ack
        data, addr = self.sock.recvfrom(100) # buffer size in bytes
        unpacked = struct.unpack("!ii", data) # https://docs.python.org/3/library/struct.html
        ack, seq_num = unpacked
        print(ack, seq_num)
        print('***************************************************************')
        return True

        # self.sock.sendto(str.encode('4096'), (UDP_IP, UDP_PORT))
        # tcp_header = struct.pack("!hH16s", seq_num, flags, digested)

    # sock.close()
    def receive_segments(self):
        "sddfsad TODO"
        print( "windows size of ",  self.my_window_size, "bytes" )

        headersize = 33+(3*4) # 2 ints * 4 bytes
        bodysize = self.my_window_size - headersize
        print('bodysize is %d'%bodysize)
        expected_seq_num = 0

        while True:
            data  = self.sock.recv(    self.my_window_size ) # buffer size in bytes
            # print("size of data", sys.getsizeof(data))

            # https://docs.python.org/3/library/struct.html
            unpacked = struct.unpack("!iii%ds"%bodysize, data)

            # source_port, destination_port, , , ,
            rcv_seq_num, ack, length, data = unpacked
            print(data.decode("utf-8") )

            if expected_seq_num == rcv_seq_num:
                print ("\tseq={} ack={} len={} ".format(1, rcv_seq_num, length))

                # self.my_window_size = 500 + asfdf

                # send ack
                sndack = struct.pack ("!ii", 1, rcv_seq_num)
                self.sock.sendto(sndack, (self.target_ip, self.target_port))
                # write segment to disk
                self.file.write(    data.decode("utf-8")    )
                expected_seq_num += 1

        # print ( sys.getsizeof( header ) )
        return


S = Server()
