import logging
from mysql.connector import Error
from src.database.database import Database

class Review:
    def __init__(self, review_id=None, game_id=None, user_id=None, rating=0.0, review_text=None, review_date=None):
        self.review_id = review_id
        self.game_id = game_id
        self.user_id = user_id
        self.rating = rating
        self.review_text = review_text
        self.review_date = review_date

    def save(self):
        try:
            cursor = Database.get_cursor()
            if self.review_id:
                # Update
                query = """
                    UPDATE Reviews
                    SET game_id = %s, user_id = %s, rating = %s,
                        review_text = %s, review_date = %s
                    WHERE review_id = %s
                """
                cursor.execute(query, (self.game_id, self.user_id, self.rating,
                                       self.review_text, self.review_date, self.review_id))
            else:
                # Insert
                query = """
                    INSERT INTO Reviews (game_id, user_id, rating, review_text, review_date)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (self.game_id, self.user_id, self.rating,
                                       self.review_text, self.review_date))
                self.review_id = cursor.lastrowid

            Database.get_connection().commit()
            cursor.close()
            logging.info(f"Review saved: {self}")
        except Error as e:
            logging.error(f"Error saving review: {e}")


    def delete(self):
        if not self.review_id:
            raise ValueError("Cannot delete a review without a review_id.")
        try:
            cursor = Database.get_cursor()
            query = "DELETE FROM Reviews WHERE review_id = %s"
            cursor.execute(query, (self.review_id,))
            Database.get_connection().commit()
            cursor.close()
            logging.info(f"Review deleted: {self}")
        except Error as e:
            logging.error(f"Error deleting review: {e}")
            raise

    def find(self):
        try:
            cursor = Database.get_cursor()
            query = "SELECT * FROM Reviews WHERE review_id = %s"
            cursor.execute(query, (self.review_id,))
            row = cursor.fetchone()
            cursor.close()

            return row

        except Error as e:
            logging.error(f"Error finding game: {e}")

    @classmethod
    def all(cls):
        try:
            cursor = Database.get_cursor(dictionary=True)
            query = "SELECT * FROM Reviews"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [cls(**row) for row in rows]
        except Error as e:
            logging.error(f"Error retrieving reviews: {e}")


    def __repr__(self):
        return f"Review(review_id={self.review_id}, game_id={self.game_id}, user_id={self.user_id}, " \
               f"rating={self.rating}, review_text='{self.review_text}', review_date={self.review_date})"
