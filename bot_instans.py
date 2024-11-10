from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import StorageKey, MemoryStorage
from aiogram.fsm.state import State, StatesGroup


aio_storage = MemoryStorage()

class FSM_ST(StatesGroup):
    start = State()  # FSM_ST:start
    spam = State()
    basic = State()
    vacancies = State()

class ANKETA(StatesGroup):
    name = State()
    mail = State()
    skills = State()
    foto = State()
    finish = State()
    load_foto= State()
    classic_handler = State()

class VAC(StatesGroup):
    empty = State()
    full = State()

class ADMIN(StatesGroup):
    first = State()


BOT_TOKEN = '6471784185:AAEWakBbPrU-bKGGanxahUq__ZbyZ1s8dBI'

bot = Bot(token=BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

bot_storage_key = StorageKey(bot_id=bot.id, user_id=bot.id, chat_id=bot.id)

dp = Dispatcher(storage=aio_storage)
