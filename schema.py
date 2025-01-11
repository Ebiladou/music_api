from pydantic import BaseModel

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