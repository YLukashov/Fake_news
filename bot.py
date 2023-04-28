from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, Message
import asyncio
from aiogram.dispatcher.filters import Text

from config import TOKEN
import news_check
import top_authors
import mailing
import add_author

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class TelegrammError(Exception):
    """Класс исключения."""


def check_tokens():
    """Проверяет доступность переменных окружения."""
    if TOKEN is None:
        raise TelegrammError('API_TOKEN недоступен')


async def send_start_menu(message: types.Message):
    but1 = KeyboardButton(text="проверить новость")
    but2 = KeyboardButton(text="авторы с наибольшем уровнем доверия")
    but3 = KeyboardButton(text="рассылка")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(but1).add(but2).add(but3)
    # Отправка сообщение с клавиатурой
    await bot.send_message(message.chat.id, "Привет! Выбери кнопку:", reply_markup=keyboard)


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message_handler(commands="start")
async def process_start_command(message: types.Message):
    asyncio.get_running_loop().create_task(send_start_menu(message))


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")


# Класс со состояниями
class ms_to_users(StatesGroup):
    text = State()


# событие на сообщение: проверить новость
@dp.message_handler(Text(equals="проверить новость"))
async def process_help_command(message: Message):
    await message.answer('Отправь в чат свою новость. Формат: автор@@@новость. Если неизвестен автор, указывать nn')
    await ms_to_users.text.set()


# Сюда приходит ответ с именем
@dp.message_handler(state=ms_to_users.text)
async def process_name(message: types.Message, state: FSMContext):
    await message.answer('Новость обрабатывается')
    name_author, text_pred = message.text.split("@@@")
    if news_check.pred(text_pred):
        await message.answer('Новость скорее всего правдивая')
        add_author.add_user(name_author, 1)
    else:
        await message.answer('Новость скорее всего ложная')
        add_author.add_user(name_author, 0)
    await ms_to_users.next()


# событие на сообщение: проверить новость
@dp.message_handler(Text(equals="авторы с наибольшем уровнем доверия"))
async def process_help_command(message: Message):
    auth = top_authors.checklist()
    for i in auth:
        await message.answer(f'''Имя: {i[0]}; Количество правдивых новостей: {i[1][0]}''')


# событие на сообщение: проверить новость
@dp.message_handler(Text(equals="рассылка"))
async def process_help_command(message: Message):
    if mailing.check_user_in_base(message.chat.id):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Отписаться"))
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Подписаться"))
    await bot.send_message(message.chat.id, "Выбери действие", reply_markup=keyboard)


@dp.message_handler(Text(equals="Подписаться"))
async def process_help_command(message: Message):
    mailing.add_user(message.chat.id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Отписаться"))
    await bot.send_message(message.chat.id, "Успешно!", reply_markup=keyboard)


@dp.message_handler(Text(equals="Отписаться"))
async def process_help_command(message: Message):
    mailing.del_user(message.chat.id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Отписаться"))
    await bot.send_message(message.chat.id, "Успешно!", reply_markup=keyboard)


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    check_tokens()
    executor.start_polling(dp)
