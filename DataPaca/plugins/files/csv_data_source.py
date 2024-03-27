import os
import pandas as pd
from utils.data_loading import DatabaseTools
from etl.plugin_interface import ExtractInterface, TransformInterface, LoadInterface
from sqlalchemy import create_engine


class CSVDataSource(ExtractInterface):
    def __init__(self, filename: str, delimiter=',', encoding='utf-8') -> None:
        self.filename = filename
        self.delimiter = delimiter
        self.encoding = encoding

        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"File {self.filename} not found.")
        if not os.access(self.filename, os.R_OK):
            raise PermissionError(f"File {self.filename} is not readable.")
        if not os.access(self.filename, os.W_OK):
            raise PermissionError(f"File {self.filename} is not writable.")

        df = pd.read_csv(self.filename)
        if df.shape[0] == 0:
            raise ValueError(f"File {self.filename} is empty.")
        if df.shape[1] == 0:
            raise ValueError(f"File {self.filename} has no columns.")

        if df.columns.to_list()[0].encode(self.encoding).decode(self.encoding) != df.columns.to_list()[0]:
            raise ValueError(f"File {self.filename} has invalid encoding.")

    def extract(self, params=None):
        try:
            return (pd.read_csv(self.filename))
        except Exception as e:
            raise e


class CSVDataCleaner(TransformInterface):

    transformations_config = {
        'Date of Admission': lambda x: pd.to_datetime(x).dt.strftime('%Y-%m-%d'),
        'Discharge Date': lambda x: pd.to_datetime(x).dt.strftime('%Y-%m-%d'),
        'Age': lambda x: pd.to_numeric(x, errors='coerce'),
        'Billing Amount': lambda x: pd.to_numeric(x, errors='coerce'),
        'Room Number': lambda x: pd.to_numeric(x, errors='coerce'),
        'Gender': lambda x: x.str.upper(),
        'Blood Type': lambda x: x.str.upper(),
        'Medical Condition': lambda x: x.str.capitalize(),
        'Doctor': lambda x: x.str.title(),
        'Hospital': lambda x: x.str.title(),
        'Insurance Provider': lambda x: x.str.title(),
        'Admission Type': lambda x: x.str.capitalize(),
        'Medication': lambda x: x.str.title(),
        'Test Results': lambda x: x.str.capitalize(),
    }

    def __init__(self, transformations=None):
        """
        Initializes the cleaner with a dictionary of transformations.
        :param transformations: A dict mapping column names to their transformation functions.
        """
        # Default transformations if none provided
        self.transformations = transformations if transformations is not None else self.transformations_config

    def transform(self, data):
        """
        Apply transformations to the dataframe based on the initialized configuration.
        :param data: pandas DataFrame to be transformed.
        :return: Transformed pandas DataFrame.
        """
        for column, transform_func in self.transformations.items():
            if column in data.columns:
                data[column] = transform_func(data[column])
        return data


class CSVDataLoader(LoadInterface):
    def __init__(self, db_name="default_db.sqlite", table_name=None, index=False):
        """
        Initializes the data loader with the target database and table names.
        :param db_name: Name of the SQLite database file to which the data will be saved.
        :param table_name: Name of the table to create and load data into.
        :param index: Whether to include the DataFrame index as a column in the table.
        """
        self.db_name = db_name
        self.table_name = table_name
        self.index = index
        self.db_tools = DatabaseTools(db_name=self.db_name)
        self.engine = create_engine(f'sqlite:///{db_name}')

    def load(self, data):
        """
        Prepares the DataFrame and loads data into the database table.
        :param data: pandas DataFrame to be loaded into the database.
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data to load must be a pandas DataFrame.")

        # Normalize DataFrame column names to ensure compatibility with SQL
        # This replaces spaces and other special characters in column names with underscores
        data.columns = [col.replace(" ", "_").replace("-", "_")
                        for col in data.columns]

        if not self.table_name:
            raise ValueError("Table name cannot be empty.")

        # Create the table in the database based on the DataFrame structure
        self.db_tools.create_table_from_df(data, self.table_name)

        # Load data into the table
        data.to_sql(self.table_name, self.engine,
                    if_exists='append', index=self.index)

        print(
            f"Data successfully loaded into table {self.table_name} in database {self.db_name}.")

        # Verify table creation and data insertion
        if self.db_tools.verify_table_creation(self.table_name):
            print(
                f"Verification: Table '{self.table_name}' exists in the database.")
        else:
            print(
                f"Verification failed: Table '{self.table_name}' does not exist in the database.")

        self.db_tools.close_connection()
