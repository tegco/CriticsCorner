import os
import django
import requests
import sqlite3

from criticscorner.settings import SECRET_KEY

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'criticscorner.settings')
django.setup()
from django.db import connection

string1 = "['"
string2 = "']"
string3 = "'"


def update_db(table_name, field, replace_string):
    conn = sqlite3.connect("db.sqlite3")  # Define the data you want to insert

    # Build the SQL query
    query = f"UPDATE {table_name}  SET {field} = REPLACE({field}, \"{replace_string}\", \"\")"

    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.close()


update_db("review_movie", "director", string1)
update_db("review_movie", "director", string2)
update_db("review_movie", "director", string3)
update_db("review_movie", "writer", string1)
update_db("review_movie", "writer", string2)
update_db("review_movie", "writer", string3)
update_db("review_movie", "genres", string1)
update_db("review_movie", "genres", string2)
update_db("review_movie", "genres", string3)
