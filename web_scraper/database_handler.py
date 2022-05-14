import json

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import event


def _get_engine():
    df_single = {
        "HOST": "mysql.studev.groept.be",
        "USER": "a21pt313",
        "PASS": "secret",
        "DRIVER": "mysql+pymysql"
    }

    engine = create_engine(df_single['DRIVER'] + "://{0}:{1}@{2}/{3}".format(
        df_single['USER'], df_single['PASS'], df_single['HOST'], 'a21pt313'),
                           echo=True, future=True)
    return engine


eng = _get_engine()

@event.listens_for(eng, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if executemany:
        cursor.fast_executemany = True


with open('data.json', 'r') as fr:
    table_exercise = json.load(fr)

table_exercise_appended = []

for item in table_exercise:
    identifier_name = list(item.keys())[0]
    nw_item = item[identifier_name]

    nw_item['identifier'] = identifier_name

    table_exercise_appended.append(nw_item)

df = pd.DataFrame(table_exercise_appended)
df = df.astype(str)
# print(df.dtypes)

df.to_sql('public_exercises', eng, index=False, if_exists="append")
