import uvicorn
from dz6.shop import shop
import datetime
from fastapi import FastAPI, HTTPException
import dz6.database as db
from passlib.context import CryptContext
from asyncio import run
from typing import List
from dz6.tools import get_password_hash
from dz6.models import ChangeUser, ChangeOrder, ChangeProduct, AddUser, AddOrder, AddProduct
from random import randint


app = FastAPI()
# app.mount("/shop/", shop)
app.mount("/shop/", shop)

@app.get("/")
async def root():
    return {"message": "Главная страница"}

@app.on_event("startup")
async def startup():
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=False)