from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session

from . import models, schemas


def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_id(db: Session, id: str):
    return db.query(models.City).filter(models.City.id == id).first()


def get_citys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate):
    # fake_hashed_password = city.password + "notreallyhashed"
    city.lon = Decimal(city.lon)
    city.lat = Decimal(city.lat)
    # db_city = models.City(id=city.id, hashed_password=fake_hashed_password)
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_alarm_infos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AlarmInfo).offset(skip).limit(limit).all()


def create_city_item(db: Session, wx_info: schemas.AlarmInfoCreate, city_id: int):
    wx_info.lon = Decimal(wx_info.lon)
    wx_info.lat = Decimal(wx_info.lat)
    db_wx_info = models.AlarmInfo(**wx_info.dict(), id=city_id)
    db.add(db_wx_info)
    db.commit()
    db.refresh(db_wx_info)
    return db_wx_info
