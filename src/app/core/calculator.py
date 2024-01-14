from typing import List
from .interfaces.calculator import ICalculator
from .interfaces.db_manager import IDataBaseManager
from .interfaces.file_manager import IFileManager
from .models.operation import Operation


class Calculator(ICalculator):
    """_App core class, makes the calculations and returns data_
    """

    def __init__(self, db_manager: IDataBaseManager,
                 file_manager: IFileManager):
        super().__init__(db_manager, file_manager)

    def eval_rpn(self, tokens: List[str]) -> int:
        """_RPN algorithm_

        Args:
            tokens (List[str]): _RPN operation as a list\
                 of operands and operators_

        Returns:
            int: _RPN operation result_
        """
        stack = []
        for token in tokens:
            if token in "+-*/":
                right, left = stack.pop(), stack.pop()
                if token == "+":
                    stack.append(left+right)
                elif token == "-":
                    stack.append(left-right)
                elif token == "*":
                    stack.append(left*right)
                elif token == "/":
                    stack.append(int(left/right))
            else:
                stack.append(int(token))
        return stack.pop()

    def calculate(self, operation: Operation) -> Operation:
        """_Calls the RPN algo, returns a Operation object with output_

        Args:
            operation (Operation): _Operation object to calculate_

        Returns:
            Operation: _Operation object updated with result_
        """
        operation.output = self.eval_rpn(operation.input)
        return operation

    def save_calculation(self, operation: Operation) -> None:
        """_Calls db to save operation_

        Args:
            operation (Operation): _Operation object to save_
        """
        self.db_manager.save(operation)

    def get_calculations_csv_file(self) -> str:
        """_Calls db to get all operations, returns csv string_

        Returns:
            str: _operations as csv string_
        """
        ops = self.db_manager.get_all()
        return self.file_manager.get_file_from_data(ops)
