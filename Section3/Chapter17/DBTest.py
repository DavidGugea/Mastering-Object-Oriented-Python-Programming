from Section2.Chapter12 import Blog, Post, Tag, assoc_post_tag
import datetime
import sqlalchemy.exc
from sqlalchemy import create_engine


def build_test_db(name="sqlite://./data.db"):
    """
    Create Test Database and Schema
    """

    engine = create_engine(name, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    return engine