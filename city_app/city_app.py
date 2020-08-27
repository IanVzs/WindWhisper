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


@router.post("/citys/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_email(db, email=city.email)
    if db_city:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_city(db=db, city=city)


@router.get("/citys/", response_model=List[schemas.City])
def read_citys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    citys = crud.get_citys(db, skip=skip, limit=limit)
    return citys

@router.get("/citys/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.post("/citys/{city_id}/alarm_infos/", response_model=schemas.AlarmInfo)
def create_item_for_city(
    city_id: int, wx_info: schemas.AlarmInfoCreate, db: Session = Depends(get_db)
):
    return crud.create_city_item(db=db, wx_info=wx_info, city_id=city_id)


@router.get("/alarm_infos/", response_model=List[schemas.AlarmInfo])
def read_alarm_infos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alarm_infos = crud.get_alarm_infos(db, skip=skip, limit=limit)
    return alarm_infos
