from contacts import AddressBook, Contact
import re
from datetime import datetime

# ========== ВАЛІДАЦІЯ ==========
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

# ========== ФУНКЦІЇ БОТА ==========
def parse_input(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args

def add_contact(book, args):
    """Додавання нового контакту з валідацією"""
    if len(args) < 2:
        print("❌ Потрібно вказати ім'я та телефон. Приклад: add Іван 0501234567")
        return
    
    name_input = args[0]
    phone_input = args[1]
    
    # Валідація імені
    valid, name = validate_name(name_input)
    if not valid:
        print(name)
        return
    
    # Валідація телефону
    valid, phone = validate_phone(phone_input)
    if not valid:
        print(phone)
        return
    
    # Email (необов'язковий)
    email = ""
    if len(args) > 2:
        valid, email = validate_email(args[2])
        if not valid:
            print(email)
            return
    
    # День народження (необов'язковий)
    birthday_input = input("День народження (РРРР-ММ-ДД, або Enter щоб пропустити): ")
    valid, birthday = validate_birthday(birthday_input)
    if not valid:
        print(birthday)
        return
    
    contact = Contact(name, phone=phone, email=email, birthday=birthday)
    book.add_contact(contact)
    print(f"✅ Контакт {name} додано!")

def search_contacts(book, args):
    """Пошук контактів"""
    if not args:
        print("❌ Вкажи текст для пошуку. Приклад: search Іван")
        return
    
    search_text = " ".join(args)
    results = book.search_contacts(search_text)
    
    if not results:
        print(f"❌ Нічого не знайдено за запитом '{search_text}'")
    else:
        print(f"✅ Знайдено {len(results)} контактів:")
        for contact in results:
            print(f"  📌 {contact.name}")
            print(f"     📞 {contact.phone}")
            if contact.email:
                print(f"     ✉️ {contact.email}")
            if contact.address:
                print(f"     🏠 {contact.address}")
            if contact.birthday:
                days = contact.days_to_birthday()
                if days == 0:
                    print("     🎂 СЬОГОДНІ ДЕНЬ НАРОДЖЕННЯ!")
                elif days:
                    print(f"     🎂 До дня народження {days} днів")

def edit_contact(book, args):
    """Редагування контакту з валідацією"""
    if not args:
        print("❌ Вкажи ім'я контакту для редагування. Приклад: edit Іван")
        return
    
    name = " ".join(args)
    contact = book.find_contact(name)
    
    if not contact:
        print(f"❌ Контакт '{name}' не знайдено")
        return
    
    print(f"\nРедагуємо контакт: {contact.name}")
    print("(Залиш поле порожнім, щоб не змінювати)")
    
    # Редагування імені
    new_name = input(f"Ім'я [{contact.name}]: ")
    if new_name:
        valid, result = validate_name(new_name)
        if valid:
            contact.name = result
        else:
            print(result)
    
    # Редагування телефону
    new_phone = input(f"Телефон [{contact.phone}]: ")
    if new_phone:
        valid, result = validate_phone(new_phone)
        if valid:
            contact.phone = result
        else:
            print(result)
    
    # Редагування email
    new_email = input(f"Email [{contact.email}]: ")
    if new_email:
        valid, result = validate_email(new_email)
        if valid:
            contact.email = result
        else:
            print(result)
    
    # Редагування дня народження
    new_birthday = input(f"День народження [{contact.birthday}]: ")
    if new_birthday:
        valid, result = validate_birthday(new_birthday)
        if valid:
            contact.birthday = result
        else:
            print(result)
    
    print(f"✅ Контакт оновлено!")

def delete_contact(book, args):
    """Видалення контакту"""
    if not args:
        print("❌ Вкажи ім'я контакту для видалення. Приклад: delete Іван")
        return
    
    name = " ".join(args)
    deleted = book.delete_contact(name)
    
    if deleted:
        print(f"✅ Контакт '{name}' видалено")
    else:
        print(f"❌ Контакт '{name}' не знайдено")

def show_birthdays(book, args):
    """Показати іменинників"""
    if not args:
        print("❌ Вкажи кількість днів. Приклад: birthdays 7")
        return
    
    try:
        days = int(args[0])
    except ValueError:
        print("❌ Вкажи число днів. Приклад: birthdays 7")
        return
    
    results = book.get_birthdays_in_days(days)
    
    if not results:
        print(f"📭 Немає іменинників через {days} днів")
    else:
        print(f"🎂 Іменинники через {days} днів:")
        for contact in results:
            print(f"  {contact.name} - {contact.birthday}")

def main() -> None:
    book = AddressBook()
    print("Welcome to the assistant bot!")
    print("Доступні команди:")
    print("  add / add-contact [ім'я] [телефон] [email]   - додати контакт")
    print("  search / search-contact [текст]              - пошук контактів")
    print("  edit / edit-contact [ім'я]                   - редагувати контакт")
    print("  delete / delete-contact [ім'я]               - видалити контакт")
    print("  birthdays / bday [дні]                       - список іменинників")
    print("  exit                                          - вихід")
    
    while True:
        user_input = input("\nEnter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command in ["add", "add-contact"]:
            add_contact(book, args)
        elif command in ["search", "search-contact"]:
            search_contacts(book, args)
        elif command in ["edit", "edit-contact"]:
            edit_contact(book, args)
        elif command in ["delete", "delete-contact"]:
            delete_contact(book, args)
        elif command in ["birthdays", "bday"]:
            show_birthdays(book, args)
        else:
            print("❌ Невідома команда")

if __name__ == "__main__":
    main()