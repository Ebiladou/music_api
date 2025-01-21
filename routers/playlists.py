from fastapi import APIRouter, Response, status, HTTPException, Depends
from database import cursor, conn
from oauth import verify_token 
from schema import Playlist, User, PlaylistResponse, UpdatedResponse
from typing import List

router = APIRouter()

@router.post("/playlists", status_code=status.HTTP_201_CREATED)
def create_playlist(playlist: Playlist, current_user: User = Depends(verify_token)):
    user_id = current_user[3]
    cursor.execute(" INSERT INTO playlists (name, description, is_public, user_id) VALUES (%s, %s, %s, %s) RETURNING * ", (playlist.name, playlist.description, playlist.is_public, user_id))
    new_playlist = cursor.fetchone()
    conn.commit()
    return new_playlist

@router.get("/playlists", response_model=List[PlaylistResponse])
def get_playlists(current_user: User = Depends(verify_token)):
    cursor.execute("SELECT playlists.name, playlists.description, playlists.is_public,  playlists.created_at, users.username AS created_by FROM playlists JOIN users ON playlists.user_id = users.id WHERE playlists.is_public = TRUE")
    playlists = cursor.fetchall()
    result = [
        {
            "name": row[0],
            "description": row[1],
            "created_at": row[3],
            "created_by": row[4],
        }
        for row in playlists
    ] 
    return result 

@router.put("/playlists/{id}", response_model=UpdatedResponse, status_code=status.HTTP_202_ACCEPTED)
def update_playlist(id: int, playlist: Playlist, current_user: User = Depends(verify_token)):
    cursor.execute("UPDATE playlists SET name = %s, description = %s, is_public = %s WHERE id = %s RETURNING *", (playlist.name, playlist.description, playlist.is_public, id))
    updated_playlist = cursor.fetchone()
    conn.commit()
    if updated_playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")
    result = {
        "id": updated_playlist[0],
        "name": updated_playlist[1],
        "description": updated_playlist[2],
        "updated_at": updated_playlist[6],
    }

    return result

@router.get("/playlists/{id}", response_model=PlaylistResponse)
def get_playlist(id: int, current_user: User = Depends(verify_token)):
    cursor.execute("SELECT playlists.id, playlists.name, playlists.description, playlists.is_public, playlists.created_at, users.username AS created_by FROM playlists JOIN users ON playlists.user_id = users.id WHERE playlists.id = %s", (id,))
    playlist = cursor.fetchone()

    print(playlist)
    
    if playlist is None:
        raise HTTPException(status_code=404, detail="Playlist not found")
    result = {
        "name": playlist[1],
        "description": playlist[2],
        "created_at": playlist[4],
        "created_by": playlist[5],
    }

    return result