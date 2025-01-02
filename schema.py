from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str

class Login_user (BaseModel):
    email : str
    password: str