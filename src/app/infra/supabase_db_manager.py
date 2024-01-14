from typing import List
from src.app.core.interfaces.db_manager import IDataBaseManager
from src.app.core.models.operation import Operation
from supabase import Client as SupabaseClient


class SupabaseDBManager(IDataBaseManager):
    """_Saves data to Supabase DB_

    """

    def __init__(self, supabase: SupabaseClient):
        super().__init__(supabase)

    def save(self, operation: Operation) -> None:
        self.supabase.table('operations').insert(
            {"input": operation.input, "output": operation.output}).execute()

    def get_all(self) -> List[dict]:
        response = self.supabase.table('operations').select("*").execute()
        return response.data
