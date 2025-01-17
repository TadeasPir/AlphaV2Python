import logging
import csv
import json
from .models.user import User
from .models.game import Game

def import_users_from_csv(csv_file_path):

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row['username']
                email = row['email']
                is_active = row['is_active'].lower() in ['true', '1', 'yes']
                credit_points = float(row['credit_points'])
                user = User(username=username, email=email, is_active=is_active, credit_points=credit_points)
                user.save()
        logging.info("Users imported successfully from CSV.")
    except Exception as e:
        logging.error(f"Error importing users from CSV: {e}")
        raise

def import_games_from_json(json_file_path):

    try:
        with open(json_file_path, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                title = item.get('title')
                release_date = item.get('release_date')
                genre = item.get('genre', 'Other')
                price = float(item.get('price', 0.0))
                is_multiplayer = bool(item.get('is_multiplayer', False))

                game = Game(title=title, release_date=release_date, genre=genre,
                            price=price, is_multiplayer=is_multiplayer)
                game.save()
        logging.info("Games imported successfully from JSON.")
    except Exception as e:
        logging.error(f"Error importing games from JSON: {e}")
        raise
