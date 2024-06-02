from aiogram import BaseMiddleware, Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from httpx import AsyncClient
import logging
import asyncio
import sys


trigger = CronTrigger(year="*", month="*", day="*", hour="18", minute="0", second="0")
api_router = Router(name="API")


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self, handler, event, data):
        data["scheduler"] = self._scheduler
        return await handler(event, data)


async def get_data_from_api(message: Message, bot: Bot):
    async with AsyncClient() as client:
        response = client.get("http://localhost:9000/zakupki/get_data")
    if len(response.json()) == 0:
        pass
    else:
        for item in response.json():
            await bot.send_message(
                chat_id="@rtstendermonitoring",
                text=f"""Цена: {item.get("price")}\nСсылка: {item.get("url")}\nОписание: {item.get("description")}\n""",
            )


@api_router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot):
    await bot.send_message(
        chat_id="@rtstendermonitoring", text=f"Hello, {message.chat.id}!"
    )


@api_router.message(Command(commands=["remind"]))
async def get_data_handler(message: Message, bot: Bot, scheduler: AsyncIOScheduler):
    await bot.send_message(
        chat_id="@rtstendermonitoring",
        text="Бот будет следить за изменениями каждый день в 18:00 вечера",
    )
    scheduler.add_job(
        get_data_from_api, trigger=trigger, kwargs={"bot": bot, "message": message}
    )


async def main():
    scheduler = AsyncIOScheduler(timezone="Asia/Yakutsk")
    scheduler.start()
    bot = Bot(
        "6889825024:AAHkKaY4sWNX5EGsZ2tRnckQzv1h5r8fORE", parse_mode=ParseMode.HTML
    )
    dp = Dispatcher()
    dp.update.middleware(
        SchedulerMiddleware(scheduler=scheduler),
    )
    dp.include_routers(api_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
