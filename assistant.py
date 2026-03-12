from contacts import AddressBook
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

    
def main() -> None:
    book = AddressBook()
    notebook = NoteBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

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

if __name__ == "__main__":
    main()
