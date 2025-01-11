from fastapi import APIRouter, status, HTTPException, Depends
from database import cursor, conn
from schema import Token
import utils, oauth
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    cursor.execute("SELECT * FROM users WHERE username = %s", (form_data.username,))
    user = cursor.fetchone()
   
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid username or password")
    
    if not utils.verify_password(form_data.password, user[2]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid username or password")
    
    access_token = oauth.create_access_token(data={"sub": user[1]})
    
    return {"access_token": access_token, "token_type": "bearer"}