from fastapi import APIRouter
from app.zakupki.zakupki_parser import get_new_data


router = APIRouter(prefix="/zakupki")

@router.get("/get_data")
def get_new():
    return get_new_data()