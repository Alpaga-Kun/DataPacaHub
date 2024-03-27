import sqlite3


class DatabaseTools:
    def __init__(self, db_name="default_db.sqlite"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)

    def infer_data_types(self, df):
        """Infers SQL data types from a pandas DataFrame."""
        type_mapping = {
            'object': 'VARCHAR(255)',
            'int64': 'INTEGER',
            'float64': 'REAL',
            'datetime64[ns]': 'DATE',
            'bool': 'BOOLEAN'
        }
        column_types = {}
        for column, dtype in df.dtypes.items():
            sql_type = type_mapping.get(str(dtype), 'TEXT')
            column_types[column] = sql_type
        return column_types

    def create_table_from_df(self, df, table_name):
        """Creates a SQL table from a pandas DataFrame structure."""
        column_types = self.infer_data_types(df)
        columns_with_types = [f"{col} {dtype}" for col,
                              dtype in column_types.items()]
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_with_types)});"
        cursor = self.connection.cursor()
        cursor.execute(create_table_query)
        self.connection.commit()

    def verify_table_creation(self, table_name):
        """Verifies that a table exists in the database."""
        cursor = self.connection.cursor()
        cursor.execute(
            f'SELECT name FROM sqlite_master WHERE type="table" AND name="{table_name}";')
        return cursor.fetchone() is not None

    def close_connection(self):
        """Closes the database connection."""
        self.connection.close()
