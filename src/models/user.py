import logging
from mysql.connector import Error
from src.database.database import Database

class User:
    def __init__(self, user_id=None, username=None, email=None, is_active=True, credit_points=0.0):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.is_active = is_active
        self.credit_points = credit_points

    def save(self):
        """Uloží (vloží nebo updatuje) uživatele do databáze."""
        cursor = Database.get_cursor()
        try:
            # Insert
            query = """
                INSERT INTO Users (username, email, is_active, credit_points)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (self.username, self.email, self.is_active, self.credit_points))
            self.user_id = cursor.lastrowid

            Database.get_connection().commit()
            cursor.close()
            logging.info(f"User saved: {self}")
        except Error as e:
            logging.error(f"Error saving user: {e}")

    def update(self):
        try:
            cursor = Database.get_cursor()
            if self.user_id:
                # Update
                query = """
                                    UPDATE Users
                                    SET username = %s, email = %s, is_active = %s, credit_points = %s
                                    WHERE user_id = %s
                                """
                cursor.execute(query, (self.username, self.email, self.is_active, self.credit_points, self.user_id))
        except Error as e:
            logging.error(f"Error editing user: {e}")


    def delete(self):
        """Smaže uživatele z databáze."""
        if not self.user_id:
            raise ValueError("Cannot delete a user without a user_id.")

        try:
            cursor = Database.get_cursor()
            query = "DELETE FROM Users WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            Database.get_connection().commit()
            cursor.close()
            logging.info(f"User deleted: {self}")
        except Error as e:
            logging.error(f"Error deleting user: {e}")
            raise

    @classmethod
    def find(cls, user_id):
        """Najde uživatele podle ID."""
        try:
            cursor = Database.get_cursor(dictionary=True)
            query = "SELECT * FROM Users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return cls(**row)
            return None
        except Error as e:
            logging.error(f"Error finding user: {e}")
            raise

    @classmethod
    def all(cls):
        """Vrátí všechny uživatele."""
        try:
            cursor = Database.get_cursor(dictionary=True)
            query = "SELECT * FROM Users"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [cls(**row) for row in rows]
        except Error as e:
            logging.error(f"Error retrieving all users: {e}")
            raise

    @classmethod
    def transfer_credits(cls, from_user_id, to_user_id, amount):
        """
        Převádí kreditní body mezi dvěma uživateli v jedné transakci.
        """
        if amount <= 0:
            raise ValueError("Amount must be positive.")

        conn = Database.get_connection()
        cursor = conn.cursor()

        try:
            conn.start_transaction()

            # Zkontrolujeme, jestli mají oba uživatelé dostatečnou existenci
            from_user = cls.find(from_user_id)
            to_user = cls.find(to_user_id)

            if from_user is None or to_user is None:
                raise ValueError("One of the users does not exist.")

            if from_user.credit_points < amount:
                raise ValueError("Insufficient credit points in source user account.")

            # Změna kreditu
            from_user.credit_points -= amount
            to_user.credit_points += amount

            # Update v DB
            update_query = "UPDATE Users SET credit_points = %s WHERE user_id = %s"
            cursor.execute(update_query, (from_user.credit_points, from_user.user_id))
            cursor.execute(update_query, (to_user.credit_points, to_user.user_id))

            conn.commit()
            cursor.close()
            logging.info(f"Transferred {amount} from User {from_user_id} to User {to_user_id}")

        except Error as e:
            conn.rollback()
            logging.error(f"Error transferring credits: {e}")
            raise
        finally:
            if not cursor.closed:
                cursor.close()

    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}', email='{self.email}', " \
               f"is_active={self.is_active}, credit_points={self.credit_points})"
