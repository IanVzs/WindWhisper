from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from route_class import TimedRoute, APIRouter
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter(route_class=TimedRoute)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/bycity/{cityid}", response_model=List[schemas.WXInfo])
def read_user_by_cityid(cityid: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_user_info = crud.get_user_by_cityid(db, cityid=cityid)
    if db_user_info is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user_info

@router.post("/users/{user_id}/wx_infos/", response_model=schemas.WXInfo)
def create_item_for_user(
    user_id: int, wx_info: schemas.WXInfoCreate, db: Session = Depends(get_db)
):
    user_info = crud.get_user(db, user_id=user_id)
    if not user_info or not user_info.wx_infos:
        return crud.create_user_item(db=db, wx_info=wx_info, user_id=user_id)
    else:
        return crud.update_user_item(db=db, wx_info=wx_info, user_id=user_id)


@router.get("/wx_infos/", response_model=List[schemas.WXInfo])
def read_wx_infos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    wx_infos = crud.get_wx_infos(db, skip=skip, limit=limit)
    return wx_infos
