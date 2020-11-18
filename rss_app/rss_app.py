from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
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


@router.post("/rss/", response_model=schemas.Rss)
def create_rss(srtdesc: str = Query(..., min_length=3), rss: schemas.RssBase=None, db: Session = Depends(get_db)):
    db_rss = crud.get_rss_by_id(db, srtdesc=srtdesc)
    if db_rss:
        raise HTTPException(status_code=400, detail="This rss already registered")
    rss = rss.dict()
    rsscreate = schemas.RssCreate(**{**rss, "srtdesc": srtdesc})
    return crud.create_rss(db=db, rss=rsscreate)


@router.get("/rss/", response_model=List[schemas.Rss])
def read_rss(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rss = crud.get_rsses(db, skip=skip, limit=limit)
    return rss

@router.get("/rss/{rss_id}", response_model=schemas.Rss)
def read_rss(rss_id: int, db: Session = Depends(get_db)):
    db_rss = crud.get_rss(db, rss_id=rss_id)
    if db_rss is None:
        raise HTTPException(status_code=404, detail="Rss not found")
    return db_rss