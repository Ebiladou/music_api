from fastapi import FastAPI
from routers import user, auth, playlists

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(playlists.router)

@app.get("/")
def read():
    return {"users": "Welcome to the music API"}