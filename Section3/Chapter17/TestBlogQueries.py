from sqlalchemy.orm import sessionmaker
import unittest
from DBTest import build_test_db


class Test_Blog_Queries(unittest.TestCase):
    @staticmethod
    def setUpClass() -> None:
        engine = build_test_db()
        Test_Blog_Queries.Session = sessionmaker(bind=engine)
        session = Test_Blog_Queries.Session()

        tag_rr = Tag(pharse="#testTag1")
        session.add(tag_rr)
        tag_w42 = Tag(pharse="#testTag2")
        session.add(tag_w42)

        blog1 = Blog(title="testTitle")
        session.add(blog1)
        b1p1 = Post(date=datetime.datetime(2013, 11, 14, 17, 25), title="Test Title", rst_text="""Text""", blog=blog1, tags=[tag_rr, tag_w42])
        session.add(b1p1)


        session.commit()