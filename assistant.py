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
    contact = Contact(name, phone=phone)
    book.add_contact(contact)
    print(f"✅ Контакт {name} з телефоном {phone} успішно додано!")

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

def main() -> None:
    book = AddressBook()
    print("Welcome to the assistant bot!")
    print("Доступні команди:")
    print("  add / add-contact [ім'я] [телефон]  - додати контакт")
    print("  search / search-contact [текст]     - пошук контактів")
    print("  exit                                 - вихід")
    
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
        else:
            print("❌ Невідома команда")

if __name__ == "__main__":
    main()