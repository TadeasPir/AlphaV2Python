import json
import logging
import os

from mysql.connector import Error
from setuptools.command.saveopts import saveopts

from src.database.database import Database

class Report:
    def __init__(self, output_dir: str = 'reports'):
        self.output_dir = output_dir
        self.setup_output_dir()
        self.reports = []

    def setup_output_dir(self):
        os.makedirs(self.output_dir, exist_ok=True)
        self.reports_file = os.path.join(self.output_dir, 'report.json')

        # Load existing reports if file exists
        if os.path.exists(self.reports_file):
            try:
                with open(self.reports_file, 'r', encoding='utf-8') as f:
                    self.reports = json.load(f)
            except json.JSONDecodeError:
                self.reports = []

    def v_game_overview(self):
        try:
            cursor = Database.get_cursor()
            query = "SELECT * FROM v_game_overview LIMIT 100;"
            cursor.execute(query, )
            row = cursor.fetchall()
            cursor.close()
            self.reports.append(row)
            self.save_to_file()

        except Error as e:
                logging.error(f"Error finding v_user_library_stats: {e}")

    def v_user_library_stats(self):

        try:
            cursor = Database.get_cursor()
            query = "SELECT * FROM v_user_library_stats LIMIT 100;"
            cursor.execute(query, )
            row = cursor.fetchall()
            cursor.close()
            self.reports.append(row)
            self.save_to_file()



        except Error as e:
            logging.error(f"Error finding v_user_library_stats: {e}")

    def save_to_file(self):
        try:
            with open(self.reports_file, 'w', encoding='utf-8') as f:
                json.dump(self.reports, f, ensure_ascii=False, indent=2)
            logging.info(" saved reports to {self.reports_file}")
        except Exception as e:
            logging.error(f" failed to save reports to file: {e}")
