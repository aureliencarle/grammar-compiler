"""AllReader class"""

from typing import List, Optional

from .binaryfile import BinaryFile
from .base_reader import BaseReader


class AllReader(BaseReader):
    """
    Reader that reads all element in a list (all patterns must match).
    """

    def __init__(
        self,
        readers: List[BaseReader]
    ):
        super().__init__()
        self.readers = readers

    def __call__(
        self,
        file: BinaryFile
    ) -> Optional[List[str]]:
        res = []
        with file.safe_pos():
            for reader in self.readers:
                pattern = reader(file)
                if pattern is None:
                    res = None
                    raise(BinaryFile.MissReadError)
                res.append(pattern)
        return res
