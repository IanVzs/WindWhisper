from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL, Unicode, DateTime, UnicodeText
from sqlalchemy.orm import relationship, Session

from .database import Base

class City(Base):
    __tablename__ = "citys"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    lon = Column(DECIMAL(10, 7))
    lat = Column(DECIMAL(10, 7))
    cityZh = Column(Unicode(16))
    provinceZh = Column(Unicode(12))
    leaderZh = Column(Unicode(16))
    is_active = Column(Boolean, default=True)

    alarm_infos = relationship("AlarmInfo", back_populates="owner")


class AlarmInfo(Base):
    __tablename__ = "alarm_infos"

    id = Column(Integer, ForeignKey("citys.id"), primary_key=True, index=True, unique=False)
    lon = Column(DECIMAL(10, 7))
    lat = Column(DECIMAL(10, 7))
    signalType = Column(Unicode(7))
    signalLevel = Column(Unicode(7))
    dt = Column(DateTime)
    issueTime = Column(DateTime)
    relieveTime = Column(DateTime)
    issueContent = Column(UnicodeText)

    owner = relationship("City", back_populates="alarm_infos")

    @classmethod
    def update(cls, db: Session, city_id: int, new_data: dict):
        db.query(cls).filter_by(id=city_id).update(new_data)
        db.commit()