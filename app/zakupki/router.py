from fastapi import APIRouter
from app.zakupki.zakupki_parser import get_new_data


router = APIRouter(prefix="/zakupki")


@router.get("/get_data")
async def get_new():
    return await get_new_data()
