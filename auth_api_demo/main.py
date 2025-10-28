from fastapi import FastAPI
from routers import users, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Auth API Demo!"}

@app.get("/ping")
def ping():
    return {"message": "pong"}