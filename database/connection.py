from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

from config import CONNECTION_STRING


engine = create_engine(
    "mssql+pyodbc:///?odbc_connect="
    + quote_plus(CONNECTION_STRING)
)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT DB_NAME()")
            )

            database_name = result.scalar()

        return True, database_name

    except Exception as e:
        return False, str(e)