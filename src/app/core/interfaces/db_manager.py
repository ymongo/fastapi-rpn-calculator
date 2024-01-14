from abc import ABC, abstractmethod
from typing import List
from ..models.operation import Operation
from supabase import Client as SupabaseClient


class IDataBaseManager(ABC):

    @abstractmethod
    def __init__(self, supabase: SupabaseClient):
        self.supabase = supabase

    @abstractmethod
    def save(self, operation: Operation) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Operation]:
        raise NotImplementedError
