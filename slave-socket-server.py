#!/usr/bin/python
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
#[x]xxxxxxxxxxxxxx\n
endMark = '\n'

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
def akquiltsync(connection, msg):
    '''
    #message as input
    #string after [s] should be sha1
    #check if  this sha has been synced
    #run akquiltsync with sha1 as input
    #then run step 3-5 of notes until change report generation
    #send request to master
    '''
    sha1 = msg[3:]
    print >>sys.stderr, '>>sha1:%s' % sha1
    
    #check if sync required
    if alreadySync :
        return
    #need to sync
    connection.sendall('Sync reqired. Do you want to sync (y/n)')

    #start sync
    print >>sys.stderr, '>>akquitsync is running...'
    cmd = 'cd ' + gminHome + ' && ' + './bin/akquiltsync ' + \
            '-k ' + kernelType + ' ' + sha1
    subprocess.check_call(cmd, shell=True)

    #clone the remote repo
    print >>sys.stderr, '>>removing the local repo %s...' % localRepo
    subprocess.call('rm -rf ' + localRepo, shell=True)
    print >>sys.stderr, '>>cloning github repo...'
    cmd = 'cd ~ ' + '&& ' + 'git clone ' + remoteUrl
    subprocess.call(cmd, shell=True)
    #Copy the patches to github repo.
    print >>sys.stderr, '>>updating the patches in github local copy...'
    cmd = 'rm' + ' -rf ' + localRepo + 'uefi/cht-m1stable/patches'
    subprocess.call(cmd, shell=True)

    cmd1 = 'cd ' + gminHome + 'uefi/cht-m1stable '
    cmd2 = 'find patches | cpio -pdmu ' + localRepo + 'uefi/cht-m1stable'
    subprocess.call(cmd1 + '&& ' + cmd2, shell=True)

    #Update technical debt report
    cmd = 'cd ' + gminHome
    print >>sys.stderr, '>>Generating TechnicalDebtSymmary.csv...'
    subprocess.call(cmd + ' && ' + './bin/akgroup ' + '-c ' + '-d ' + \
                    'uefi/cht-m1stable/patches ' + '> ' + localRepo + \
                    'uefi/cht-m1stable/TechnicalDebtSummary.csv', \
                    shell=True)
    print >>sys.stderr, '>>Generating TechnicalDebt.csv...'
    subprocess.call(cmd + ' && ' + './bin/akgroup ' + '-cv ' + '-d ' + \
                    'uefi/cht-m1stable/patches ' + '> ' + localRepo + \
                    'uefi/cht-m1stable/TechnicalDebt.csv', shell=True)

    #get the difference between updated series and github one
    print >>sys.stderr, '>>saving the git diff into "git-diff.txt"...'
    with open('git-diff.txt', 'w') as diffFile :
	subprocess.call('cd ' + localRepo + ' && ' + \
                 'git diff uefi/cht-m1stable/patches/series', \
                 shell=True, stdout=diffFile, stderr=diffFile)

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
        msg = ''

        while True:
            msg += connection.recv(1024)
            if msg == '':
                print >>sys.stderr, 'client is closed!'
                break
            if not msgStart:
                msgStart = True
                func = msgMapping(msg)
            if msg.endswith(endMark):
                func(connection, msg)
                print >>sys.stderr, "received '%s'" % msg
                '''
                #one message received. Client is still connected 
                Go back to inital state to waiting for new message
                '''
                msg = ''
                msgStart = False
                print >>sys.stderr, 'still connected; waiting for new message'
    finally:
        #clean up the connection
        connection.close()
