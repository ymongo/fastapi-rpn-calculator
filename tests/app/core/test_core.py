import pytest
from unittest.mock import Mock, patch
from src.app.core.models.operation import Operation
from src.app.core.interfaces.file_manager import IFileManager
from src.app.core.interfaces.db_manager import IDataBaseManager
from src.app.core.calculator import Calculator


class TestCalculator:
    @pytest.fixture
    def mock_db_manager(self):
        mock = Mock(spec=IDataBaseManager)
        return mock

    @pytest.fixture
    def mock_file_manager(self):
        mock = Mock(spec=IFileManager)
        return mock

    @patch('src.app.core.calculator.super')
    def test_init_should_call_super(self, mock_super,
                                    mock_db_manager, mock_file_manager):
        # When
        Calculator(mock_db_manager, mock_file_manager)

        # Then
        assert mock_super.called

    def test_eval_rpn_calculates_properly(self, mock_db_manager,
                                          mock_file_manager):
        # Given
        calc = Calculator(mock_db_manager, mock_file_manager)
        operation_token_list = ["3", "2", "+"]
        expected_result = 5

        # When
        result = calc.eval_rpn(operation_token_list)

        # Then
        assert result == expected_result

    def test_eval_rpn_raise_zero_error_if_division_by_zero(self,
                                                           mock_db_manager,
                                                           mock_file_manager):
        # Given
        calc = Calculator(mock_db_manager, mock_file_manager)
        operation_token_list = ["2", "0", "/"]

        # When
        with pytest.raises(ZeroDivisionError):
            calc.eval_rpn(operation_token_list)

    def test_eval_rpn_raise_index_error_if_out_of_operands(self,
                                                           mock_db_manager,
                                                           mock_file_manager):
        # Given
        calc = Calculator(mock_db_manager, mock_file_manager)
        operation_token_list = ["2", "3", "/", "-"]

        # When
        with pytest.raises(IndexError):
            calc.eval_rpn(operation_token_list)

    @patch('src.app.core.calculator.Calculator.eval_rpn')
    def test_calculate_calls_eval_rpn(self, mock_eval,
                                      mock_db_manager,
                                      mock_file_manager):
        # Given
        calc = Calculator(mock_db_manager, mock_file_manager)
        operation_token_list = ["2", "3", "+"]
        expected_result = 5
        mock_eval.return_value = expected_result
        operation = Operation(operation_token_list)

        # When
        operation.output = calc.calculate(operation)

        # Then
        assert mock_eval.called

    def test_save_calculation_calls_db_save(self,
                                            mock_db_manager,
                                            mock_file_manager):
        # Given
        calc = Calculator(mock_db_manager, mock_file_manager)
        operation_token_list = ["2", "3", "+"]

        operation = Operation(operation_token_list)

        # When
        calc.save_calculation(operation)

        # Then
        assert mock_db_manager.save.called

    def test_get_calculations_csv_file_calls_db_and_file_mngrs(
            self,
            mock_db_manager,
            mock_file_manager):

        # Given
        calc = Calculator(mock_db_manager, mock_file_manager)

        # When
        calc.get_calculations_csv_file()

        # Then
        assert mock_db_manager.get_all.called
        assert mock_file_manager.get_file_from_data.called
