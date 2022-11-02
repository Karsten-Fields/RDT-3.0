import socket   #for sockets
import sys
import check

# create dgram udp socket
try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
        print 'Failed to create socket'
        sys.exit()

#variables
host = 'localhost'
port = 8888
seq = 0

for i in range(3):
        while 1:
                msg = 'Hello World' + str(i)
                s.settimeout(4)
                try:
                        print "sending packet to reciever"
                        s.sendto(check.ip_checksum(msg) + "," + str(seq) + "," + msg, (host, port))
                        print "sent " + check.ip_checksum(msg) + "," + str(seq) + "," + msg
                        print "attempting to receive ACK"
                        d = s.recvfrom(1024)
                        reply = d[0]
                        addr = d[1]
                        #print "reply is: " + reply
                        #splitting data into array consisting of checksum, seq, and ACK
                        r = reply.split(",")
                        #checking if corrupt, or wrong seq, or not acknowledged (d[2] is the ACK: 0 for not acknowledged, 1 for acknowledged)
                        if int(r[0]) != 1 or int(r[1]) != seq:
                                print "packet either corrupt or out of sequence and was dropped"
                                continue
                        else:
                                #flip sequence to go to next state
                                print "packet acknowledgement " + r[1] + " received"
                                seq = 1 - seq
                                #exit while loop because data was not corrupt, the sequence was correct, and the ack was verified
                                break
                except socket.timeout:
                        print('Issue with communication caused timeout.')
                i += 1
        print("\n")
