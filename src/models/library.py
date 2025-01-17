import logging
from mysql.connector import Error
from src.database.database_singleton import Database
from .user import User
from .game import Game

class Library:
    def __init__(self, user_id, game_id, purchase_date, has_dlc=False):
        self.user_id = user_id
        self.game_id = game_id
        self.purchase_date = purchase_date
        self.has_dlc = has_dlc

    def save(self):
        """
        Vloží nebo aktualizuje záznam v Library (jestli je záznam jedinečný díky PK (user_id, game_id),
        tak se v praxi obvykle nevloží duplicita, ale zde pro jednoduchost:
        budeme dělat upsert-like.
        """
        try:
            # Ověřit, zda user i game existují
            user = User.find(self.user_id)
            game = Game.find(self.game_id)
            if not user or not game:
                raise ValueError("User or Game does not exist.")

            cursor = Database.get_cursor()
            # Nejdřív zkusíme najít existující záznam
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
        """
        Smaže záznam z Library.
        """
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


    def purchase_game(cls, user_id, game_id):
        """
        Příklad transakce, kdy uživatel kupuje hru:
        - Ověříme, že uživatel i hra existují.
        - Odepíšeme cenu z user.credit_points.
        - Zapíšeme záznam do Library (pokud už nemá).
        """
        conn = Database.get_connection()
        cursor = conn.cursor()

        try:
            conn.start_transaction()
            user = User.find(user_id)
            game = Game.find(game_id)
            if not user or not game:
                raise ValueError("User or Game does not exist.")

            if user.credit_points < game.price:
                raise ValueError("Insufficient credit points to purchase the game.")

            # Odepíšeme cenu
            user.credit_points -= game.price

            # Uložíme změnu user (updatujeme v DB)
            update_query = "UPDATE Users SET credit_points = %s WHERE user_id = %s"
            cursor.execute(update_query, (user.credit_points, user.user_id))

            # Přidáme/aktualizujeme záznam v Library
            insert_query = """
                INSERT INTO Library (user_id, game_id, purchase_date, has_dlc)
                VALUES (%s, %s, CURDATE(), %s)
                ON DUPLICATE KEY UPDATE purchase_date = CURDATE();
            """
            cursor.execute(insert_query, (user.user_id, game.game_id, False))

            conn.commit()
            cursor.close()
            logging.info(f"User {user_id} purchased game {game_id}.")
        except Error as e:
            conn.rollback()
            logging.error(f"Error purchasing game: {e}")
            raise
        finally:
            if not cursor.closed:
                cursor.close()

    @classmethod
    def find(cls, user_id, game_id):
        try:
            cursor = Database.get_cursor(dictionary=True)
            query = "SELECT * FROM Library WHERE user_id = %s AND game_id = %s"
            cursor.execute(query, (user_id, game_id))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return cls(**row)
            return None
        except Error as e:
            logging.error(f"Error finding library record: {e}")
            raise

    @classmethod
    def all(cls):
        """Vrátí všechny záznamy v Library."""
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
