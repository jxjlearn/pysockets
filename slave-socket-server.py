# coding: utf-8

import socket
import sys

#create an NET, STREAMing(TCP/IP) socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tells the kernel to reuse a local socket in TIME_WAIT state
#serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

#mesage definition
def msgMapping(connection):
#message as input
#mapping messages to differnt functions
    mapper = {
        '[s]': akquiltsync,
        '[r]': changeReport,
        '[t]': msgEcho,  #testing
    }
    msgStart = False
    msg = ''
    while True:
        data = connection.recv(16)
        print >>sys.stderr, "received '%s'" % data
        if data:
            if not msgStart:
                msgStart = True
                func = mapper.get(data[:3], noDefinition)
            msg += data
        else:
            print msg
            print func
            func(connection, msg)
            print >>sys.stderr, 'no more data from', client_address
            break

#function definitions
def akquiltsync(msg):
#run akquiltsync with sha1 as input
#then run step 3-5 of notes until change report generation
#send request to master
    pass

def changeReport(msg):
#changed content as input
#generate the change report
    pass

def gitUpdate():
#update github
    pass

def msgEcho(connection, msg):
#send the message back for testing
#connected socket and message are inputs
    print >>sys.stderr, 'echo back to the client'
    connection.sendall(msg[3:])

def noDefinition(connection, msg):
#msg not defined; server will send the error message back to client
    print >>sys.stderr, 'sending data back to the client'
    connection.sendall('message not defined!')





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
        msgMapping(connection)
    finally:
        #clean up the connection
        connection.close()





