from functools import lru_cache
from fastapi import FastAPI, Depends, HTTPException

from .settings import Settings, supabase
from .schemas import CsvResponse, OperationPayload, OperationResponse
from ..core.models.operation import Operation
from ..core.interfaces.calculator import ICalculator

settings = Settings()
"""_Gets settings needed to instantiate calculator_"""


@lru_cache
def get_calculator() -> ICalculator:
    """_Instantiates and returns instance of calculator from lru_cache_
    """
    db_manager = settings.providers.get('db_manager').get('class')(supabase)
    file_manager = settings.providers.get('file_manager').get('class')()
    calculator = settings.providers.get('calculator').get('class')
    return calculator(db_manager, file_manager)


app = FastAPI()


@app.post("/calculate", response_model=OperationResponse)
def calculate_operation(payload: OperationPayload,
                        calc: ICalculator = Depends(get_calculator)):
    """_Api method, returns a calculated operation_
    """
    try:
        result: Operation = calc.calculate(Operation(payload.input))
        calc.save_calculation(result)
        return result
    except (ZeroDivisionError, IndexError):
        raise HTTPException(status_code=422)


@app.get("/operations", response_class=CsvResponse)
def get_operations(calc: ICalculator = Depends(get_calculator)):
    """_Api method, returns the list of calculated operations_

    """
    data: str = calc.get_calculations_csv_file()
    response = CsvResponse(iter([data]))
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    return response
