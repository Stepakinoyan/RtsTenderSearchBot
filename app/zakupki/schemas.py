from pydantic import BaseModel
from datetime import date


class Zakupki(BaseModel):
    price: str
    description: str
    url: str
    post_date: date
