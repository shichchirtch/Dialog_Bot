import asyncio
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedMultiselect, ManagedRadio
from aiogram_dialog.api.entities.modes import ShowMode
from bot_instans import dp, bot_storage_key
from bot_base import users_db
import pickle


async def radio_button_clicked(callback: CallbackQuery,
                               radio: ManagedRadio,
                               dialog_manager: DialogManager, *args, **kwargs):
    selected_language = radio.get_checked()
    state = dialog_manager.middleware_data["state"]
    lan_dict = {'1': 'English', '2': 'Русский', '3': "Deutsch"}
    await state.update_data(lan=lan_dict[selected_language])
    us_dict = await state.get_data()
    await asyncio.sleep(1)
    await callback.message.answer(f"Вы выбрали:  <b>{us_dict['lan']}</b>")
    await asyncio.sleep(1)
    dialog_manager.show_mode = ShowMode.SEND
    await dialog_manager.next()


async def radio_spam_button_clicked(callback: CallbackQuery,
                                    radio: ManagedRadio,
                                    dialog_manager: DialogManager, *args, **kwargs):
    temp_dict = {'1': 'Ну и ладно', '2': 'Очень хорошо'}
    await callback.message.answer(f"{temp_dict[callback.data[-1]]}")
    dialog_manager.show_mode = ShowMode.SEND
    await dialog_manager.next()


async def category_filled(callback: CallbackQuery, checkbox: ManagedMultiselect, dialog_manager: DialogManager, *args,
                          **kwargs):
    choose = checkbox.get_checked()
    dialog_dict = dialog_manager.dialog_data
    dialog_dict['skills'] = choose


async def on_confirm_clicked(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, *args, **kwargs):
    selected_skills = dialog_manager.dialog_data.get('skills', [])
    if selected_skills:
        await dialog_manager.next()  # Переход к следующему окну
    else:
        await callback.message.answer("Выберите хотя бы один скил", show_alert=True)


async def button_skolko(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    await callback.message.answer(f'Количество запусков бота {len(users_db)}')
    await dialog_manager.done()  # выход из режима админа


async def button_get_ankest(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    bot_dict = await dp.storage.get_data(key=bot_storage_key)  # Получаю словарь бота
    if len(bot_dict):
        for anketa in bot_dict.values():
            await callback.message.answer_photo(photo=anketa.foto_id, caption=anketa.description)
            await asyncio.sleep(0.2)
    else:
        await callback.message.answer(f'У бота нет анкет')
    await dialog_manager.done()  # выход из режима админа


async def button_zagruz_db(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    # bot_dict = await dp.storage.get_data(key=bot_storage_key)  # Получаю словарь бота
    with open('save_db.pkl', 'rb') as file:
        recover_base = pickle.load(file)
        await dp.storage.set_data(key=bot_storage_key, data=recover_base)
    await callback.message.answer('База данных успешно загружена !')
    await dialog_manager.done()  # выход из режима админа


async def button_save_db(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    bot_dict = await dp.storage.get_data(key=bot_storage_key)  # Получаю словарь бота
    with open('save_db.pkl', 'wb') as file:
        pickle.dump(bot_dict, file)
    await callback.message.answer('База данных успешно записана !')
    await dialog_manager.done()  # выход из режима админа
