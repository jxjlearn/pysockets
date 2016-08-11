
# coding: utf-8

# In[6]:

import socket
import sys
#create an NET, STREAMing(TCP/IP) socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#server address
server_address = ('localhost', 6666)

#bind the socket to a host and a port
print >>sys.stderr, 'starting up on %s port %s' % server_address
serversocket.bind(server_address)

#Listen for incoming connections
serversocket.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = serversocket.accept()
    
    #connection happens
    try:
        print >>sys.stderr, 'connection from', client_address
        
        #Recieve the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print >>sys.stderr, "received '%s'" % data
            if data:
                print >>sys.stderr, 'sending data back to the client'
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
    
    finally:
        #clean up the connection
        connection.close()
                    


# In[ ]:



