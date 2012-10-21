#
# Client.py
#
# Created on: October 14, 2012
#     Author: Todd Lunter
#

import socket
import Queue
import threading
from IRC.Message import Message
from IRC.Exceptions import LockError, MessageSendError

class ClientReceiver(threading.Thread):
    def __init__(self, socket, msg_queue, running):
        """Inits a Client Receiver with a socket and msg_queue"""
        threading.Thread.__init__(self)

        self.socket = socket
        self.msg_queue = msg_queue
        self.running = running
    
    def run(self):
        """Receives a message from the socketted IRC server and calls it to a function"""

        partial_msg = ""

        while self.running.is_set():
            chunk = self.socket.recv(1024)
            
            partial_msg += chunk
            raw_msgs = partial_msg.split('\r\n')
            partial_msg = raw_msgs[-1]

            for raw_msg in raw_msgs[:-1]:
                msg = Message.from_string(raw_msg)

                self.msg_queue.put(msg)

class Client(object):
    """
    Implements the necessary input and output for a socketted IRC connection

    Attributes:
        `socket`: Socket layer that the server connects through
        `address`: Address for the server to connect to
        `port`: Port for the server to connect to
        `msg_queue`: Queue to store all messages received from the IRC server
    """

    def __init__(self, address, port):
        """Inits an IRC Client with the given address and port"""
        
        self.address = address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msg_queue = Queue.Queue()

        self.running = threading.Event()

    def __repr__(self):
        return "Client(%r, %r)" % (self.address, self.port)

    def __eq__(self, other):
        return self.address == other.address and self.port == other.port

    def __hash__(self):
        hashables = (self.address, self.port)

        result = 0
        for value in hashables:
            result = 33*result + hash(value)
        return hash(result)

    def start(self):
        """Initiates a receiving thread and gives it a lock"""
        self.socket.connect((str(self.address), int(self.port)))
        
        self.running.set()

        recv_thread = ClientReceiver(self.socket, self.msg_queue, self.running)
        recv_thread.start()

    def send(self, msg):
        """Sends a message to the socketted IRC server assuming it is connected"""
        raw_msg = msg.to_raw()

        bytes_sent = 0
        while bytes_sent < len(raw_msg):
            bytes_sent += self.socket.send(raw_msg[bytes_sent:])
            if bytes_sent == 0:
                raise MessageSendError()

