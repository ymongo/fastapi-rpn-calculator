from abc import ABC, abstractmethod
from typing import List
from .db_manager import IDataBaseManager
from .file_manager import IFileManager
from ..models.operation import Operation


class ICalculator(ABC):

    @abstractmethod
    def __init__(self, db_manager: IDataBaseManager,
                 file_manager: IFileManager):
        self.db_manager = db_manager
        self.file_manager = file_manager

    @abstractmethod
    def eval_rpn(self, tokens: List[str]) -> int:
        raise NotImplementedError

    @abstractmethod
    def calculate(self, operation: Operation) -> Operation:
        raise NotImplementedError

    @abstractmethod
    def save_calculation(self, operation: Operation) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_calculations_csv_file(self) -> str:
        raise NotImplementedError
