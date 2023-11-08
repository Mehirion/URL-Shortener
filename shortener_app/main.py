import validators

from fastapi import FastAPI, HTTPException

from . import schemas

app = FastAPI()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

@app.post("/url")
def create_url(url: schemas.URLBase):
    if not validators.url(url.target_url):
        raise_bad_request(message="your provided URL is not valid")
    return f"Create database entry for: {url.target_url}"

# @app.get("/")
# def read_root():
#     return "Hi! This is my first python app made with using API :P"