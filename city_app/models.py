from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# TODO 报警字段信息还需要更新
class City(Base):
    __tablename__ = "citys"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    alarm_infos = relationship("AlarmInfo", back_populates="owner")


class AlarmInfo(Base):
    __tablename__ = "alarm_infos"

    id = Column(Integer, ForeignKey("citys.id"), primary_key=True, index=True)
    openid = Column(String(12), index=True)
    city = Column(String(12), index=True)

    owner = relationship("City", back_populates="alarm_infos")
