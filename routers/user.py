from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Doe", "email": "jane@example.com"},
]


class User(BaseModel):
    name: str
    email: str


class UserID(BaseModel):
    id: int


@app.post("/users/")
async def create_user(user: User):
    new_user = {"id": len(users) + 1, "name": user.name, "email": user.email}
    users.append(new_user)
    return new_user


@app.get("/users/")
async def get_users():
    return users


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    existing_user = next((user for user in users if user["id"] == user_id), None)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    existing_user["name"] = user.name
    existing_user["email"] = user.email
    return existing_user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users.remove(user)
    return {"message": "User deleted Successfully"}
