from aiogram_dialog import Dialog, Window
from bot_instans import ADMIN
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Row, Group, Column
from callback_dialogs import (button_skolko, button_get_ankest, button_save_db, button_zagruz_db)


admin_dialog = Dialog(
    Window(
        Const('Возможные дейсвтия'),
        Group(
            Column(
                Button(
                    text=Const('Сколько запустило'),
                    id='skolko',
                    on_click=button_skolko),
                Button(
                    text=Const('Показать все анкеты'),
                    id='get_ankets_collection',
                    on_click=button_get_ankest),
            ),
            Row(
                Button(
                    text=Const('Загрузить БД'),
                    id='zagruz_bd',
                    on_click=button_zagruz_db),
                Button(
                    text=Const('Сохранить БД'),
                    id='save_bd',
                    on_click=button_save_db),
            ),
        ),
        state=ADMIN.first,
    ),
)













