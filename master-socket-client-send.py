
# coding: utf-8

# In[10]:

import socket
import sys

endMark = '[$]'

if len(sys.argv) >3:
    print >>sys.stderr, "Usage: master-socket-cilent-send <message>\n master-socket-client-send -f <file path>"
    exit(-1)
elif len(sys.argv) == 3:
    script, parameter, messageFile = sys.argv
    if parameter == '-f':
        with open(messageFile) as msgfile:
            messageTosend = msgfile.read().replace('\n', '') + endMark
    else:
        print >>sys.stderr, "Usage: master-socket-cilent-send <message>\n master-socket-client-send -f <file path>"
        exit(-1)
elif len(sys.argv) == 2:
    script, messageTosend = sys.argv
    messageTosend += endMark
else:
    messageTosend = 'This is the message. It will be repeated.' + endMark
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
    print messageTosend
    #Look for the response
    amount_received = 0
    amount_expected = len(messageTosend)

    while amount_received < amount_expected:
        data = clientsocket.recv(1024)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data
        if data.endswith(endMark):
            print >>sys.stderr, 'message received by the server'
            break

finally:
    print >>sys.stderr, 'closing client'
    clientsocket.close()


# In[ ]:



