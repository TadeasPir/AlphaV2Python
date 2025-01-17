import mysql.connector
import yaml
import logging
from typing import Optional
from mysql.connector import MySQLConnection

class DatabaseSingleton:
    _instance: Optional['DatabaseSingleton'] = None
    _connection: Optional[MySQLConnection] = None

    def __new__(cls) -> 'DatabaseSingleton':
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Initialize only if connection hasn't been established
        if DatabaseSingleton._connection is None:
            self._load_config()

    def _load_config(self):
        """Load database configuration from config.yaml file"""
        try:
            with open('config/config.yaml', 'r') as file:
                config = yaml.safe_load(file)
                self.db_config = config['db']
        except Exception as e:
            logging.error(f"Failed to load database configuration: {str(e)}")
            raise

    def connect(self) -> MySQLConnection:
        """Establish database connection if it doesn't exist"""
        if DatabaseSingleton._connection is None:
            try:
                DatabaseSingleton._connection = mysql.connector.connect(
                    host=self.db_config['host'],
                    user=self.db_config['user'],
                    password=self.db_config['password'],
                    database=self.db_config['database']
                )
                logging.info("Database connection established successfully")
            except Exception as e:
                logging.error(f"Failed to connect to database: {str(e)}")

        return DatabaseSingleton._connection

    def get_connection(self) -> MySQLConnection:
        """Get existing connection or create new one"""
        if DatabaseSingleton._connection is None:
            return self.connect()
        return DatabaseSingleton._connection

    def close_connection(self):
        """Close the database connection"""
        if DatabaseSingleton._connection is not None:
            try:
                DatabaseSingleton._connection.close()
                DatabaseSingleton._connection = None
                logging.info("Database connection closed successfully")
            except Exception as e:
                logging.error(f"Error closing database connection: {str(e)}")
                raise