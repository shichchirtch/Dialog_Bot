import asyncio
from aiogram.types import Message
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog import DialogManager, ShowMode
from anketa_class import Anketa
from bot_instans  import dp, bot_storage_key

skills_dict = {
        '1':"Redis",
        '2':"PostgreSQL",
        '3':"aiogram-dialog",
        '4':"miniapp",
        '5':"Интеграция с openAI",
        '6':"scheduler",
        '7':"BS4",
        '8':"pandas",
        '9':"Jenkins",
        '10':"react"}


# Хэндлер, который сработает, если пользователь ввел корректный возраст
async def correct_name_handler(message: Message, widget: ManagedTextInput,
                               dialog_manager: DialogManager, name: str) -> None:
    state = dialog_manager.middleware_data["state"]
    us_dict = await state.get_data()
    us_dict['name'] = name
    await state.set_data(us_dict)
    await message.answer(text=f'Отлично, <b>{name.capitalize()}</b>')
    await asyncio.sleep(1)
    dialog_manager.show_mode = ShowMode.SEND
    await message.delete()
    await dialog_manager.next()


# Хэндлер, который сработает на ввод некорректного возраста
async def error_name_handler(message: Message,widget: ManagedTextInput,dialog_manager: DialogManager,error: ValueError):
    await message.answer(text='Вы ввели некорректное имя. Попробуйте еще раз')
    await asyncio.sleep(1)


async def correct_mail_handler(
        message: Message, widget: ManagedTextInput,
        dialog_manager: DialogManager, mail: str) -> None:
    state = dialog_manager.middleware_data["state"]
    us_dict = await state.get_data()
    us_dict['mail'] = mail
    await state.set_data(us_dict)
    await message.answer(text=f'Адрес, <b>{mail}</b> записан')
    await asyncio.sleep(1)
    dialog_manager.show_mode = ShowMode.SEND
    await message.delete()
    await dialog_manager.next()


# Хэндлер, который сработает на ввод некорректного возраста
async def error_mail_handler(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, error: ValueError):
    await message.answer(text='Вы ввели некорректное адрес электронной почты. Попробуйте еще раз')
    await asyncio.sleep(1)


async def on_photo_sent(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    # Получаем ID фото
    foto_id = message.photo[-1].file_id  # Берем последнее фото (наибольшего размера)
    state = dialog_manager.middleware_data["state"]
    us_dict = await state.get_data()
    us_name = us_dict['name']
    us_mail = us_dict['mail']
    us_skills = dialog_manager.dialog_data['skills']
    print('us_skills = ', us_skills)  # ['4', '5']
    us_dict['foto_id'] = foto_id
    skill = ''
    for index in us_skills:
        if index in skills_dict:
            skill+=f'- {skills_dict[index]}\n\n'
    us_dict['skills'] = skill
    new_anketa = Anketa(foto_id=foto_id, description=f'✅  <b>Анкета Заявителя</b>\n\nИмя: <b>{us_name}</b>\n\nemail: <b>{us_mail}</b>\n\n'
                                                     f'Профессиональные навыки:   🔥\n\n{skill}\n\n🔷')
    await state.set_data(us_dict)
    bot_dict = await dp.storage.get_data(key=bot_storage_key)  # Получаю словарь бота
    bot_dict[message.from_user.id] = new_anketa  # Записываю боту анкету юзера по телеграм id
    await dp.storage.update_data(key=bot_storage_key, data=bot_dict)  # перезаписываю словарь бота
    await message.delete()
    await dialog_manager.next()


async def message_not_foto_handler(message: Message, widget: MessageInput,
        dialog_manager: DialogManager) -> None:
    dialog_manager.show_mode = ShowMode.NO_UPDATE
    await message.answer('*** Пришлите мне ваше фото 👦')









