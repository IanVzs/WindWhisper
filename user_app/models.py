from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    wx_infos = relationship("WXInfo", back_populates="owner")


class WXInfo(Base):
    __tablename__ = "wx_infos"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)
    openid = Column(String(12), index=True)
    city_id = Column(Integer, index=True)

    owner = relationship("User", back_populates="wx_infos")
    
    @classmethod
    def update(cls, db: Session, user_id: int, new_data: dict):
        db.query(cls).filter_by(id=user_id).update(new_data)
        db.commit()
        return db.query(cls).filter_by(id=user_id).first()