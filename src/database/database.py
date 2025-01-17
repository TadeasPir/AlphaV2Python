import logging
import mysql.connector
from mysql.connector import Error
from src.config import Config
import yaml

class Database:
    """
    Třída Database se stará o vytvoření a správu jednoho připojení k databázi.
    """
    _connection = None

    @classmethod
    def _load_config(cls):
        """Load database configuration from config.yaml file"""
        try:
            with open('config/config.yaml', 'r') as file:
                config = yaml.safe_load(file)
                cls.db_config = config['db']
        except Exception as e:
            logging.error(f"Failed to load database configuration: {str(e)}")


    @classmethod
    def connect(cls):
        """Naváže spojení s databází, pokud ještě není navázáno."""
        if cls._connection is None:
            try:
                cls._connection = mysql.connector.connect(
                    host=cls.db_config['host'],
                    user=cls.db_config['user'],
                    password=cls.db_config['password'],
                    database=cls.db_config['database'])
                logging.info("Connected to the database successfully.")
            except Error as e:
                logging.error(f"Failed to connect to the database: {e}")
                raise

    @classmethod
    def get_connection(cls):
        """Vrátí aktivní connection objekt."""
        cls.connect()
        return cls._connection

    @classmethod
    def close_connection(cls):
        """Uzavře spojení k databázi."""
        if cls._connection is not None and cls._connection.is_connected():
            cls._connection.close()
            cls._connection = None
            logging.info("Database connection closed.")

    @classmethod
    def get_cursor(cls, dictionary=False):
        """
        Vrátí nový kurzor pro databázi.
        :param dictionary: Pokud True, vrátí kurzor, který vrací řádky jako slovníky.
        """
        conn = cls.get_connection()
        return conn.cursor(dictionary=dictionary)
