from enum import Enum

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

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

try:
    from colorama import Back, Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
except ImportError:
    Back = Fore = Style = None


class CommandCategory(Enum):
    CONTACTS = "Contacts"
    NOTES = "Notes"
    OTHER = "Other"


def color_text(text: str, fore=None, back=None, style=None) -> str:
    """Wrap text with colorama codes if available."""
    if Fore is None or Style is None:
        return text

    parts = []
    if style:
        parts.append(style)
    if fore:
        parts.append(fore)
    if back:
        parts.append(back)

    parts.append(text)
    parts.append(Style.RESET_ALL)
    return "".join(parts)


def format_notes_table(notes):
    """Format a list of notes into a table using tabulate."""
    if not notes:
        return "📭 Нотаток ще немає."

    table_data = []
    for note in notes:
        tags_str = ", ".join(note.tags) if note.tags else "—"
        created = note.created_at.strftime('%d.%m.%Y %H:%M')
        updated = note.updated_at.strftime('%d.%m.%Y %H:%M')
        table_data.append([note.title, note.text, tags_str, created, updated])

    if tabulate:
        headers = [
            color_text("Назва", fore=Fore.WHITE, back=Back.BLUE, style=Style.BRIGHT),
            color_text("Текст", fore=Fore.WHITE, back=Back.BLUE, style=Style.BRIGHT),
            color_text("Теги", fore=Fore.WHITE, back=Back.BLUE, style=Style.BRIGHT),
            color_text("Створено", fore=Fore.WHITE, back=Back.BLUE, style=Style.BRIGHT),
            color_text("Оновлено", fore=Fore.WHITE, back=Back.BLUE, style=Style.BRIGHT),
        ]
        return tabulate(table_data, headers=headers, tablefmt="grid")
    else:
        # Fallback without tabulate
        lines = ["Назва | Текст | Теги | Створено | Оновлено"]
        lines.append("-" * 50)
        for row in table_data:
            lines.append(" | ".join(row))
        return "\n".join(lines)


