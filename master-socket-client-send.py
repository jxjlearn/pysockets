
# coding: utf-8

# In[4]:

import socket
import sys

if len(sys.argv) > 2:
    print >>sys.stderr, "Usage: master-socket-cilent-send <message>"
    exit(-1)
elif len(sys.argv) == 2:
    script, messageTosend = sys.argv
else:
    messageTosend = 'This is the message. It will be repeated.'
#Create a TCP/IP client
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect the client to the server; make sure server is running
server_address = ('localhost', 6666)
print >>sys.stderr, 'connecting to %s port %s' % server_address
clientsocket.connect(server_address)

#Send the message after the connection is established
try:
    #Send data
    print >>sys.stderr, 'sending "%s"' % messageTosend
    clientsocket.sendall(messageTosend)
    
    #Look for the response
    amount_received = 0
    amount_expected = len(messageTosend)
    
    while amount_received < amount_expected:
        data = clientsocket.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data
        
finally:
    print >>sys.stderr, 'closing client'
    clientsocket.close()


# In[ ]:



