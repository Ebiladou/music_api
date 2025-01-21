from fastapi import APIRouter, Response, status, HTTPException, Depends
from database import cursor, conn
from schema import User, UserResponse
from utils import hash_password
from oauth import verify_token 
from typing import List

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def get_users(current_user: User = Depends(verify_token)):
    cursor.execute(" SELECT * FROM users ")
    user_details = cursor.fetchall()
    users = [
        {"email": row['email'], "username": row['username'], "id": row['id']}
        for row in user_details
    ]
    return users

@router.post("/users/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup_user(user: User):
    hashed_password = hash_password(user.password)
    cursor.execute (" INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING * ", (user.username, user.email, hashed_password))
    new_user = cursor.fetchone()
    conn.commit()
    result = {"email": new_user['email'], "username": new_user['username'], "id": new_user['id']}
    return result

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, current_user: User = Depends(verify_token)):
    cursor.execute (" DELETE FROM users WHERE id = %s RETURNING * ", (user_id, ))
    deleted_user = cursor.fetchone()
    conn.commit()

    if deleted_user == None:
        raise HTTPException(status_code=404, detail=f"User {user_id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: int, user: User, current_user: User = Depends(verify_token)):
    hashed_password = hash_password(user.password)
    cursor.execute (" UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s RETURNING *", (user.username, user.email, hashed_password, str(user_id)))
    updated_user = cursor.fetchone()
    conn.commit()
    
    if updated_user == None:
        raise HTTPException(status_code=404, detail=f"User {user_id} does not exist")
    
    user = {"email": updated_user['email'], "username": updated_user['username'], "id": updated_user['id']}
    return user 

@router.get("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def getone_user(user_id: int, current_user: User = Depends(verify_token)):
    cursor.execute(" SELECT * FROM users WHERE id = %s ", [user_id], binary=True)
    single_user = cursor.fetchone()

    if single_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = {"email": single_user['email'], "username": single_user['username'], "id": single_user['id']}
    return user  