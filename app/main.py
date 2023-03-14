from fastapi import FastAPI

from app.db import engine
from app.routers import GameConfigRoute
from app.models import Models

app = FastAPI()

app.include_router(GameConfigRoute.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Models.GameConfigModel.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.get("/health", tags=["health"])
async def root():
    return {"message": "OK"}
