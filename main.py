import asyncio
import uuid
from urllib.parse import urlencode

import aiogram
import aiohttp
from aiogram import Dispatcher
from aiogram.filters import CommandStart, CommandObject

import settings

bot = aiogram.Bot(token=settings.BOT_TOKEN)

dp = Dispatcher()


@dp.message(CommandStart(deep_link=True))
async def deep_link(message: aiogram.types.Message, command: CommandObject):
    try:
        telegram_auth_request_id = uuid.UUID(command.args)
    except (ValueError, AttributeError):
        return

    query = {
        'telegram_auth_token': settings.TELEGRAM_AUTH_TOKEN,
        'telegram_auth_request_id': str(telegram_auth_request_id),
        'user_id': message.from_user.id,
        'username': message.from_user.username or message.from_user.first_name,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(f'{settings.TELEGRAM_AUTH_REQUEST_RESPONSE_URL}?{urlencode(query)}') as response:
            response.raise_for_status()

    await message.answer(f'Вы успешно авторизованы. Вернитесь в приложение.')


@dp.message(CommandStart())
async def deep_link(message: aiogram.types.Message):
    query = {
        'telegram_auth_token': settings.TELEGRAM_AUTH_TOKEN,
        'user_id': message.from_user.id,
        'username': message.from_user.username or message.from_user.first_name,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(f'{settings.TELEGRAM_AUTH_GET_URL_URL}?{urlencode(query)}') as response:
            response.raise_for_status()

            url = (await response.json())['front_authorization_url']

    await message.answer(
        f'Вы успешно авторизованы. Нажмите кнопку, чтобы перейти в приложение.',
        reply_markup=aiogram.types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    aiogram.types.InlineKeyboardButton(
                        text='Перейти в приложение',
                        web_app=aiogram.types.WebAppInfo(url=url),
                    ),
                ],
            ],
        ),
    )


async def main():
    await dp.start_polling(
        bot,
        allowed_updates=['message'],
    )

if __name__ == "__main__":
    asyncio.run(main())
