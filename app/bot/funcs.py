from aiogram import Bot
from httpx import AsyncClient


async def get_data_from_api(bot: Bot):
    async with AsyncClient() as client:
        response = client.get("http://search-api:8000/zakupki/get_data")
    if len(response.json()) == 0:
        pass
    else:
        for item in response.json():
            await bot.send_message(
                chat_id="@rtstendermonitoring",
                text=f"""Цена: {item.get("price")}\nСсылка: {item.get("url")}\nОписание: {item.get("description")}\n""",
            )
