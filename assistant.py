from contacts import (
    AddressBook,
    add_contact_handler,
    search_contacts_handler,
    edit_contact_handler,
    delete_contact_handler,
    show_birthdays_handler,
    show_all_contacts_handler,
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

    commands = {
        'add': {
            'aliases': ['add-contact'],
            'handler': add_contact_handler,
            'object': book,
            'description': {
                'example': 'add / add-contact [ім\'я] [телефон] [email]',
                'description': 'додати контакт'
            }
        },
        'search': {
            'aliases': ['search-contact'],
            'handler': search_contacts_handler,
            'object': book,
            'description': {
                'example': 'search / search-contact [текст]',
                'description': 'пошук контактів'
            }
        },
        'edit': {
            'aliases': ['edit-contact'],
            'handler': edit_contact_handler,
            'object': book,
            'description': {
                'example': 'edit / edit-contact [ім\'я]',
                'description': 'редагувати контакт'
            }
        },
        'delete': {
            'aliases': ['delete-contact'],
            'handler': delete_contact_handler,
            'object': book,
            'description': {
                'example': 'delete / delete-contact [ім\'я]',
                'description': 'видалити контакт'
            }
        },
        'birthdays': {
            'aliases': ['bday'],
            'handler': show_birthdays_handler,
            'object': book,
            'description': {
                'example': 'birthdays / bday [дні]',
                'description': 'список іменинників'
            }
        },
        'show-all': {
            'aliases': ['show-all-contacts', 'contacts', 'list'],
            'handler': show_all_contacts_handler,
            'object': book,
            'description': {
                'example': 'show-all / show-all-contacts / contacts / list',
                'description': 'показати всі контакти'
            }
        },
        'add-note': {
            'aliases': [],
            'handler': add_note_handler,
            'object': notebook,
            'description': {
                'example': 'add-note [назва] [текст]',
                'description': 'додати нотатку'
            }
        },
        'edit-note': {
            'aliases': [],
            'handler': edit_note_handler,
            'object': notebook,
            'description': {
                'example': 'edit-note [назва] [новий текст]',
                'description': 'редагувати нотатку'
            }
        },
        'delete-note': {
            'aliases': [],
            'handler': delete_note_handler,
            'object': notebook,
            'description': {
                'example': 'delete-note [назва]',
                'description': 'видалити нотатку'
            }
        },
        'add-tags': {
            'aliases': [],
            'handler': add_tags_handler,
            'object': notebook,
            'description': {
                'example': 'add-tags [назва] [тег1] [тег2] ...',
                'description': 'додати теги'
            }
        },
        'remove-tag': {
            'aliases': [],
            'handler': remove_tag_handler,
            'object': notebook,
            'description': {
                'example': 'remove-tag [назва] [тег]',
                'description': 'видалити тег'
            }
        },
        'all-notes': {
            'aliases': [],
            'handler': all_notes_handler,
            'object': notebook,
            'description': {
                'example': 'all-notes',
                'description': 'показати всі нотатки'
            }
        },
        'search-note': {
            'aliases': [],
            'handler': search_by_title_handler,
            'object': notebook,
            'description': {
                'example': 'search-note [запит]',
                'description': 'пошук нотаток за назвою'
            }
        },
        'search-tag': {
            'aliases': [],
            'handler': search_by_tag_handler,
            'object': notebook,
            'description': {
                'example': 'search-tag [тег]',
                'description': 'пошук нотаток за тегом'
            }
        },
        'sort-notes-title': {
            'aliases': [],
            'handler': sort_by_title_handler,
            'object': notebook,
            'description': {
                'example': 'sort-notes-title',
                'description': 'сортувати нотатки за назвою'
            }
        },
        'sort-notes-date': {
            'aliases': [],
            'handler': sort_by_date_handler,
            'object': notebook,
            'description': {
                'example': 'sort-notes-date',
                'description': 'сортувати нотатки за датою'
            }
        },
        'sort-notes-tag': {
            'aliases': [],
            'handler': sort_by_tag_handler,
            'object': notebook,
            'description': {
                'example': 'sort-notes-tag',
                'description': 'сортувати нотатки за тегом'
            }
        },
        'close': {
            'aliases': ['exit'],
            'handler': None,  # special case
            'object': None,
            'description': {
                'example': 'close / exit',
                'description': 'вихід'
            }
        }
    }

    # Build registry
    registry = {}
    for cmd, info in commands.items():
        for alias in [cmd] + info['aliases']:
            registry[alias] = info

    print("Welcome to the assistant bot!")
    print("Доступні команди:")
    for cmd, info in commands.items():
        desc = info['description']
        print(f"  {desc['example']} - {desc['description']}")
    print()
    
    while True:
        user_input = input("\nEnter a command: ")
        command, args = parse_input(user_input)

        if command in registry:
            info = registry[command]
            if info['handler'] is None:  # exit command
                print("Good bye!")
                break
            else:
                print(info['handler'](info['object'], args))
        else:
            print("❌ Невідома команда")

            
if __name__ == "__main__":
    main()