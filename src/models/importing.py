import logging
import csv

from src.models.user import User



def import_users_from_csv(file_path):
    """
    Imports users from a CSV file and saves them to the database.

    :param file_path: Path to the CSV file containing user data.
    """
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                user_id = row["user_id"].strip()
                username = row["username"].strip()
                email = row["email"].strip()
                is_active = row["is_active"].strip()
                credit_points = row["credit_points"].strip()


                user = User(
                    user_id=int(user_id) if user_id else None,
                    username=username,
                    email=email,
                    is_active=is_active,
                    credit_points=credit_points
                )
                user.save()

            logging.info(f"Successfully imported users from {file_path}.")
    except Exception as e:
        logging.error(f"Failed to import users from {file_path}: {e}")


