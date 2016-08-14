# pysockets
Py scripts using sockets to establish the communication between master client and slave server.

Message format:
```
[x]xxxxxxxxxxx$
```

.. Function 'msgmapping' will map the message to different function based on the first 3 characters of message: [x]

Server script thinks the message is over when catches'$' at the end.
## usage
slave-socket-server.py : receives the message from master client and perform the corresponding scripts on slave machine.
```
python slave-socket-server.py 
```
master-socket-client-send,py: sends message to slave server
```
python master-socket-client
```
.. send default message defined in the script

```
python master-socket-client-send.py <msg>
```
.. send customized message

```
python master-socket-client-send.py -f <path2file/file>
```
.. read message from file and send message 

## issues
1. endMark = '$'. Assuming there's no'$' inside the message
