from typing import List
from src.app.core.interfaces.file_manager import IFileManager
from src.app.core.models.operation import Operation
import pandas as pd


class CsvFileManager(IFileManager):
    """_Output csv from data_

    """

    def get_file_from_data(self, operations: List[Operation]) -> str:
        df = pd.DataFrame(operations)
        return df.to_csv(index=False)
