from fastapi import APIRouter, status, HTTPException
from database import cursor, conn
from schema import Login_user
import utils, oauth

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login (userlog: Login_user):
    cursor.execute (" SELECT * FROM users WHERE email = %s ", (userlog.email,))
    loged_user = cursor.fetchone()
   
    if loged_user == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="invalid username or password")
    
    if not utils.verify_password(userlog.password, loged_user[2]):
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="invalid username or password")
    
    access_token = oauth.create_access_token(data={"sub": loged_user[0]})
    
    return {"access_token": access_token, "token_type": "bearer"}