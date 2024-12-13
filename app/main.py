from fastapi import FastAPI
from app.routers import task, user
from app.backend.db import engine, Base
import uvicorn

app = FastAPI()


@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}


app.include_router(task.router)
app.include_router(user.router)

Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


