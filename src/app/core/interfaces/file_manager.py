
from abc import ABC, abstractmethod
from typing import List
from ..models.operation import Operation


class IFileManager(ABC):
    @abstractmethod
    def get_file_from_data(self, operations: List[Operation]) -> str:
        raise NotImplementedError
