import asyncio
import logging
from aiogram import BaseMiddleware, Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from funcs import get_data_from_api
from config import settings

logging.basicConfig(level=logging.INFO)
trigger = CronTrigger(year="*", month="*", day="*", hour="8", minute="0", second="0")
bot = Bot(settings.TOKEN)
dp = Dispatcher()


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self, handler, event, data):
        data["scheduler"] = self._scheduler
        return await handler(event, data)


@dp.message(CommandStart())
async def hello(message: types.Message):
    await bot.send_message(
        chat_id="@rtstendermonitoring", text=f"Hello, {message.from_user.full_name}!"
    )


@dp.message(Command("remind"))
async def get_data_handler(message: types.Message, scheduler: AsyncIOScheduler):
    await bot.send_message(
        chat_id="@rtstendermonitoring",
        text="Бот будет следить за изменениями каждый день в 18:00 вечера",
    )
    scheduler.add_job(
        get_data_from_api, trigger=trigger, kwargs={"bot": bot}
    )


async def main():
    scheduler = AsyncIOScheduler(timezone="Asia/Yakutsk")
    scheduler.start()

    dp.update.middleware(
        SchedulerMiddleware(scheduler=scheduler),
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())