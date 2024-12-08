import pyodbc
import pandas as pd


# Database connection function
def get_database_data(query):
    # Connection details
    server = 'DESKTOP-DDJT56D'
    database = 'us_election_data'
    username = 'INFA_REP'
    password = 'admin'
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    connection = pyodbc.connect(connection_string)

    # Fetch data
    df = pd.read_sql(query, connection)

    # Close connection
    connection.close()
    return df
