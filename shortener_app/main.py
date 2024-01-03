import secrets

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import models,schemas
from .database import SessionLocal, engine
from . import crud, models, schemas

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="your provided URL is not valid")

    # chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # key = "".join(secrets.choice(chars) for each in range(5))
    # secret_key = "".join(secrets.choice(chars) for each in range(8))
    # db_url = models.URL (
    #     target_url=url.target_url, key=key, secret_key=secret_key
    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db.url.key
    db_url.admin_url = db.url.secret_key

    return db_url

@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
    ):
    # db_url = (
    #     db.query(models.URL)
    #     .filter(models.URL.key == url_key, models.URL.is_active)
    #     .first()
    if db_url:= crud.create_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

#    return f"Create database entry for: {url.target_url}"
# @app.get("/")
# def read_root():
#     return "Hi! This is my first python app made with using API :P"