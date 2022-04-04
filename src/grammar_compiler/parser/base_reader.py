"""BaseReader abstract class"""

import abc
from typing import Optional, Any

from .binaryfile import BinaryFile


class BaseReader(metaclass=abc.ABCMeta):
    """
    Base class for a reader. The __call__ function is abstract
    and must be implemented in derived classes.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def __call__(
        self,
        file: BinaryFile
    ) -> Optional[Any]:
        pass
