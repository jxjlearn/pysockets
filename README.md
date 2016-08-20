# pysockets
Py scripts using sockets to establish the communication between master client and slave server.

Message format:
```
[x]xxxxxxxxxxx[$]
```
.. [s]: Run akquiltsync, copy pathced to github repo, and update debt report
.. [r]: Message with content of change report
.. [t]: message echo for testing
.. [$]: endMark

Function 'msgmapping' will map the message to different function based on the first 3 characters of message: [x]

Server script thinks the message is over when catches endMark at the end.

## usage
slave-socket-server.py : receives the message from master client and perform the corresponding scripts on slave machine.
```
python slave-socket-server.py 
```
master-send.py: interactive interface
```
python master-send.py
```

master-socket-client-send,py: sends message to slave server
```
python master-socket-client-send.py
```
.. sends default message defined in the script

```
python master-socket-client-send.py <msg>
```
.. sends customized message

```
python master-socket-client-send.py -f <path2file/file>
```
.. sends file content as the message 

## issues
1. endMark = '[$]'. Message will be process after all of it is recieved. It garantees the compleness of message received, but would cosume more space if the message is very long.
