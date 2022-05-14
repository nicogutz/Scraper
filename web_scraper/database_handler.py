import json
import os
import sys

import sqlparse
from sqlalchemy import text, create_engine


class DatabaseHandler:
    def __init__(self):
        self.src_dir = os.path.dirname(__file__)
        self.file_archive = "processed_files.csv"
        self.database = self._get_engine()
        self.sql_commands = self._getSQL()

    def database_insert(self, command, data):
        with self.database.connect() as db:
            for row in data:
                db.execute(text(command), row)
            db.commit()

    @staticmethod
    def _get_engine():
        df_single = {
            "HOST": "mysql.studev.groept.be",
            "USER": "a21pt313",
            "PASS": "secret",
            "DRIVER": "mysql+pymysql"
        }

        engine = create_engine(df_single['DRIVER'] + "://{0}:{1}@{2}".format(
            df_single['USER'], df_single['PASS'], df_single['HOST'], 'a21pt313'),
                               echo=True, future=True)
        return engine

    def _getSQL(self):
        """
        This method reads the query file, splits the data and strips the comments.

        :return: array containing the sql commands without comments and separated by ;
        """
        try:
            fd = open(os.path.join(self.src_dir + '/config/database_queries.sql'), 'r')
            sql_file = fd.read()
            fd.close()
        except OSError as OSe:
            print(OSe)
            sys.exit()

        sql_commands = sqlparse.split(sql_file)

        for count, sql_command in enumerate(sql_commands):
            sql_commands[count] = sqlparse.format(sql_command, strip_comments=True)

        return sql_commands


with open('data.json', 'r') as fr:
    table_exercise = json.load(fr)
dict_exercise =

dbh = DatabaseHandler()
