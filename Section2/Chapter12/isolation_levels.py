import sqlite3
from contextlib import closing

database = sqlite3.connect("Blog.db", isolation_level='DEFERRED')
try:
    with closing(database.cursor()) as cursor:
        cursor.execute("BEGIN")
        # cursor.execute("some statement")
        # cursor.execute("another statement")

    database.commit()
except Exception as e:
    database.rollback()
