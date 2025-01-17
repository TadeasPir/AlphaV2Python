import logging
from mysql.connector import Error
from src.database.database import Database

class Achievement:
    def __init__(self, achievement_id=None, user_id=None, game_id=None,
                 achievement_title=None, date_earned=None, points_earned=0.0):
        self.achievement_id = achievement_id
        self.user_id = user_id
        self.game_id = game_id
        self.achievement_title = achievement_title
        self.date_earned = date_earned
        self.points_earned = points_earned

    def save(self):
        try:
            cursor = Database.get_cursor()
            if self.achievement_id:
                # Update
                query = """
                    UPDATE Achievements
                    SET user_id = %s, game_id = %s, achievement_title = %s,
                        date_earned = %s, points_earned = %s
                    WHERE achievement_id = %s
                """
                cursor.execute(query, (self.user_id, self.game_id, self.achievement_title,
                                       self.date_earned, self.points_earned, self.achievement_id))
            else:
                # Insert
                query = """
                    INSERT INTO Achievements (user_id, game_id, achievement_title, date_earned, points_earned)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (self.user_id, self.game_id, self.achievement_title,
                                       self.date_earned, self.points_earned))
                self.achievement_id = cursor.lastrowid

            Database.get_connection().commit()
            cursor.close()
            logging.info(f"Achievement saved: {self}")
        except Error as e:
            logging.error(f"Error saving achievement: {e}")
            raise

    def delete(self):
        if not self.achievement_id:
            raise ValueError("Cannot delete an achievement without an achievement_id.")
        try:
            cursor = Database.get_cursor()
            query = "DELETE FROM Achievements WHERE achievement_id = %s"
            cursor.execute(query, (self.achievement_id,))
            Database.get_connection().commit()
            cursor.close()
            logging.info(f"Achievement deleted: {self}")
        except Error as e:
            logging.error(f"Error deleting achievement: {e}")
            raise

    @classmethod
    def find(cls, achievement_id):
        try:
            cursor = Database.get_cursor(dictionary=True)
            query = "SELECT * FROM Achievements WHERE achievement_id = %s"
            cursor.execute(query, (achievement_id,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return cls(**row)
            return None
        except Error as e:
            logging.error(f"Error finding achievement: {e}")
            raise

    @classmethod
    def all(cls):
        try:
            cursor = Database.get_cursor(dictionary=True)
            query = "SELECT * FROM Achievements"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [cls(**row) for row in rows]
        except Error as e:
            logging.error(f"Error retrieving achievements: {e}")
            raise

    def __repr__(self):
        return f"Achievement(achievement_id={self.achievement_id}, user_id={self.user_id}, " \
               f"game_id={self.game_id}, achievement_title='{self.achievement_title}', " \
               f"date_earned={self.date_earned}, points_earned={self.points_earned})"
