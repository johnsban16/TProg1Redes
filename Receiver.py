import socket
import struct, sys
import time

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
        self.window_size = 5000
        self.file = 0
        self.mss = 0
        self.target_ip   = 0
        self.target_port = 0
        print("listening on", my_dir)
        self.start()

    def start(self):
        "asadfs TODO"
        self.negotite_window()
        self.file = open("Output.txt", "wb") # write as bytes
        self.receive_segments()
        self.file.close()


    def negotite_window(self):
        "negotites the window size"
        print("waiting for connection")
        data, addr = self.sock.recvfrom(100) # buffer size in bytes

        print('***************************************************************')
        " wait SYN ----------------------------"
        unpacked = struct.unpack("!iii11s", data) # https://docs.python.org/3/library/struct.html
        mssrcv, window_size_rcv, port, ip = unpacked
        self.mss = mssrcv # udpate our mss value
        ipcdd = ip.decode("utf-8")
        print("A connection request from :", ipcdd,"port", port,
              "has been received.\n Its windows size is:", window_size_rcv, "bytes")
        print("informing client that our initial max window size is", self.window_size)

        " sending syn-ack ----------------------"
        #removing garbage from Sender ip and casting to bytes"
        self.target_ip  =  str.encode(ipcdd.translate( dict.fromkeys(range(32)) ))
        self.target_port = port
        my_ip = str.encode(UDP_IP)
        data = struct.pack("!ii11s", self.window_size, UDP_PORT, my_ip)
        self.sock.sendto(data, (self.target_ip, self.target_port))

        " wait ack------------------------------"
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

        headersize = 33+(3*4) +1# 2 ints * 4 bytes
        bodysize = self.mss
        print('PKG body size is %d'%bodysize)
        expected_seq_num = 0

        start = time.time()

        while True:
            data  = self.sock.recv(    self.mss + headersize )

            # https://docs.python.org/3/library/struct.html
            unpacked = struct.unpack("!?iii%ds"%bodysize, data)

            fin, rcv_seq_num, ack, length, data = unpacked

            if fin:
                print('pkg with FIN flag received')
                break

            if expected_seq_num == rcv_seq_num:
                print ("\tseq={} ack={} len={} ".format(1, rcv_seq_num+1, length))

                self.window_size += length

                # write segment to disk
                if length < self.mss:
                    # remove null bytes
                    self.file.write( data.partition(b'\0')[0]    )
                else:
                    self.file.write( data   )

                # send ack
                sndack = struct.pack ("!ii", rcv_seq_num+1, self.window_size)
                self.sock.sendto(sndack, (self.target_ip, self.target_port))
                expected_seq_num += length
        end = time.time()
        self.file.close()
        print("recibidos {} bytes en {} segundos".format(0, str(round(end - start, 2))))
        return


S = Server()
