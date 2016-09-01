#!/usr/bin/python
# coding: utf-8
#interactive interface to send message to slave
import socket
import sys

endMark = '\n'

#Create a TCP/IP client
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect the client to the server; make sure server is running
server_address = ('localhost', 6666)
print >>sys.stderr, 'connecting to %s port %s' % server_address
clientsocket.connect(server_address)

#Send the message after the connection is established
try:
    while True:
        messageRecv = ''
        #accept the input from stdin
        print >>sys.stderr, 'waiting for new instruction'
        messageTosend = raw_input(">: ") + endMark
        #Send data
        print >>sys.stderr, 'sending "%s"' % messageTosend
        clientsocket.sendall(messageTosend)
        #Look for the response
        while True :
            messageRecv += clientsocket.recv(1024)
            if messageRecv.endswith(endMark):
                print >>sys.stderr, 'received: "%s"' % messageRecv
                break

finally:
    print >>sys.stderr, 'closing client'
    clientsocket.close()
