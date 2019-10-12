"""Executors objects. Provide a channel of communication with binaries, either
locally running or remotely"""
from socket import socket


class Remote(object):
    def __init__(self, host, port, line_sep=b'\n', read_size=4096):
        """
        Args:
            host: domain name or ip adress to connect to
            port: port number to use
            line_sep: the line separator to use while reading stream (e.g reading lines separatly)
            read_size: the max number of bytes to get for each read operation
        """

        self.host = host
        self.port = port
        self.line_sep = line_sep
        self.read_size = read_size
        self._buffer = b''
        self.connect()

    def connect(self):
        self._socket = socket()
        self._socket.connect((self.host, self.port))

    def _recv(self):
        self._buffer += self._socket.recv(self.read_size)

    def _send(self, to_send):
        return self._socket.send(to_send)

    def recvline(self):
        """Read a line from the input stream using line_sep as line separator"""

        # Read till end of line
        while self.line_sep not in self._buffer:
            self._recv()
        return self._recvline()

    def _recvline(self):
        """Only get the first line from the buffer, should only be called from
        readline as this last one make sure there is a line in the buffer."""

        idx = self._buffer.find(self.line_sep)
        line = self._buffer[:idx]
        self._buffer = self._buffer[idx+1:]
        return line

    def sendline(self, to_send):
        to_send += self.line_sep
        return self._send(to_send)
