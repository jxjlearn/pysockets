# coding: utf-8

import socket
import sys
import subprocess

#constants
global gminHome, localRepo, kernelType
gminHome = './gmin-quilt-representation/'   #path to gmin-quilt-representation
localRepo = './test/'  #path to local repo
remoteUrl = 'https://xjjiao@github.com/intel-otcak/test.git'  #URL for remote repo
kernelType = 'cht-m1stable'
server_address = ('localhost', 6666) #server address


#mesage format definition
#[x]xxxxxxxxxxxxxx$
endMark = '@#$'

def msgMapping(msg):
#message as input
#mapping messages to differnt functions
#based on the fist 3 characters
    mapper = {
        '[s]': akquiltsync,
        '[r]': changeReport,
        '[t]': msgEcho,  #testing
    }
    return mapper.get(msg[:3], noDefinition)

#function definitions
def akquiltsync(msg):
#message as input
#string after [s] should be sha1
#run akquiltsync with sha1 as input
#then run step 3-5 of notes until change report generation
#send request to master
    sha1 = msg[3:]
    subprocess.check_call([gminHome + 'bin/akquiltsync', '-k', kernelType, sha1])

    #clone the remote repo
    subprocess.call(['git', 'clone', remoteUrl])

    #After akquiltsync finishes, the repo is on a specific branch created by the script.
    #Copy the patches to github repo.
    subprocess.call(['rm', '-rf', localRepo + 'uefi/cht-m1stable/patches'])
    subprocess.call(['cd', gminHome + 'uefi/cht-m1stable'])
    res = subprocess.Popen(['find', 'patches'], stdout=subprocess.PIPE)
    subprocess.check_call(['cpio', '-pdmuv', localRepo + 'uefi/cht-m1stable'], stdin=res.stdout)

    #Update technical debt report
    subprocess.call(['cd', gminHome])
    subprocess.call(['./bin/akgroup', '-c', '-d', 'uefi/cht-m1stable/patches', '>', localrepo + 'uefi/cht-m1stable/TechnicalDebtSummary.csv'])
    subprocess.call(['./bin/akgroup', '-cv', '-d', 'uefi/cht-m1stable/patches', '>', localrepo + 'uefi/cht-m1stable/TechnicalDebt.csv'])

    #Update change report



def changeReport(msg):
#changed content as input
#generate the change report
    pass

def gitUpdate():
#update github
    pass

def changeReport(connection, msg):
#msg[3:] is the content of report
    print >>sys.stderr, 'The follwing is the change report:'
    print >>sys.stderr, msg[3:]


def msgEcho(connection, msg):
#send the message back for testing
#connected socket and message are inputs
    print >>sys.stderr, 'echo back to the client'
    connection.sendall(msg[3:])

def noDefinition(connection, msg):
#msg not defined; server will send the error message back to client
    print >>sys.stderr, 'wrong format. notify the client'
    connection.sendall('Wrong format!' + endMark)



#create an NET, STREAMing(TCP/IP) socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tells the kernel to reuse a local socket in TIME_WAIT state
#serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


#server address

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
        msgStart = False
        msgEnd = False
        msg = ''

        while True:
            data = connection.recv(1024)
            print >>sys.stderr, "received '%s'" % data
            if not msgStart:
                msgStart = True
                func = msgMapping(data)
            msg += data
            if data.endswith(endMark):
                func(connection, msg)
                print >>sys.stderr, 'no more data from ', client_address
                print >>sys.stderr, 'notify the client that message received'
                connection.sendall(endMark)
                break
            if data == '':
                print >>sys.stderr, 'message without endMark, ignored!'
                break
    finally:
        #clean up the connection
        connection.close()
