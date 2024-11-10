from aiogram_dialog import Dialog, StartMode, Window
from getters import get_languages, get_spam,  get_skills, get_anketa
from bot_instans import FSM_ST, ANKETA, VAC
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row,  Column, Multiselect, Radio, Next, Start
from aiogram_dialog.widgets.input import TextInput,  MessageInput
from aiogram_dialog.widgets.media import  DynamicMedia
from aiogram.types import ContentType
from callback_dialogs import (radio_button_clicked, category_filled,
                              radio_spam_button_clicked, on_confirm_clicked)
import operator
from lexicon import *
from dialog_functions import name_check, mail_check
from input_handlers import (correct_name_handler, error_name_handler,
                            error_mail_handler, correct_mail_handler, on_photo_sent,
                            message_not_foto_handler)

start_dialog = Dialog(
    Window(
        Const('Выберите язык интрефейса 👇'),
        Row(
            Radio(
                checked_text=Format('🔘 {item[0]}'),
                unchecked_text=Format('⚪️ {item[0]}'),
                id='radio_lang',
                item_id_getter=operator.itemgetter(1),
                items="languages",
                on_state_changed=radio_button_clicked
            ),
        ),
        state=FSM_ST.start,
        getter=get_languages
    ),

    Window(
        Const('Вы хотите получать сообщения от бота ?'),
        Row(
            Radio(
                checked_text=Format('🔘 {item[0]}'),
                unchecked_text=Format('⚪️ {item[0]}'),
                id='spam_window',
                item_id_getter=operator.itemgetter(1),
                items="spam_data",
                on_state_changed=radio_spam_button_clicked,
            ),
        ),
        state=FSM_ST.spam,
        getter=get_spam
    ),
    Window(
        Format(basic_menu),
        Row(
            Start(Const('Актуальные вакансии'),
                  id='see_stelle_button',
                  state=VAC.empty),
            Start(Const('Заполнить анкету'),
                  id='anketa_button',
                  state=ANKETA.name),
        ),
        state=FSM_ST.basic,
    ),
)

anketa_dialog = Dialog(
    Window(
        Const('Введите ваше имя'),
        TextInput(
            id='name_input',
            type_factory=name_check,
            on_success=correct_name_handler,
            on_error=error_name_handler,
        ),
        state=ANKETA.name,
    ),
    Window(
        Const('Введите адрес вашей электронной почты'),
        TextInput(
            id='mail_input',
            type_factory=mail_check,
            on_success=correct_mail_handler,
            on_error=error_mail_handler,
        ),
        state=ANKETA.mail,
    ),

Window( # Окно показывает виджет с мультиселектом
       Const(text='Отметьте свои скилы'),
        Column(
            Multiselect(
                checked_text=Format('[✔️] {item[0]}'),
                unchecked_text=Format('[  ] {item[0]}'),
                id='multi_topics',
                item_id_getter=operator.itemgetter(1),
                items="skills",
                min_selected=1,
                max_selected=6,
                on_state_changed=category_filled
            ),
            Button(Const("Подтвердить"), id="confirm_button", on_click=on_confirm_clicked)
        ),
        state=ANKETA.skills,
        getter=get_skills
    ),


    Window(
        Const('Отправьте фото в ответ'),
        Next(Const("Загрузить фото"),
             id="send_foto"),
        state=ANKETA.load_foto,
    ),

    Window(  # Окно принимающее фото
        Const(text='Пришлите мне Ваше Фото 👦'),
        MessageInput(
            func=on_photo_sent,
            content_types=ContentType.PHOTO,
        ),
        MessageInput(
            func=message_not_foto_handler,
            content_types=ContentType.ANY,
        ),
        state=ANKETA.classic_handler
    ),

    Window(
        Const('Данные приняты'),
        Next(Const('Сформировать анкету'), id='next2'),
        state=ANKETA.foto,
    ),

    Window(
        Format(text='{capt}'),
        DynamicMedia("foto"),
        Start(Const('В основное меню ▶️'),
              id='go_to_basic',
              state=FSM_ST.basic,
              mode=StartMode.RESET_STACK),
        state=ANKETA.finish,
        getter=get_anketa
    ),
)

vacancies = Dialog(
    Window(
        Const('В базе пока нет вакансий'),
        Start(Const('В основное меню ▶️'),
              id='go_to_basic',
              state=FSM_ST.basic,
              mode=StartMode.RESET_STACK),
        state=VAC.empty,
    ), )
