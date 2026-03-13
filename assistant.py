from contacts import (
    AddressBook,
    add_contact_handler,
    search_contacts_handler,
    edit_contact_handler,
    delete_contact_handler,
    show_birthdays_handler,
)
from notes import (
    NoteBook,
    add_note_handler,
    edit_note_handler,
    delete_note_handler,
    add_tags_handler,
    remove_tag_handler,
    search_by_title_handler,
    search_by_tag_handler,
    sort_by_title_handler,
    sort_by_date_handler,
    sort_by_tag_handler,
    all_notes_handler,
)


def parse_input(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def main() -> None:
    book = AddressBook()
    notebook = NoteBook()
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
            print(add_contact_handler(book, args))
        elif command in ["search", "search-contact"]:
            print(search_contacts_handler(book, args))
        elif command in ["edit", "edit-contact"]:
            print(edit_contact_handler(book, args))
        elif command in ["delete", "delete-contact"]:
            print(delete_contact_handler(book, args))
        elif command in ["birthdays", "bday"]:
            print(show_birthdays_handler(book, args))
        
        elif command == "add-note":
            print(add_note_handler(args, notebook))
        elif command == "edit-note":
            print(edit_note_handler(args, notebook))
        elif command == "delete-note":
            print(delete_note_handler(args, notebook))
        elif command == "add-tags":
            print(add_tags_handler(args, notebook))
        elif command == "remove-tag":
            print(remove_tag_handler(args, notebook))
        elif command == "all-notes":
            print(all_notes_handler(notebook))
        elif command == "search-note":
            print(search_by_title_handler(args, notebook))
        elif command == "search-tag":
            print(search_by_tag_handler(args, notebook))
        elif command == "sort-notes-title":
            print(sort_by_title_handler(notebook))
        elif command == "sort-notes-date":
            print(sort_by_date_handler(notebook))
        elif command == "sort-notes-tag":
            print(sort_by_tag_handler(notebook))

        else:
            print("❌ Невідома команда")

            
if __name__ == "__main__":
    main()