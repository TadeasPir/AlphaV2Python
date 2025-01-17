import logging
from mysql.connector import Error

from src.database.database import Database
from src.models.genre_enum import GenreEnum


class Game:
    def __init__(self, game_id=None, title=None, release_date=None, genre='Other', price=0.0, is_multiplayer=False):
        self.game_id = game_id
        self.title = title
        self.release_date = release_date
        self.genre = genre
        self.price = price
        self.is_multiplayer = is_multiplayer
        self.genre_enum = GenreEnum


    def save(self):

        try:
            cursor = Database.get_cursor()
            if self.genre not in GenreEnum.__members__:
                logging.error("incorect value for genre")
                raise ValueError

            if self.game_id:
                # Update
                query = """
                    UPDATE Games
                    SET title = %s, release_date = %s, genre = %s,
                        price = %s, is_multiplayer = %s
                    WHERE game_id = %s
                """
                cursor.execute(query, (self.title, self.release_date, self.genre,
                                       self.price, self.is_multiplayer, self.game_id))
            else:
                # Insert
                query = """
                    INSERT INTO Games (title, release_date, genre, price, is_multiplayer)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (self.title, self.release_date, self.genre,
                                       self.price, self.is_multiplayer))
                self.game_id = cursor.lastrowid

            Database.get_connection().commit()
            cursor.close()
            logging.info(f"Game saved: {self}")
        except Error as e:
            logging.error(f"Error saving game: {e}")
            raise

    def delete(self):
        if not self.game_id:
            raise ValueError("Cannot delete a game without a game_id.")

        try:
            cursor = Database.get_cursor()
            query = "DELETE FROM Games WHERE game_id = %s"
            cursor.execute(query, (self.game_id,))
            Database.get_connection().commit()
            cursor.close()
            logging.info(f"Game deleted: {self}")
        except Error as e:
            logging.error(f"Error deleting game: {e}")
            raise


    def find(self):
        try:
            cursor = Database.get_cursor()
            query = "SELECT * FROM Games WHERE game_id = %s"
            cursor.execute(query, (self.game_id,))
            row = cursor.fetchone()
            cursor.close()

            return row

        except Error as e:
            logging.error(f"Error finding game: {e}")


    @classmethod
    def all(cls):
        try:
            cursor = Database.get_cursor(dictionary=True)
            query = "SELECT * FROM Games"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [cls(**row) for row in rows]
        except Error as e:
            logging.error(f"Error retrieving all games: {e}")
            raise

    def __repr__(self):
        return f"Game(game_id={self.game_id}, title='{self.title}', release_date={self.release_date}, " \
               f"genre='{self.genre}', price={self.price}, is_multiplayer={self.is_multiplayer})"
