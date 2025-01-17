import logging
from datetime import datetime

from mysql.connector import Error
from src.database.database import Database
from .user import User
from .game import Game

class Library:
    def __init__(self, user_id = None, game_id = None, purchase_date = None, has_dlc=False):
        self.user_id = user_id
        self.game_id = game_id
        self.purchase_date = purchase_date
        self.has_dlc = has_dlc

    def save(self):

        try:

            user = User(user_id=self.user_id).find()
            game = Game(game_id=self.game_id).find()
            if not user or not game:
                raise ValueError("User or Game does not exist.")

            cursor = Database.get_cursor()

            select_query = """
                SELECT COUNT(*) as count_row FROM Library
                WHERE user_id = %s AND game_id = %s
            """
            cursor.execute(select_query, (self.user_id, self.game_id))
            result = cursor.fetchone()
            count_row = result[0] if result else 0

            if count_row > 0:
                # Update
                query = """
                    UPDATE Library
                    SET purchase_date = %s, has_dlc = %s
                    WHERE user_id = %s AND game_id = %s
                """
                cursor.execute(query, (self.purchase_date, self.has_dlc, self.user_id, self.game_id))
            else:
                # Insert
                query = """
                    INSERT INTO Library (user_id, game_id, purchase_date, has_dlc)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (self.user_id, self.game_id, self.purchase_date, self.has_dlc))

            Database.get_connection().commit()
            cursor.close()
            logging.info(f"Library record saved: {self}")
        except Error as e:
            logging.error(f"Error saving library record: {e}")
            raise

    def delete(self):

        try:
            cursor = Database.get_cursor()
            query = "DELETE FROM Library WHERE user_id = %s AND game_id = %s"
            cursor.execute(query, (self.user_id, self.game_id))
            Database.get_connection().commit()
            cursor.close()
            logging.info(f"Library record deleted: {self}")
        except Error as e:
            logging.error(f"Error deleting library record: {e}")
            raise

    def find(self):
        try:
            cursor = Database.get_cursor()
            query = "SELECT * FROM Library WHERE user_id = %s AND game_id = %s"
            cursor.execute(query, (self.user_id, self.game_id))
            row = cursor.fetchone()
            cursor.close()

            return row

        except Error as e:
            logging.error(f"Error finding library: {e}")



    @classmethod
    def all(cls):

        try:
            cursor = Database.get_cursor(dictionary=True)
            query = "SELECT * FROM Library"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [cls(**row) for row in rows]
        except Error as e:
            logging.error(f"Error retrieving library records: {e}")
            raise

    def __repr__(self):
        return f"Library(user_id={self.user_id}, game_id={self.game_id}, " \
               f"purchase_date={self.purchase_date}, has_dlc={self.has_dlc})"
