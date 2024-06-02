from fastapi import FastAPI
from app.zakupki.router import router

app = FastAPI()
app.include_router(router)
