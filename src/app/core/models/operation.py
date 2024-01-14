from typing import List


class Operation():
    """_App core object. input is the operation, output the result_
    """
    input: List[str]
    output: int

    def __init__(self, input: str, output: int = None):
        self.input = input
        self.output = output

    def __repr__(self):
        return str({"input":  self.input, "output":  self.output})
