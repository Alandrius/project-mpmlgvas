from contacts import AddressBook, Contact
from notes import (
    NoteBook,
    add_note_handler,
    edit_note_handler,
    delete_note_handler,
    search_by_title_handler,
    sort_by_title_handler,
    sort_by_date_handler,
)

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

def main() -> None:
    book = AddressBook()
    notebook = NoteBook()
    print("Welcome to the assistant bot!")
    print("Доступні команди:")
    print("  add / add-contact [ім'я] [телефон]          - додати контакт")
    print("  search / search-contact [текст]             - пошук контактів")
    print("  edit / edit-contact [ім'я]                  - редагувати контакт")
    print("  delete / delete-contact [ім'я]              - видалити контакт")
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
        
        elif command == "add-note":
            print(add_note_handler(args, notebook))
        elif command == "edit-note":
            print(edit_note_handler(args, notebook))
        elif command == "delete-note":
            print(delete_note_handler(args, notebook))
        elif command == "search-note":
            print(search_by_title_handler(args, notebook))
        elif command == "sort-notes-title":
            print(sort_by_title_handler(notebook))
        elif command == "sort-notes-date":
            print(sort_by_date_handler(notebook))

        else:
            print("❌ Невідома команда")

            
if __name__ == "__main__":
    main()