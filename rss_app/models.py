import datetime
from sqlalchemy.orm import relationship, Session
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL, Unicode, DateTime, UnicodeText


from .database import Base

class Rss(Base):
    __tablename__ = "rss"

    id = Column(Integer, primary_key=True, index=True)
    srtdesc = Column(Unicode(16), index=True)
    dtcrt = Column(DateTime, default=datetime.datetime.now())
    url = Column(Unicode(256))
    description = Column(Unicode(64))
    status = Column(Integer, default=1)

    articles = relationship("Articles", back_populates="owner")

class Articles(Base):
    __tablename__ = "articles"

    id = Column(Integer, ForeignKey("rss.id"), primary_key=True, index=True)
    dtpub = Column(DateTime)
    title = Column(Unicode(256))
    content = Column(UnicodeText)
    openum = Column(Integer, default=1)
    
    owner = relationship("Rss", back_populates="articles")
