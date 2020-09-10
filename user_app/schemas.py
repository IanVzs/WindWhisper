from typing import List

from pydantic import BaseModel


class WXInfoBase(BaseModel):
    openid: str
    city_id: int = 0


class WXInfoCreate(WXInfoBase):
    pass


class WXInfo(WXInfoBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    wx_infos: List[WXInfo] = []

    class Config:
        orm_mode = True
