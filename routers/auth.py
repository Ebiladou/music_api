from fastapi import APIRouter, status, HTTPException
from database import cursor, conn
from schema import Login_user
import utils

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login (userlog: Login_user):
    cursor.execute (" SELECT * FROM users WHERE email = %s ", (userlog.email,))
    loged_user = cursor.fetchone()

    if loged_user == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="invalid username or password")

    if not utils.verify_password(userlog.password, loged_user.password):
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="invalid username or password")
    
    return {"token": "token sent"}