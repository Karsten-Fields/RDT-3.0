import socket
import sys
import check
import time

HOST = ''       # Symbolic name meaning all available interfaces
PORT = 8888     # Arbitrary non-privileged port
seq = 0

# Datagram (udp) socket
try :
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print 'Socket created'
except socket.error, msg :
        print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()


# Bind socket to local host and port
try:
        s.bind((HOST, PORT))
except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

print 'Socket bind complete'

#now keep talking with the client
while 1:
        # receive data from client (data, addr)
        d = s.recvfrom(2048)
        data = d[0]
        addr = d[1]

        if not data:
                break

        contents = data.split(",")
        checksum = contents[0]
        sequence = contents[1]
        message = contents[2]

        print "checksum: ", checksum, ", sequence: ", sequence, ", message: ", message

        if checksum  == check.ip_checksum(message) and int(sequence) == seq:
                print("message is: ", message)
                s.sendto("1," + str(seq), addr)
                seq = 1 - seq

s.close()
