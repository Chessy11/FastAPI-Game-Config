from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.db import engine
from app.routers import (
    chat_route, choose_bonus_route, 
    free_spin_bonus_route, game_route, 
    line_route, reel_route, symbol_route,
    user_route, cloudinary_route, adapter_route
    )
from app.models import models
from cloudinary import config
import os

load_dotenv()

if not all([os.getenv("CLOUDINARY_CLOUD_NAME"), os.getenv("CLOUDINARY_API_KEY"), os.getenv("CLOUDINARY_API_SECRET")]):
    raise Exception("Cloudinary credentials are not set properly")

config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


app = FastAPI(root_path="/")

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(game_route.router)
app.include_router(symbol_route.router)
app.include_router(free_spin_bonus_route.router)
app.include_router(choose_bonus_route.router)
app.include_router(reel_route.router)
app.include_router(user_route.router)
app.include_router(line_route.router)
app.include_router(chat_route.router)
app.include_router(cloudinary_route.router)
app.include_router(adapter_route.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.GameModel.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.get("/health", tags=["health"])
async def root():
    return {"message": "OK"}
