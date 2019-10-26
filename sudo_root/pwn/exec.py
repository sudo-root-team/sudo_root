"""Executors objects. Provide a channel of communication with binaries, either
locally running or remotely"""
from socket import socket
from subprocess import Popen, PIPE, STDOUT


class Executor(object):
    """Interface of communication with remote or local binaries.
    Classes that inherit from this should reimplement the connect, _recv
    and _send methods.
    """
    def __init__(self, line_sep=b'\n', read_size=4096):
        """
        Args:
            line_sep: the line separator to use while reading stream
            read_size: the max number of bytes to get for each read operation
        """
        self.line_sep = line_sep
        self.read_size = read_size
        self._buffer = b''
        self.connect()

    def connect(self):
        raise NotImplementedError()

    def _recv(self):
        raise NotImplementedError()

    def _send(self, to_send):
        raise NotImplementedError()

    def recvline(self):
        """Read a line from the input stream using line_sep as line separator.
        """
        # Read till end of line
        while self.line_sep not in self._buffer:
            self._recv()
        return self._recvline()

    def _recvline(self):
        """Only get the first line from the buffer, should only be called from
        readline as this last one make sure there is a line in the buffer.
        """
        idx = self._buffer.find(self.line_sep)
        line = self._buffer[:idx]
        # +1 for the jumping the '\n'
        self._buffer = self._buffer[idx + 1:]
        return line

    def sendline(self, to_send):
        to_send += self.line_sep
        return self._send(to_send)

    def recv(self, n_bytes):
        """Read the exact number of bytes from the socket."""
        if n_bytes < 0:
            return b''
        # fill with already buffered data
        buffer = self._buffer[:n_bytes]
        self._buffer = self._buffer[n_bytes:]
        # get remaining bytes from the socket if needed
        while len(buffer) < n_bytes:
            to_read = n_bytes - len(buffer)
            self._recv()
            buffer += self._buffer[:to_read]
            self._buffer = self._buffer[to_read:]
        return buffer

    def send(self, to_send):
        return self._send(to_send)


class Remote(Executor):
    """Provide a communication channel with remote services.
    """
    def __init__(self, host, port, **kwargs):
        """
        Args:
            host: domain name or ip adress to connect to
            port: port number to use
        """

        self.host = host
        self.port = port
        self._socket = None
        super().__init__(**kwargs)

    def connect(self):
        # close socket and empty buffer if connecting again
        if self._socket:
            self._socket.close()
            self._buffer = b''
        self._socket = socket()
        self._socket.connect((self.host, self.port))

    def _recv(self):
        self._buffer += self._socket.recv(self.read_size)

    def _send(self, to_send):
        return self._socket.send(to_send)


class Local(Executor):
    """Provide a communication channel with a local process. It takes care
    of executing the process.
    """
    def __init__(self, binary_path, args=[], read_size=1, **kwargs):
        """
        Args:
            binary_path: path of the binary to execute
            args: arguments to pass while executing the binary
        """
        self.binary_path = binary_path
        self.args = args
        self._process = None
        super().__init__(read_size=read_size, **kwargs)

    def connect(self):
        """Create and the process and setup the communication channel.
        STDOUT and STDERR are merged together.
        """
        # kill the process and empty buffer if creating a new one
        if self._process:
            self._process.kill()
            self._buffer = b''

        cmd = [self.binary_path, *self.args]
        self._process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        self._stdin = self._process.stdin
        self._stdout = self._process.stdout

    def _recv(self):
        self._buffer += self._stdout.read(self.read_size)

    def _send(self, to_send):
        count = self._stdin.write(to_send)
        self._stdin.flush()
        return count
