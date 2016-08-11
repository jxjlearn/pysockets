
# coding: utf-8

# In[ ]:

import socket
import sys

#Create a TCP/IP client
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect the client to the server; make sure server is running
server_address = ('localhost', 6666)
print >>sys.stderr, 'connecting to %s port %s' % server_address
clientsocket.connect(server_address)

#Send the message after the connection is established
try:
    #Send data
    message = 'This is the message. It will be repeated'
    print >>sys.stderr, 'sending "%s"' % message
    clientsocket.sendall(message)
    
    #Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = clientsocket.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data
        
finally:
    print >>sys.stderr, 'closing client'
    clientsocket.close()

