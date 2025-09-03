class Config:
    """
    Clase de configuración para rutas y parámetros del ETL.
    """
    INPUT_PATH = r'Files\F1Wins.csv'
    SQLITE_DB_PATH = r'Files\etl_data.db'
    SQLITE_TABLE = 'ride_bookings_clean'