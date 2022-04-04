"""CharacterReader class"""

from typing import Optional, Callable

from .binaryfile import BinaryFile
from .base_reader import BaseReader


class CharacterReader(BaseReader):
    """
    Reader that reads one character that matches a condition.
    """

    def __init__(
        self,
        predicate: Callable[str, bool]
    ):
        super().__init__()
        self.predicate = predicate

    def __call__(
        self,
        file: BinaryFile
    ) -> Optional[str]:
        with file.safe_pos():
            res = file.read(1)
            if res is None or not self.predicate(res):
                raise(BinaryFile.MissReadError)
        return res
