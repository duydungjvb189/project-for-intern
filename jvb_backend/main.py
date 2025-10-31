from fastapi import FastAPI
from routers import auth_route, item_route, user_route

app = FastAPI()

app.include_router(user_route.router)
app.include_router(auth_route.router)
app.include_router(item_route.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Auth API Demo!"}

@app.get("/ping")
def ping():
    return {"message": "pong"}