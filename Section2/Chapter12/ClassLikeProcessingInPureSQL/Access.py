import sqlite3
from pathlib import Path
from Blog import Blog


class Access:
    def open(self, path: Path) -> None:
        self.database = sqlite3.connect(Path)
        self.database.row_factory = sqlite3.Row

    def get_blog(self, id: str) -> Blog:
        query_blog = """
            SELECT * FROM blog WHERE id=? 
        """
        row = self.database.execute(query_blog, (id,)).fetchone()
        blog = Blog(title=row["TITLE"])
        blog._id = row["ID"]
        return blog
