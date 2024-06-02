from fastapi import FastAPI
from zakupki.router import router

app = FastAPI()
app.include_router(router)
