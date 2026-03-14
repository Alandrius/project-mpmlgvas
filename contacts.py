from datetime import datetime, timedelta
from validation import (
    validate_name,
    validate_phone,
    validate_email,
    validate_birthday,
    input_error,
    require_args,
)


class Contact:
    """Клас для одного контакту"""
    def __init__(self, name, address="", phone="", email="", birthday=""):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday
    
    def days_to_birthday(self):
        """Скільки днів до дня народження"""
        if not self.birthday:
            return None
        
        today = datetime.now().date()
        bday = datetime.strptime(self.birthday, "%Y-%m-%d").date()
        try:
            next_bday = bday.replace(year=today.year)
        except ValueError:
            # Для 29.02 у невисокосний рік беремо 28.02
            next_bday = bday.replace(year=today.year, day=28)
        
        if next_bday < today:
            try:
                next_bday = next_bday.replace(year=today.year + 1)
            except ValueError:
                next_bday = next_bday.replace(year=today.year + 1, day=28)
        
        return (next_bday - today).days

class AddressBook:
    """Клас для книги контактів"""
    def __init__(self):
        self.contacts = []
    
    def add_contact(self, contact):
        self.contacts.append(contact)
        return True
    
    def get_all_contacts(self):
        return self.contacts
    
    def search_contacts(self, search_text):
        results = []
        search_text = search_text.lower()
        for contact in self.contacts:
            if (search_text in contact.name.lower() or 
                search_text in contact.phone or 
                search_text in contact.email.lower()):
                results.append(contact)
        return results
    
    def find_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                return contact
        return None
    
    def delete_contact(self, name):
        for i, contact in enumerate(self.contacts):
            if contact.name.lower() == name.lower():
                return self.contacts.pop(i)
        return None
    
    def get_birthdays_in_days(self, days):
        results = []
        target_date = datetime.now().date() + timedelta(days=days)
        
        for contact in self.contacts:
            if contact.birthday:
                days_to = contact.days_to_birthday()
                if days_to == days:
                    results.append(contact)
        return results


@input_error
@require_args(2, "Потрібно вказати ім'я та телефон. Приклад: add Іван 0501234567", args_index=1)
def add_contact_handler(book, args):
    """Додавання нового контакту з валідацією"""
    name_input = args[0]
    phone_input = args[1]

    # Валідація імені
    valid, name = validate_name(name_input)
    if not valid:
        raise ValueError(name)
    
    # Валідація телефону
    valid, phone = validate_phone(phone_input)
    if not valid:
        raise ValueError(phone)
    
    # Email (необов'язковий)
    email = ""
    if len(args) > 2:
        valid, email = validate_email(args[2])
        if not valid:
            raise ValueError(email)
    
    # День народження (необов'язковий)
    birthday_input = input("День народження (РРРР-ММ-ДД, або Enter щоб пропустити): ")
    valid, birthday = validate_birthday(birthday_input)
    if not valid:
        raise ValueError(birthday)
    
    contact = Contact(name, phone=phone, email=email, birthday=birthday)
    book.add_contact(contact)
    return f"✅ Контакт {name} додано!"

@input_error
@require_args(1, "Вкажи текст для пошуку. Приклад: search Іван", args_index=1)
def search_contacts_handler(book, args):
    """Пошук контактів"""
    search_text = " ".join(args)
    results = book.search_contacts(search_text)

    if not results:
        return f"❌ Нічого не знайдено за запитом '{search_text}'"

    lines = [f"✅ Знайдено {len(results)} контактів:"]
    for contact in results:
        lines.append(f"  📌 {contact.name}")
        lines.append(f"     📞 {contact.phone}")
        if contact.email:
            lines.append(f"     ✉️ {contact.email}")
        if contact.address:
            lines.append(f"     🏠 {contact.address}")
        if contact.birthday:
            days = contact.days_to_birthday()
            if days == 0:
                lines.append("     🎂 СЬОГОДНІ ДЕНЬ НАРОДЖЕННЯ!")
            elif days:
                lines.append(f"     🎂 До дня народження {days} днів")
    return "\n".join(lines)

@input_error
@require_args(1, "Вкажи ім'я контакту для редагування. Приклад: edit Іван", args_index=1)
def edit_contact_handler(book, args):
    """Редагування контакту з валідацією"""
    name = " ".join(args)
    contact = book.find_contact(name)

    if not contact:
        raise KeyError(f"❌ Контакт '{name}' не знайдено")
    
    print(f"\nРедагуємо контакт: {contact.name}")
    print("(Залиш поле порожнім, щоб не змінювати)")
    
    # Редагування імені
    new_name = input(f"Ім'я [{contact.name}]: ")
    if new_name:
        valid, result = validate_name(new_name)
        if valid:
            contact.name = result
        else:
            raise ValueError(result)
    
    # Редагування телефону
    new_phone = input(f"Телефон [{contact.phone}]: ")
    if new_phone:
        valid, result = validate_phone(new_phone)
        if valid:
            contact.phone = result
        else:
            raise ValueError(result)
    
    # Редагування email
    new_email = input(f"Email [{contact.email}]: ")
    if new_email:
        valid, result = validate_email(new_email)
        if valid:
            contact.email = result
        else:
            raise ValueError(result)
    
    # Редагування дня народження
    current_bday = contact.birthday.isoformat() if contact.birthday else ""
    new_birthday = input(f"День народження [{current_bday}]: ")
    if new_birthday:
        valid, result = validate_birthday(new_birthday)
        if valid:
            contact.birthday = result
        else:
            raise ValueError(result)
    
    return "✅ Контакт оновлено!"

@input_error
@require_args(1, "Вкажи ім'я контакту для видалення. Приклад: delete Іван", args_index=1)
def delete_contact_handler(book, args):
    """Видалення контакту"""
    name = " ".join(args)
    deleted = book.delete_contact(name)

    if deleted:
        return f"✅ Контакт '{name}' видалено"
    raise KeyError(f"❌ Контакт '{name}' не знайдено")

@input_error
@require_args(1, "Вкажи кількість днів. Приклад: birthdays 7", args_index=1)
def show_birthdays_handler(book, args):
    """Показати іменинників"""
    try:
        days = int(args[0])
    except ValueError:
        raise ValueError("❌ Вкажи число днів. Приклад: birthdays 7")
    if days < 0:
        raise ValueError("❌ Кількість днів не може бути від'ємною")
    
    results = book.get_birthdays_in_days(days)

    if not results:
        return f"📭 Немає іменинників через {days} днів"

    lines = [f"🎂 Іменинники через {days} днів:"]
    for contact in results:
        lines.append(f"  {contact.name} - {contact.birthday}")
    return "\n".join(lines)


@input_error
def show_all_contacts_handler(book, args):
    """Показати всі контакти"""
    contacts = book.get_all_contacts()
    if not contacts:
        return "📭 Список контактів порожній"

    lines = [f"📒 Всього контактів: {len(contacts)}"]
    for contact in contacts:
        lines.append(f"  📌 {contact.name}")
        lines.append(f"     📞 {contact.phone}")
        if contact.email:
            lines.append(f"     ✉️ {contact.email}")
        if contact.address:
            lines.append(f"     🏠 {contact.address}")
        if contact.birthday:
            days = contact.days_to_birthday()
            if days == 0:
                lines.append("     🎂 СЬОГОДНІ ДЕНЬ НАРОДЖЕННЯ!")
            elif days:
                lines.append(f"     🎂 До дня народження {days} днів")
    return "\n".join(lines)