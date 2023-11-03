

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "Hi! This is my first python app made with using API :P"