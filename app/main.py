from fastapi import FastAPI

from app.db import engine
from app.routers import GameRoute, SymbolRoute, FreeSpinBonusRoute, ReelRoute, ChooseBonusRoute
from app.models import Models

app = FastAPI()

app.include_router(GameRoute.router)
app.include_router(SymbolRoute.router)
app.include_router(FreeSpinBonusRoute.router)
app.include_router(ChooseBonusRoute.router)
app.include_router(ReelRoute.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Models.GameModel.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.get("/health", tags=["health"])
async def root():
    return {"message": "OK"}
