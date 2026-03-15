import re
from datetime import datetime

def validate_name(name):
    """Перевірка імені"""
    name = name.strip()
    if len(name) < 2:
        return False, "❌ Ім'я має бути не менше 2 символів"
    if not name.replace(" ", "").isalpha():
        return False, "❌ Ім'я може містити тільки літери та пробіли"
    return True, name.title()

def validate_phone(phone):
    """Перевірка телефону (Україна)"""
    phone = phone.strip()
    # Видаляємо всі пробіли, дужки, тире
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Патерни: +380XXXXXXXXX або 0XXXXXXXXX
    if re.match(r'^\+?380\d{9}$', phone) or re.match(r'^0\d{9}$', phone):
        # Приводимо до єдиного формату +380XXXXXXXXX
        if phone.startswith('0'):
            phone = '+38' + phone
        elif phone.startswith('380'):
            phone = '+' + phone
        return True, phone
    return False, "❌ Неправильний формат телефону. Використовуйте: +380501234567 або 0501234567"

def validate_email(email):
    """Перевірка email"""
    email = email.strip()
    if len(email) > 254:
        return False, "❌ Email занадто довгий (максимум 254 символи)"
    if ".." in email:
        return False, "❌ Email не може містити дві крапки підряд"
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        local_part = email.split("@")[0]
        if len(local_part) > 64:
            return False, "❌ Частина email до @ занадто довга (максимум 64 символи)"
        return True, email.lower()
    return False, "❌ Неправильний формат email. Приклад: name@example.com"

def validate_birthday(birthday):
    """Перевірка дати народження"""
    if not birthday:
        return True, ""
    
    birthday = birthday.strip()
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, birthday):
        return False, "❌ Формат дати: РРРР-ММ-ДД (наприклад: 1990-01-31)"
    
    try:
        # Перевіряємо чи існує така дата
        birth_date = datetime.strptime(birthday, "%Y-%m-%d").date()
        today = datetime.now().date()
        if birth_date > today:
            return False, "❌ Дата народження не може бути в майбутньому"
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
        if age > 120:
            return False, "❌ Вік не може бути більше 120 років"
        return True, birthday
    except ValueError:
        return False, "❌ Неправильна дата. Перевір місяць та день"


def validate_note_title(title):
    """Перевірка назви нотатки."""
    clean_title = title.strip()
    if not clean_title:
        return False, "❌ Назва нотатки не може бути порожньою"
    if len(clean_title) < 2:
        return False, "❌ Назва нотатки має бути мінімум 2 символи"
    if len(clean_title) > 100:
        return False, "❌ Назва нотатки занадто довга (максимум 100 символів)"
    return True, clean_title


def validate_note_text(text):
    """Перевірка тексту нотатки."""
    clean_text = text.strip()
    if not clean_text:
        return False, "❌ Текст нотатки не може бути порожнім"
    if len(clean_text) > 2000:
        return False, "❌ Текст нотатки занадто довгий (максимум 2000 символів)"
    return True, clean_text


def validate_tags(tags):
    """Перевірка та нормалізація списку тегів."""
    normalized_tags = []
    for tag in tags:
        clean_tag = tag.strip().lower()
        if not clean_tag:
            continue
        if len(clean_tag) > 30:
            return False, "❌ Тег занадто довгий (максимум 30 символів)"
        if not re.match(r"^[a-zа-яіїєґ0-9_-]+$", clean_tag):
            return False, "❌ Тег може містити лише літери, цифри, '-' або '_'"
        if clean_tag not in normalized_tags:
            normalized_tags.append(clean_tag)
    return True, normalized_tags


def require_args(min_count, message, args_index=0):
    """Декоратор перевірки мінімальної кількості аргументів."""
    def decorator(func):
        def inner(*args, **kwargs):
            command_args = []
            if len(args) > args_index:
                command_args = args[args_index]
            if len(command_args) < min_count:
                raise ValueError(message)
            return func(*args, **kwargs)
        return inner
    return decorator


def input_error(func):
    """Декоратор для єдиної обробки помилок у CLI-хендлерах."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "❌ Недостатньо аргументів для команди."
        except KeyError as error:
            if error.args:
                message = str(error.args[0]).strip()
            else:
                message = str(error).strip().strip("'")
            if not message:
                return "❌ Запис не знайдено."
            if message.startswith("❌"):
                return message
            return f"❌ {message}"
        except ValueError as error:
            message = str(error).strip()
            if not message:
                return "❌ Сталася помилка."
            if message.startswith("❌"):
                return message
            return f"❌ {message}"

    return inner