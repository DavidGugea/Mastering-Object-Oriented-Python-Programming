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

Base = declarative_base()


class Blog(Base):
    __tablename__ = "BLOG"
    id = Column(Integer, primary_key=True)
    title = Column(String)

    def as_dict(self):
        return dict(
            title=self.title,
            underline="=" * len(self.title),
            entries = [e.as_dict() for e in self.entries],
        )
