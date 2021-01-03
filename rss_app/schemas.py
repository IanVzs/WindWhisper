"""
Base: 读写可见
Create: 仅写时可见
[本体] : 仅读时可见
"""
from typing import List
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel


class ArticlesBase(BaseModel):
    dtpub: datetime
    title: str
    content: str
    openum: int

class ArticlesCreate(ArticlesBase):
    pass


class Articles(ArticlesBase):
    id: int

    class Config:
        orm_mode = True


class RssBase(BaseModel):
    url: str
    description: str


class RssCreate(RssBase):
    srtdesc: str
    class Config:
        min_anystr_length = 1
        max_anystr_length = 16

class RssItem(RssBase):
    class Config:
        orm_mode = True

class Rss(RssBase):
    srtdesc: str
    articles: List[Articles] = []

    class Config:
        orm_mode = True
