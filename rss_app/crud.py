from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session

from . import models, schemas


def format_lon_lat(data):
    data.lon = Decimal(data.lon)
    data.lat = Decimal(data.lat)
    return data

def get_rss(db: Session, rss_id: int):
    return db.query(models.Rss).filter(models.Rss.id == rss_id).first()

def get_rsses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rss).offset(skip).limit(limit).all()

def get_rss_by_srtdesc(db: Session, srtdesc: str):
    return db.query(models.Rss).filter(models.Rss.srtdesc == srtdesc).first()

def create_rss(db: Session, rss: schemas.RssCreate):
    db_rss = models.Rss(**rss.dict())
    db.add(db_rss)
    db.commit()
    db.refresh(db_rss)
    return db_rss

def list_article_by_srtdesc(db: Session, srtdesc: str):
    return db.query(models.Articles).filter(models.Articles.srtdesc == srtdesc).all()

def create_rss_article(db: Session, rss_article: schemas.ArticlesCreate):
    db_rss_article = models.Articles(**rss_article.dict())
    db.add(db_rss_article)
    db.commit()
    db.refresh(db_rss_article)
    return db_rss_article

def update_rss_article(db: Session, rss_articles: schemas.ArticlesCreate, rss_id: int):
    rss_articles = format_lon_lat(rss_articles)
    new_articles = models.Articles.update(db, rss_id, rss_articles)
    return new_articles