from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Query, BackgroundTasks

from route_class import TimedRoute, APIRouter
from . import crud, models, schemas
from .database import SessionLocal, engine
from helpers import api, parser, tools
from loggers import backtaskLog as logger

models.Base.metadata.create_all(bind=engine)

router = APIRouter(route_class=TimedRoute)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def write_rss_details(desc, url, db: Session=Depends(get_db)) -> int:
    logger.info(f"write_rss_details|{db}|{desc}|{url}")
    content = api.get(url)
    list_data = parser.list_rss(content)
    len_data = len(list_data)
    logger.info(f"write_rss_count|{desc}|{tools.get_now()}|all_{len_data}")
    counter = 0
    for data in list_data:
        data = data
        # TODO 
        rss_article = schemas.ArticlesCreate({})
        sign = crud.create_rss_article(db, rss_article)
        if sign:
            counter += 1
    logger.info(f"all_{len_data}|success_{counter}|failed_{len_data-counter}")
    return counter

@router.post("/rss/save_details", response_model=schemas.Status)
async def create_rss_details(srtdesc: str = Query(..., min_length=3), rss: schemas.RssBase=None, db: Session = Depends(get_db),
    background_tasks: BackgroundTasks=None):
    rst = schemas.Status()
    # import pdb; pdb.set_trace()

    # db_rss = crud.get_rss_by_srtdesc(db, srtdesc=srtdesc)
    # if db_rss:
    #     raise HTTPException(status_code=400, detail="This rss already registered")
    # rss = rss.dict()
    # rsscreate = schemas.RssCreate(**{**rss, "srtdesc": srtdesc})
    # crud.create_rss(db=db, rss=rsscreate)
    desc, url = srtdesc, rss.url
    background_tasks.add_task(write_rss_details, desc, url)
    rst.status = 0
    return rst.dict()

@router.post("/rss/title/", response_model=schemas.Rss)
def create_rss(srtdesc: str = Query(..., min_length=3), rss: schemas.RssBase=None, db: Session = Depends(get_db)):
    db_rss = crud.get_rss_by_srtdesc(db, srtdesc=srtdesc)
    if db_rss:
        raise HTTPException(status_code=400, detail="This rss already registered")
    rss = rss.dict()
    rsscreate = schemas.RssCreate(**{**rss, "srtdesc": srtdesc})
    return crud.create_rss(db=db, rss=rsscreate)


@router.get("/rss/list_title", response_model=List[schemas.RssItem])
def read_rsses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rss = crud.get_rsses(db, skip=skip, limit=limit)
    return rss

@router.get("/rss/get/{rss_id}", response_model=schemas.Rss)
def read_rss(rss_id: int, db: Session = Depends(get_db)):
    db_rss = crud.get_rss(db, rss_id=rss_id)
    if db_rss is None:
        raise HTTPException(status_code=404, detail="Rss not found")
    return db_rss
