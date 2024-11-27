import os
from dotenv import load_dotenv
from aiogram.types import Message, BotCommand
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram import Bot, Dispatcher, Router, F
from src.database.postgres_service import PostgresManager
from src.database.database import init_db
import asyncio

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
dp = Dispatcher()
router = Router()
bot = Bot(token=API_TOKEN)


@dp.startup.register
async def on_startup():
    commands = [
        BotCommand(command="/start", description="Start using the bot"),
        BotCommand(command="/help", description="About me")
    ]
    await bot.set_my_commands(commands)


@router.message(Command(commands=['start']))
async def start_command_handler(message: Message):
    telegram_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    bio = "Telegram user"
    await message.answer(f"Welcome back, {username}!")


async def main():
    dp.include_router(router)
    await bot.delete_webhook()
    await dp.start_polling(bot)


asyncio.run(main())
