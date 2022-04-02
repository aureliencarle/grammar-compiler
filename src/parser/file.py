class File:

    def __init__(
        self,
        filename: str,
        mode: str
    ):
        self.filename = filename
        self.mode = mode
        self._file = None

    def read(self, *args):
        return self._file.read(*args)

    def write(self, *args):
        return self._file.write(*args)

    def move_cursor_left(
        self,
        delta: int
    ):
        self._file.seek(1, -delta)

    def move_cursor_right(
        self,
        delta: int
    ):
        self._file.seek(1, +delta)

    def __enter__(self):
        self._file = open(self.filename, self.mode)

    def __exit__(self, *args):
        if self._file:
            self._file.close()
