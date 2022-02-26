from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Table
from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Enum,
    Float,
    Integer,
    Interval,
    LargeBinary,
    Numeric,
    PickleType,
    SmallInteger,
    String,
    Text,
    Time,
    Unicode,
    UnicodeText,
    ForeignKey
)
from sqlalchemy.orm import relationship, backref
from AssocPostTag import assoc_post_tag

Base = declarative_base()


class Post(Base):
    __tablename__ = "POST"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(DateTime)
    rst_text = Column(UnicodeText)
    blog_id = Column(Integer, ForeignKey("BLOG.id"))
    blog = relationship("Blog", backref="entries")
    tags = relationship("Tag", secondary=assoc_post_tag, backref="posts")

    def as_dict(self):
        return dict(
            title=self.title,
            undelrine="-" * len(self.title),
            date=self.date,
            rst_text=self.rst_text,
            tags=[t.phrase for t in self.tags],
        )
