from aiogram import Router
import asyncio
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from bot_base import user_dict, users_db
from filters import PRE_START, IS_ADMIN
from lexicon import *
from copy import deepcopy
from aiogram.fsm.context import FSMContext
from keyboards import pre_start_clava
from bot_instans import FSM_ST, ADMIN
from aiogram_dialog import  DialogManager, StartMode


ch_router = Router()

# @ch_router.message(F.photo)
# async def foto_id_geber_messages(message: Message):
#     data = message.photo[-1].file_id
#     print(data)


@ch_router.message(CommandStart(), PRE_START())
async def command_start_process(message:Message, dialog_manager: DialogManager, state:FSMContext):

    # if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict)
        await state.set_data({'foto_id':'', 'lan':'ru'})
        await message.answer(text=f'👋\n\n\<b>Привет, {message.from_user.first_name}!</b>\n'
               'Это бот для добавления персональной анкеты в базу данных анкет IT-профессий', reply_markup=ReplyKeyboardRemove())
        await dialog_manager.start(state=FSM_ST.start, mode=StartMode.RESET_STACK)





@ch_router.message(PRE_START())
async def before_start(message: Message, dialog_manager: DialogManager):
    prestart_ant = await message.answer(text='Klicken auf <b>start</b> !',
                                        reply_markup=pre_start_clava)
    # await dialog_manager.done()  # Здесь возникает ошибка

    await message.delete()
    await asyncio.sleep(3)
    await prestart_ant.delete()

@ch_router.message(Command('admin'), IS_ADMIN())
async def basic_menu_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ADMIN.first)
    await asyncio.sleep(1)
    await message.delete()


@ch_router.message(Command('basic_menu'))
async def basic_menu_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=FSM_ST.basic, mode=StartMode.RESET_STACK)

@ch_router.message(Command('help'))
async def basic_menu_start(message: Message, dialog_manager: DialogManager):
    await message.answer(text=help_text)
    await dialog_manager.start(state=FSM_ST.basic, mode=StartMode.RESET_STACK)

