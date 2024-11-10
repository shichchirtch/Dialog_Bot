from aiogram.types import ContentType
from aiogram_dialog import DialogManager
from aiogram.fsm.context import FSMContext
from aiogram_dialog.api.entities import MediaAttachment, MediaId



async def get_languages(dialog_manager: DialogManager, **kwargs):
    checked = dialog_manager.find('radio_lang').get_checked()  # Возвращает ключ в словаре language

    language = {
        '1': 'en',
        '2': 'ru',
        '3': 'de'
    }
    chosen_lang = language['2' if not checked else checked]
    lang = {
        'ru': {
            '1': '🇬🇧 Английский',
            '2': '🇷🇺 Русский',
            '3': '🇩🇪 Немецкий',
            'text': 'Выберите язык'
        },
        'en': {
            '1': '🇬🇧 English',
            '2': '🇷🇺 Russian',
            '3': '🇩🇪 German',
            'text': 'Choose language'
        },
        'fr': {
            '1': '🇬🇧 Englisch',
            '2': '🇷🇺 Russisch',
            '3': '🇩🇪 Deutsch',
            'text': 'Choisissez la langue'
        }
    }
    languages = [
        (f"{lang[chosen_lang]['1']}", '1'),
        (f"{lang[chosen_lang]['2']}", '2'),
        (f"{lang[chosen_lang]['3']}", '3')
    ]
    return {"languages": languages,
            'text': lang[chosen_lang]['text']}



async def get_spam(dialog_manager: DialogManager, **kwargs):
    spam = [('🤢','1'), ('😃','2')]
    check_info = dialog_manager.dialog_data.get('spam_wahl', '')
    return {"spam_data": spam, 'spam_wahl':check_info}

async  def get_anketa(dialog_manager: DialogManager, state:FSMContext, **kwargs):
    us_dict = await state.get_data()
    image_id = us_dict['foto_id']
    us_name = us_dict['name']
    us_mail = us_dict['mail']
    skill = us_dict['skills']
    captutra = (f'✅  <b>Анкета Заявителя</b>\n\nИмя: <b>{us_name}</b>\n\nemail: <b>{us_mail}</b>\n\n'
                f'Профессиональные навыки:   🔥\n\n{skill}\n\n🔷')
    image = MediaAttachment(ContentType.PHOTO, file_id=MediaId(image_id))
    return {'foto': image, 'capt':captutra}

async def get_skills(dialog_manager: DialogManager, **kwargs):
    skills = [
        ("Redis", '1'),
        ("PostgreSQL", '2'),
        ("aiogram-dialog", '3'),
        ("miniapp", '4'),
        ("Интеграция с openAI", '5'),
        ("scheduler", '6'),
        ("BS4", '7'),
        ("pandas", '8'),
        ("Jenkins", '9'),
        ("react", '10'),
    ]
    return {"skills": skills}
