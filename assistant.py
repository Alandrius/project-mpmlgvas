from contacts import AddressBook, Contact

def parse_input(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args

def add_contact(book, args):
    """Додавання нового контакту"""
    if len(args) < 2:
        print("❌ Потрібно вказати ім'я та телефон. Приклад: add Іван 0501234567")
        return
    
    name, phone = args[:2]
    
    # Запитати день народження (необов'язково)
    birthday = input("День народження (РРРР-ММ-ДД, або Enter щоб пропустити): ")
    
    contact = Contact(name, phone=phone, birthday=birthday)
    book.add_contact(contact)
    print(f"✅ Контакт {name} додано!")

def search_contacts(book, args):
    """Пошук контактів за текстом"""
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
    """Редагування контакту"""
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
    
    new_name = input(f"Ім'я [{contact.name}]: ")
    if new_name:
        contact.name = new_name
    
    new_phone = input(f"Телефон [{contact.phone}]: ")
    if new_phone:
        contact.phone = new_phone
    
    new_email = input(f"Email [{contact.email}]: ")
    if new_email:
        contact.email = new_email
    
    new_address = input(f"Адреса [{contact.address}]: ")
    if new_address:
        contact.address = new_address
    
    new_birthday = input(f"День народження [{contact.birthday}]: ")
    if new_birthday:
        contact.birthday = new_birthday
    
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

# 👇 НОВА ФУНКЦІЯ ДЛЯ ДНІВ НАРОДЖЕННЯ
def show_birthdays(book, args):
    """Показати контакти з днями народження через N днів"""
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
    print("  add / add-contact [ім'я] [телефон]          - додати контакт")
    print("  search / search-contact [текст]             - пошук контактів")
    print("  edit / edit-contact [ім'я]                  - редагувати контакт")
    print("  delete / delete-contact [ім'я]              - видалити контакт")
    print("  birthdays / bday [дні]                      - список іменинників через N днів")
    print("  exit                                         - вихід")
    
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