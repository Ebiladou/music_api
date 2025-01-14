from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    email: str
    username: str
    id: int

class UserInDB(User):
    hashed_password: str

class Login_user (BaseModel):
    email : str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class Playlist(BaseModel):
    name: str
    description: str | None = None
    is_public: bool | None = None
    user_id: int | None = None

class PlaylistResponse(BaseModel):
    name: str
    description: str
    created_by: str
    created_at: datetime 