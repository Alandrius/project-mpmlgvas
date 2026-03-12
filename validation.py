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
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
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
        datetime.strptime(birthday, "%Y-%m-%d")
        return True, birthday
    except ValueError:
        return False, "❌ Неправильна дата. Перевір місяць та день"