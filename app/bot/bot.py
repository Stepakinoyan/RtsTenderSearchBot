from aiogram import BaseMiddleware, Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import settings
import requests
import logging
import asyncio
import sys




TOKEN = settings.TOKEN
trigger = CronTrigger(year="*", month="*", day="*", hour="18", minute="0", second="0")
api_router = Router(name='API')

class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self,handler,event,data):
        data["scheduler"] = self._scheduler
        return await handler(event, data)

async def get_data_from_api(message: Message, bot: Bot):
    response = requests.get("http://localhost:9000/zakupki/get_data")
    if len(response.json()) == 0:
        pass
    else:
        for item in response.json():
            await bot.send_message(-1002037411048, f"""Цена: {item.get("price")}\nСсылка: {item.get("url")}\nОписание: {item.get("description")}\n""")


@api_router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot):
    await bot.send_message(-1002037411048 ,f"Hello, {message.chat.id}!")


@api_router.message(Command(commands=["remind"]))
async def get_data_handler(message: Message, bot: Bot, scheduler: AsyncIOScheduler):
        await bot.send_message(-1002037411048,
            text="Бот будет следить за изменениями каждый день в 18:00 вечера"
        )
        scheduler.add_job(get_data_from_api , trigger=trigger, kwargs={"bot": bot, 'message': message})

async def main():
    scheduler = AsyncIOScheduler(timezone='Asia/Yakutsk')
    scheduler.start()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.update.middleware(
        SchedulerMiddleware(scheduler=scheduler),
    )
    dp.include_routers(api_router)
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())