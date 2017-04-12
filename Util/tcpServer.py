import queue
import select
import socket
import sys


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

        # Initialize queues and IPs, a dict containing entries for each client socket that represents the following:
        # queues - A queue of data to be sent when a chance is available
        # IPs - IP of the client socket
        self.queues = {}
        self.IPs = {}

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
        self.queues[sock_].put(message)
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
                # accept the new connection, set it to nonblocking and add to appropiate lists
                clientSocket, clientIP = self.socket.accept()
                clientSocket.setblocking(0)
                self.readers.append(clientSocket)
                self.queues[clientSocket] = queue.Queue()
                self.IPs[clientSocket] = clientIP
                print("New connection accepted %s" % (str(clientIP)))
            else:
                # Otherwise, one of the clients sent data to the server to be processed
                data = sock.recv(self.recvBlockSize)
                if data:
                    # If the received data is valid (basically, length > 0), then call callback and let it handle it

                    if self.readCallback:
                        self.readCallback(self.IPs[sock], self.queues[sock], data)
                    print("Valid data read %d: %s" % (len(data), data))
                else:
                    # We received zero bytes, so we should close the stream. Stop writing to it.
                    if sock in self.writers:
                        self.writers.remove(sock)

                    self.readers.remove(sock)

                    # Close the connection.
                    sock.close()

                    # Destroy is queue
                    del self.queues[sock]
                    del self.IPs[sock]
                    print("Socket connection closed!")

        # Loop through each available socket for writing
        for sock in write:
            try:
                # Get the next chunk of data in the queue, but don't wait.
                data = self.queues[sock].get_nowait()
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

            # Destroy its queue and IP information
            del self.queues[sock]
            del self.IPs[sock]
            print("Error occurred. Closing socket")
    #
    # def run(self):
    #     # Start listening
    #     self._socket.listen(self._max_connections)
    #     # Create a list of readers (sockets that will be read from) and a list
    #     # of writers (sockets that will be written to).
    #     readers = [self._socket]
    #     writers = []
    #     # Create a dictionary of queue.Queues for data to be sent.
    #     # This dictionary maps sockets to queue.Queue objects
    #     queues = dict()
    #     # Create a similar dictionary that stores IP addresses.
    #     # This dictionary maps sockets to IP addresses
    #     IPs = dict()
    #     # Now, the main loop.
    #     while readers:
    #         # Block until a socket is ready for processing.
    #         read, write, err = select.select(readers, writers, readers)
    #         # Deal with sockets that need to be read from.
    #         for sock in read:
    #             if sock is self._socket:
    #                 # We have a viable connection!
    #                 client_socket, client_ip = self._socket.accept()
    #                 # Make it a non-blocking connection.
    #                 client_socket.setblocking(0)
    #                 # Add it to our readers.
    #                 readers.append(client_socket)
    #                 # Make a queue for it.
    #                 queues[client_socket] = queue.Queue()
    #                 # Store its IP address.
    #                 IPs[client_socket] = client_ip
    #             else:
    #                 # Someone sent us something! Let's receive it.
    #                 data = sock.recv(self.recv_bytes)
    #                 if data:
    #                     # Call the callback
    #                     self.callback(IPs[sock], queues[sock], data)
    #                     # Put the client socket in writers so we can write to it
    #                     # later.
    #                     if sock not in writers:
    #                         writers.append(sock)
    #                 else:
    #                     # We received zero bytes, so we should close the stream
    #                     # Stop writing to it.
    #                     if sock in writers:
    #                         writers.remove(sock)
    #                     # Stop reading from it.
    #                     readers.remove(sock)
    #                     # Close the connection.
    #                     sock.close()
    #                     # Destroy is queue
    #                     del queues[sock]
    #         # Deal with sockets that need to be written to.
    #         for sock in write:
    #             try:
    #                 # Get the next chunk of data in the queue, but don't wait.
    #                 data = queues[sock].get_nowait()
    #             except queue.Empty:
    #                 # The queue is empty -> nothing needs to be written.
    #                 writers.remove(sock)
    #             else:
    #                 # The queue wasn't empty; we did, in fact, get something.
    #                 # So send it.
    #                 sock.send(data)
    #         # Deal with erroring sockets.
    #         for sock in err:
    #             # Remove the socket from every list.
    #             readers.remove(sock)
    #             if sock in writers:
    #                 writers.remove(sock)
    #             # Close the connection.
    #             sock.close()
    #             # Destroy its queue.
    #             del queues[sock]
