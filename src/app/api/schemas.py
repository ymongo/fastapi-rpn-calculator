
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated
from pydantic import BaseModel, Field, field_validator
from typing import List
import re
from ..core.models.operation import Operation


OperatorOrOperand = Annotated[str, Field(pattern=r'(-?[1-9]\d*|0|\+|\*|\/|-)')]


class OperationPayload(BaseModel):
    input: List[OperatorOrOperand]

    @field_validator('input')
    @classmethod
    def minimal_working_operation(
            cls, value: List[OperatorOrOperand]) -> List[OperatorOrOperand]:
        if len(value) < 3:
            raise ValueError('input list must have at least 3 items')
        elif len(value) == 3:
            operand_pattern = r'(-?[1-9]\d*|0)'
            if (not re.match(operand_pattern, value[0])
                    or not re.match(operand_pattern, value[1])):
                raise ValueError('input must have at least 2 operands')
            if not re.match(r'[\+\*\/-]?', value[2]):
                raise ValueError('input must have at least 1 operator')
        return value


class OperationResponse(Operation, BaseModel):
    pass


class CsvResponse(StreamingResponse):
    media_type = "text/csv"
