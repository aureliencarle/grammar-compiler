"""AnyReader class"""

from typing import List, Optional

from .binaryfile import BinaryFile
from .base_reader import BaseReader


class AnyReader(BaseReader):
    """
    Reader that reads any element in a list (first pattern that matches).
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
    ) -> Optional[str]:
        res = None
        for reader in self.readers:
            res = reader(file)
            if res:
                break
        return res
