from fastapi import FastAPI
from routers import user
import database

app = FastAPI()

app.include_router(user.router)

@app.get("/")
def read():
    return {"users": "Welcome to the music API"}