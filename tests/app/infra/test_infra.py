import pytest
from unittest.mock import Mock, patch
from supabase import Client as SupabaseClient
from src.app.infra.supabase_db_manager import SupabaseDBManager
from src.app.core.models.operation import Operation
from src.app.infra.csv_file_manager import CsvFileManager


class TestCsvFileManager:

    def test_get_file_from_data_should_return_data_as_csv_string(self):
        # Given
        csv_file_manager = CsvFileManager()
        operations = [
            Operation(["3", "2", "+"], 5),
            Operation(["3", "2", "-"], 1)
        ]
        expected = '0\n"{\'input\': [\'3\', \'2\', \'+\'], \'output\': 5}"\n"{\'input\': [\'3\', \'2\', \'-\'], \'output\': 1}"\n'

        # When
        result = csv_file_manager.get_file_from_data(operations)

        # Then
        assert result == expected


class TestSupabaseDBManager:

    @pytest.fixture
    def mock_supabase(self):
        mock = Mock(spec=SupabaseClient)
        return mock

    @patch('src.app.infra.supabase_db_manager.super')
    def test_init_should_call_super(self, mock_super, mock_supabase):
        # When
        SupabaseDBManager(mock_supabase)

        # Then
        assert mock_super.called

    def test_save_should_call_db_insert(self, mock_supabase):
        # Given
        db_mngr = SupabaseDBManager(mock_supabase)
        operation = Operation(["3", "2", "+"], 5)

        # When
        db_mngr.save(operation)

        # Then
        assert mock_supabase.table('operations').insert.called

    def test_get_all_should_call_db_select_and_return_data(self,
                                                           mock_supabase):
        # Given
        db_mngr = SupabaseDBManager(mock_supabase)

        # When
        db_mngr.get_all()

        # Then
        assert mock_supabase.table('operations').select.called
