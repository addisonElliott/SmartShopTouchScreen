import queue
import select
import socket
import sys
import struct
import json

class SocketData():
    __slots__ = ['writeQueue', 'readBufLen', 'readBuf', 'IP']
    def __init__(self, writeQueue = None, readBufLen = -1, readBuf = None, IP = None):
        # writeQueue - A queue of data to be sent when a chance is available
        # readBufLen - Length of the packet size
        # readBuf - Contains the data read from the socket.
        # IP - IP of the socket
        self.writeQueue = writeQueue
        self.readBufLen = readBufLen
        self.readBuf = readBuf
        self.IP = IP

class TcpServer:
    def __init__(self, host=None, port=None, readCallback=None, maxConnections=10, recvBlockSize=4096, connectNow = True):
        # Handle the socket's host. If the host is set to special value of public, then it is directed to (0.0.0.0)
        if host == "public":
            self.host = socket.gethostname()
        else:
            self.host = host

        self.port = port
        if port is not None and type(self.port) is not int:
            raise ValueError("Port must be an integer %r" % (self.port))

        self.readCallback = readCallback
        self.maxConnections = maxConnections
        if type(self.maxConnections) is not int:
            raise ValueError("Maximum number of connections (maxConnections) must be an integer %r" %
                             (self.maxConnections))

        self.recvBlockSize = recvBlockSize
        if type(self.recvBlockSize) is not int:
            raise ValueError("recvBlockSize must be an integer %r" % (self.recvBlockSize))

        # Initialize the readers and writers variable which contains a list of sockets that are queued for reading or
        # writing by select function
        self.readers = []
        self.writers = []

        # Initialize socket data dictionary which contains information for each socket connected
        self.socketData = {}

        print('Successfully initialized the TcpServer')
        if host and port and connectNow:
            self.start()
            print('Given host and port, attempting to connect')

    def start(self):
        # Create the socket, INET, streaming. Set it to non blocking and bind it to the given host and port
        # Listen for connections (maximum amount being maxConnections)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.maxConnections)

        # Append socket to the readers list
        self.readers.append(self.socket)

    def send(self, IP, message):
        # Loop through each IP in IPs dictionary, get the sock associated with the IP
        sock_ = None
        for sock, IP_ in self.IPs:
            if IP_ is IP:
                sock_ = sock

        # If no socket found, then throw an error
        if sock_ is None:
            raise ValueError("Invalid socket to send data to, IP: %s" % (IP))

        # Append the message to the socket's queue and put it in the writers list if not already present
        self.socketData[sock_].writeQueue.put(message)
        if sock_ not in self.writers:
            self.writers.append(sock_)

    def run(self):
        # Select what sockets are available to read from readers (as well as any read errors) and what sockets to write
        # with writers. Set timeout to zero so that if nothing is available for reading or writing, then just return
        read, write, err = select.select(self.readers, self.writers, self.readers, 0)

        # Loop through each available socket for reading
        for sock in read:
            print("Sockets to be read")
            if sock is self.socket:
                # If the socket available for reading is the server socket, then a new connection is available,
                # accept the new connection, set it to nonblocking
                # Add its socket data to the socketData list
                clientSocket, clientIP = self.socket.accept()
                clientSocket.setblocking(0)
                self.readers.append(clientSocket)
                self.socketData[clientSocket] = SocketData(queue.Queue(), -1, b'', clientIP)
                print("New connection accepted %s" % (str(clientIP)))
            else:
                # Otherwise, one of the clients sent data to the server to be processed
                data = sock.recv(self.recvBlockSize)
                print(data)
                if data:
                    socketData = self.socketData[sock]
                    socketData.readBuf += data

                    if socketData.readBufLen == -1 and len(socketData.readBuf) >= 2:
                        socketData.readBufLen = struct.unpack(">H", socketData.readBuf[:2])[0]
                        socketData.readBuf = socketData.readBuf[2:]
                        #print ('New data: %s, size: %i' % (socketData.readBuf.decode(encoding='UTF-8'), socketData.readBufLen))

                    if socketData.readBufLen != -1 and len(socketData.readBuf) >= socketData.readBufLen:
                        packet = socketData.readBuf[:socketData.readBufLen].decode(encoding='UTF-8')
                        jsonData = json.loads(packet)
                        print('New data2: %s at size %i: %s %i' % (packet, socketData.readBufLen, str(jsonData), jsonData['EID']))
                        socketData.readBuf = socketData.readBuf[socketData.readBufLen:]
                        socketData.readBufLen = -1

                        if self.readCallback:
                            self.readCallback(self.socketData[sock], jsonData)
                else:
                    # We received zero bytes, so we should close the stream. Stop writing to it.
                    if sock in self.writers:
                        self.writers.remove(sock)

                    self.readers.remove(sock)

                    # Close the connection.
                    sock.close()

                    # Get rid of the socket data
                    del self.socketData[sock]
                    print("Socket connection closed!")

        # Loop through each available socket for writing
        for sock in write:
            try:
                # Get the next chunk of data in the queue, but don't wait.
                data = self.socketData[sock].writeQueue.get_nowait()
            except queue.Empty:
                # The queue is empty -> nothing needs to be written, remove it from writers list
                self.writers.remove(sock)
                print("Removed writer from queue now")
            else:
                # The queue wasn't empty; we did, in fact, get something. So send it.
                sock.send(data)
                print("Wrote data %d: %s" % (len(data), data))

        # Loop through each available socket for errors
        for sock in err:
            # Remove the socket from every list.
            self.readers.remove(sock)
            if sock in self.writers:
                self.writers.remove(sock)

            # Close the connection.
            sock.close()

            # Destroy the socket data
            del self.socketData[sock]
            print("Error occurred. Closing socket")
