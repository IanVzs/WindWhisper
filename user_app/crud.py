from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_cityid(db: Session, cityid: str):
    skip = 0
    limit = 1000
    return db.query(models.WXInfo).filter(models.WXInfo.city_id == cityid).offset(skip).limit(limit).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_wx_infos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WXInfo).offset(skip).limit(limit).all()


def create_user_item(db: Session, wx_info: schemas.WXInfoCreate, user_id: int):
    db_wx_info = models.WXInfo(**wx_info.dict(), id=user_id)
    db.add(db_wx_info)
    db.commit()
    db.refresh(db_wx_info)
    return db_wx_info

def get_wxinfo_by_openid(db: Session, openid: str):
    return db.query(models.WXInfo).filter(models.WXInfo.openid == openid).first()

def update_user_item(db: Session, wx_info: schemas.WXInfoCreate, user_id: int):
    new_info = models.WXInfo.update(db, user_id, wx_info)
    return new_info
