# from struct import pack, unpack
# from sys import getsizeof as sizeof

from socket import socket
from pickle import dumps, loads
from .message import Message


class Channel:
    """
    A Message class that sends and recieves data
    by pre-calculating the size of the data to be recieved
    so that there are no overloads or packet losses
    """

    def __init__(self, conn: socket):
        self.conn = conn

    def send(self, data: Message):
        """
        First sends the size of the data using struct's pack()
        then the data itself
        """
        self.conn.send(dumps(data))

        # data_encoded = dumps(data)
        # bufsize = pack("!i", sizeof(data_encoded))
        # self.conn.send(bufsize)
        # self.conn.send(data_encoded)

    def recv(self) -> Message:
        """
        A recv_all type method that
        ensures that there is no data loss
        """

        return loads(self.conn.recv(2048))
        # bufsize = unpack("!i", self.conn.recv(100))[
        #     0
        # ]  # 37 seems to be the size of a packed `int`
        # data = loads(self.conn.recv(bufsize))
        # return data

    def close(self):
        self.conn.close()
