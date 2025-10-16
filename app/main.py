# app/main.py
from fastapi import FastAPI, HTTPException, status, Response
from .schemas import User 

app = FastAPI()
users: list[User] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/users")
def get_users():
    return users


@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for u in users:
        if u.user_id == user_id:
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")


@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    # 409 if duplicate user_id
    if any(u.user_id == user.user_id for u in users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")
    users.append(user)
    return user



@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.user_id == user_id:
            users.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")