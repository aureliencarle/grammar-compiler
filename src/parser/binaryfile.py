"""Contains the BinaryFile class"""


class BinaryFile:
    """Manage read/write operations for files in binary mode"""

    encoding = 'utf-8'

    def __init__(
        self,
        filename: str,
        mode: str
    ):
        self.filename = filename
        self.mode = self._get_mode(mode)
        self._file = None

    @property
    def pos(self):
        """Current cursor position in the file"""
        return self._file.tell()

    @pos.setter
    def pos(self, value):
        """Sets the cursor position in the file"""
        self._file.seek(value, 0)

    @staticmethod
    def _get_mode(mode: str):
        return (mode + 'b' if ('b' not in mode)
                else mode)

    def read(self, *args):
        return self._file.read(*args).decode(self.encoding)

    def readline(self, *args):
        return self._file.readline(*args).decode(self.encoding)

    def write(self, line: str):
        return self._file.write(line.encode(self.encoding))

    def move_cursor_left(
        self,
        delta: int
    ):
        self._file.seek(-delta, 1)

    def move_cursor_right(
        self,
        delta: int
    ):
        self._file.seek(+delta, 1)

    def __enter__(self):
        self._file = open(self.filename, self.mode)
        return self

    def __exit__(self, *args):
        if self._file:
            self._file.close()