def parse_input(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def format_help_table(commands_by_category) -> str:
    """Format help output with tabulate if available."""
    lines = []

    for category, items in commands_by_category.items():
        category_text = category.value if isinstance(category, CommandCategory) else str(category)
        header = color_text(category_text, fore=Fore.CYAN, style=Style.BRIGHT)
        lines.append(header)

        table_data = []
        for item in items:
            example = item['help']['example']
            description = item['help']['description']
            table_data.append([example, description])

        if tabulate:
            header_cmd = color_text("Command", fore=Fore.WHITE, back=Back.BLUE, style=Style.BRIGHT)
            header_desc = color_text("Description", fore=Fore.WHITE, back=Back.BLUE, style=Style.BRIGHT)
            lines.append(
                tabulate(table_data, headers=[header_cmd, header_desc], tablefmt="plain")
            )
        else:
            for example, description in table_data:
                lines.append(f"  {example} - {description}")

        lines.append("")

    return "\n".join(lines)


def print_help(commands) -> None:
    """Print the help section grouped by category."""
    categories = {}
    for info in commands.values():
        category = info.get('category', CommandCategory.OTHER)
        categories.setdefault(category, []).append(info)

    print("Welcome to the assistant bot!")
    print(format_help_table(categories))


def main() -> None:
    book = AddressBook()
    notebook = NoteBook()

    commands = {
        'add': {
            'aliases': ['add-contact'],
            'handler': add_contact_handler,
            'object': book,
            'category': CommandCategory.CONTACTS,
            'help': {
                'example': 'add / add-contact [ім\'я] [телефон] [email]',
                'description': 'додати контакт'
            }
        },
        'search': {
            'aliases': ['search-contact'],
            'handler': search_contacts_handler,
            'object': book,
            'category': CommandCategory.CONTACTS,
            'help': {
                'example': 'search / search-contact [текст]',
                'description': 'пошук контактів'
            }
        },
        'edit': {
            'aliases': ['edit-contact'],
            'handler': edit_contact_handler,
            'object': book,
            'category': CommandCategory.CONTACTS,
            'help': {
                'example': 'edit / edit-contact [ім\'я]',
                'description': 'редагувати контакт'
            }
        },
        'delete': {
            'aliases': ['delete-contact'],
            'handler': delete_contact_handler,
            'object': book,
            'category': CommandCategory.CONTACTS,
            'help': {
                'example': 'delete / delete-contact [ім\'я]',
                'description': 'видалити контакт'
            }
        },
        'birthdays': {
            'aliases': ['bday'],
            'handler': show_birthdays_handler,
            'object': book,
            'category': CommandCategory.CONTACTS,
            'help': {
                'example': 'birthdays / bday [дні]',
                'description': 'список іменинників'
            }
        },
        'show-all': {
            'aliases': ['show-all-contacts', 'contacts', 'list'],
            'handler': show_all_contacts_handler,
            'object': book,
            'category': CommandCategory.CONTACTS,
            'help': {
                'example': 'show-all / show-all-contacts / contacts / list',
                'description': 'показати всі контакти'
            }
        },
        'add-note': {
            'aliases': [],
            'handler': add_note_handler,
            'object': notebook,
            'category': CommandCategory.NOTES,
            'help': {
                'example': 'add-note',
                'description': 'додати нотатку (буде запропоновано ввести назву та текст)'
            }
        },
        'edit-note': {
            'aliases': [],
            'handler': edit_note_handler,
            'object': notebook,
            'category': CommandCategory.NOTES,
            'help': {
                'example': 'edit-note [назва] [новий текст]',
                'description': 'редагувати нотатку'
            }
        },
        'delete-note': {
            'aliases': [],
            'handler': delete_note_handler,
            'object': notebook,
            'category': CommandCategory.NOTES,
            'help': {
                'example': 'delete-note [назва]',
                'description': 'видалити нотатку'
            }
        },
        'add-tags': {
            'aliases': [],
            'handler': add_tags_handler,
            'object': notebook,
            'category': CommandCategory.NOTES,
            'help': {
                'example': 'add-tags [назва] [тег1] [тег2] ...',
                'description': 'додати теги'
            }
        },
        'remove-tag': {
            'aliases': [],
            'handler': remove_tag_handler,
            'object': notebook,
            'category': CommandCategory.NOTES,
            'help': {
                'example': 'remove-tag [назва] [тег]',
                'description': 'видалити тег'
            }
        },
        'all-notes': {
            'aliases': [],
            'handler': all_notes_handler,
            'object': notebook,
            'category': CommandCategory.NOTES,
            'help': {
                'example': 'all-notes',
                'description': 'показати всі нотатки'
            }
        },
        'search-note': {
            'aliases': [],
            'handler': search_by_title_handler,
            'object': notebook,
            'category': CommandCategory.NOTES,
            'help': {
                'example': 'search-note [запит]',
                'description': 'пошук нотаток за назвою'
            }
        },
        'search-tag': {
            'aliases': [],
            'handler': search_by_tag_handler,
            'object': notebook,
            'category': CommandCategory.NOTES,
            'help': {
                'example': 'search-tag [тег]',
                'description': 'пошук нотаток за тегом'
            }
        },
        'sort-notes-title': {
            'aliases': [],
            'handler': sort_by_title_handler,
            'object': notebook,
            'category': CommandCategory.NOTES,
            'help': {
                'example': 'sort-notes-title',
                'description': 'сортувати нотатки за назвою'
            }
        },
        'sort-notes-date': {
            'aliases': [],
            'handler': sort_by_date_handler,
            'object': notebook,
            'category': CommandCategory.NOTES,
            'help': {
                'example': 'sort-notes-date',
                'description': 'сортувати нотатки за датою'
            }
        },
        'sort-notes-tag': {
            'aliases': [],
            'handler': sort_by_tag_handler,
            'object': notebook,
            'category': CommandCategory.NOTES,
            'help': {
                'example': 'sort-notes-tag',
                'description': 'сортувати нотатки за тегом'
            }
        },
        'close': {
            'aliases': ['exit'],
            'handler': None,  # special case
            'object': None,
            'category': CommandCategory.OTHER,
            'help': {
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

    print_help(commands)

    while True:
        user_input = input("\nEnter a command: ")
        command, args = parse_input(user_input)

        if command in registry:
            info = registry[command]
            if info['handler'] is None:  # exit command
                print("Good bye!")
                break
            else:
                result = info['handler'](info['object'], args)
                if isinstance(result, list):
                    print(format_notes_table(result))
                else:
                    print(result)
        else:
            print("❌ Невідома команда")

            
if __name__ == "__main__":
    main()