# pysockets
Python and groovy scripts using sockets to establish the communication between master client and slave server.

Message format:
```
[x]xxxxxxxxxxx\n
```
* [s]: Run akquiltsync, copy patched to github repo, and update debt report.
* [r]: Message with content of change report
* [t]: Message echo for testing
* [d]: Everthing is done. After receiving this message, the slave server will send a "Done" message to master client and close the connection. Server will be still running and waiting for new connection. Master client will be closed after receiving this message.
* \n: endMark, the special string marks the end of the message.

Function 'msgmapping' will map the message to different function based on the first 3 characters of message: [x]

## Usage

slave-socket-server.py : receives the message from master client and perform the corresponding scripts on slave machine.
```
python slave-socket-server.py 
```
groovy-master/master-send.gy: interfactive interface of master client written with Groovy
```
groovy master-send.gy
```
master-send.py: interactive interface of master client written with Python
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

## Known issues
1. endMark = '\n'. Slave server will assume the message is over when it sees endMark. If endMark appreas in the middle of message, the message will be truncated.
2. Message will be process after all of it is recieved. It garantees the compleness of message received, but would cosume more space if the message is very long.
3. If message without endMark is received by slave server, the server will think the message is not complete and wait forever.

## Todo
1. Complete the function to generate change report
2. Integrate the groovy code into Jenkins
3. Complete the function to check if sha1 has been synced


