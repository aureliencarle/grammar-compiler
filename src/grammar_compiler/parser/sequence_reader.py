"""SequenceReader class"""

from typing import List

from .binaryfile import BinaryFile
from .base_reader import BaseReader


class SequenceReader(BaseReader):
    """
    Readers that reads 0 to N similar elements. As it can read 0 elements,
    the reader should never return None (empty list if 0 elements).
    """

    def __init__(
        self,
        reader: BaseReader
    ):
        super().__init__()
        self.reader = reader

    def __call__(
        self,
        file: BinaryFile
    ) -> List[str]:
        res = []
        end_sequence = False
        while not end_sequence:
            with file.safe_pos():
                token = self.reader(file)
                if token is not None:
                    res.append(token)
                else:
                    end_sequence = True
                    raise(BinaryFile.MissReadError)
        return res
