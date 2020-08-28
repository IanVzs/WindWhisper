"""
Base: 读写可见
Create: 仅写时可见
[本体] : 仅读时可见
"""
from typing import List
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel


class AlarmInfoBase(BaseModel):
    lon: Decimal = Decimal(0)
    lat: Decimal = Decimal(0)
    signalType: str
    signalLevel: str
    issueTime: datetime
    relieveTime: datetime
    issueContent: str = ''

class AlarmInfoCreate(AlarmInfoBase):
    pass


class AlarmInfo(AlarmInfoBase):
    id: int

    class Config:
        orm_mode = True


class CityBase(BaseModel):
    id: int
    lon: Decimal = Decimal(0)
    lat: Decimal = Decimal(0)
    cityZh: str
    provinceZh: str = ''
    leaderZh: str = ''


class CityCreate(CityBase):
    pass


class City(CityBase):
    is_active: bool = 1
    alarm_infos: List[AlarmInfo] = []

    class Config:
        orm_mode = True