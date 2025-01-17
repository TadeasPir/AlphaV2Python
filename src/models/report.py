import logging
from mysql.connector import Error
from src.database.database import Database

class Review:

    def v_user_library_stats(self):
        try:
            cursor = Database.get_cursor()
            query = "SELECT * FROM v_user_library_stats LIMIT 100;"
            cursor.execute(query, )
            row = cursor.fetchone()
            cursor.close()

            return row

        except Error as e:
            logging.error(f"Error finding v_user_library_stats: {e}")

    def v_game_overview(self):
        try:
            cursor = Database.get_cursor()
            query = "SELECT * FROM v_game_overview LIMIT 100;"
            cursor.execute(query, )
            row = cursor.fetchone()
            cursor.close()

            return row

        except Error as e:
            logging.error(f"Error finding v_user_library_stats: {e}")


