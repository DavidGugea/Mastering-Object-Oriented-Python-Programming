import sqlite3
from contextlib import closing

DDL_string = """
CREATE TABLE blog(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT
);
CREATE TABLE post(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TIMESTAMP,
    title TEXT,
    rst_text TEXT,
    blog_id INTEGER REFERENCES blog(id)
);
CREATE TABLE tag(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phrase TEXT UNIQUE ON CONFLICT FAIL
);
CREATE TABLE assoc_post_tag(
    post_id INTEGER REFERENCES post(id),
    tag_id INTEGER REFERENCES tag(id)
);
"""

database = sqlite3.connect("Blog.db")
try:
    database.executescript(DDL_string)
except sqlite3.OperationalError:
    print("DDL Already executed")

if __name__ == '__main__':
    create_blog = """
        INSERT INTO blog(title) VALUES(?);
    """
    update_blog = """
        UPDATE blog SET title=:new_title WHERE title=:old_title;
    """

    with closing(database.cursor()) as cursor:
        print("started cursor")
        cursor.execute(
            update_blog,
            dict(
                new_title="2013-2014 Travel",
                old_title="Travel Blog"
            )
        )
        print("finished cursor")

    database.commit()

database.close()
