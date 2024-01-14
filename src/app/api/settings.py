import sys
import os
from importlib import import_module
from supabase import create_client, Client as SupabaseClient
from pydantic_settings import BaseSettings

CALC_MODULE = 'core.calculator'
CALC_CLASS = 'Calculator'

DB_MNGR_MODULE = 'infra.supabase_db_manager'
DB_CLASS = 'SupabaseDBManager'

FILE_MNGR_MODULE = 'infra.csv_file_manager'
FILE_CLASS = 'CsvFileManager'

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")
supabase: SupabaseClient = create_client(url, key)
"""_supabase client, I need to explore dependency injection libs_
"""


class Settings(BaseSettings):
    app_name: str = "FastAPI RPN Calculator"

    providers: dict = {
        "calculator": {"class": getattr(import_module(CALC_MODULE),
                                        CALC_CLASS)},
        "db_manager": {"class": getattr(import_module(DB_MNGR_MODULE),
                                        DB_CLASS)},
        "file_manager": {"class": getattr(import_module(FILE_MNGR_MODULE),
                                          FILE_CLASS)},
    }
    """_base for a custom dependency injection_
    """
