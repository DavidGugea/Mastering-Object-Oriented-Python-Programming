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


assoc_post_tag = Table(
    "ASSOC_POST_TAG",
    Base.metadata,
    Column("POST_ID", Integer, ForeignKey("POST.id")),
    Column("TAG_ID", Integer, ForeignKey("TAG.id")),
)