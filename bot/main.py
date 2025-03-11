import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import BotCommand
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis

from config import BOT_TOKEN, REDIS_HOST, REDIS_PORT
from dialogs.comments import comments_dialog
from dialogs.tasks import tasks_dialog
from handlers import start, tasks

# Initialization of the bot and storage
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
storage = RedisStorage(
    redis=Redis(host=REDIS_HOST, port=REDIS_PORT, db=2),
    key_builder=DefaultKeyBuilder(with_destiny=True),
)
dp = Dispatcher(bot=bot, storage=storage, fsm_strategy=FSMStrategy.USER_IN_CHAT)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="tasks", description="Мои задачи"),
    ]
    await bot.set_my_commands(commands)


# The main function
async def main():
    dp.include_router(start.router)
    dp.include_router(tasks.router)
    dp.include_router(tasks_dialog)
    dp.include_router(comments_dialog)
    setup_dialogs(dp)

    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
