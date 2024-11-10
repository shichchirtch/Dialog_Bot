import re

# Регулярное выражение для имени
name_pattern = r"^[A-Za-zА-Яа-яЁё]{4,50}(?:[-\s][A-Za-zА-Яа-яЁё]{2,50})*$"

def name_check(name: str) -> str:
    print('we are into name function')
    data = bool(re.match(name_pattern, name))
    if data:
        return name
    raise ValueError


email_pattern = r"^(?=.{7,30}$)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

def mail_check(mail: str) -> str:
    print('we are into mail function')
    data = bool(re.match(email_pattern, mail))
    if data:
        return mail
    raise ValueError

