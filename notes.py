from datetime import datetime
from collections import UserDict


class Note:
    def __init__(self, title: str, text: str, tags: list[str] | None = None):
        self.title: str = title.strip()
        self.text: str = text.strip()
        self.tags: list[str] = [t.strip().lower() for t in (tags or [])]
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = self.created_at

    def add_tags(self, tags: list[str]) -> None:
        for tag in tags:
            t = tag.strip().lower()
            if t and t not in self.tags:
                self.tags.append(t)
        self.updated_at = datetime.now()

    def remove_tag(self, tag: str) -> None:
        t = tag.strip().lower()
        if t not in self.tags:
            raise ValueError(f"Тег '{tag}' не знайдено в нотатці.")
        self.tags.remove(t)
        self.updated_at = datetime.now()

    def __str__(self) -> str:
        tags_str = ", ".join(self.tags) if self.tags else "—"
        return (
            f"[{self.title}]\n"
            f"   Текст   : {self.text}\n"
            f"   Теги    : {tags_str}\n"
            f"   Створено: {self.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            f"   Змінено : {self.updated_at.strftime('%d.%m.%Y %H:%M')}"
        )

class NoteBook(UserDict):
    def add_note(self, title: str, text: str, tags: list[str] | None = None) -> Note:
        if title.strip() in self.data:
            raise ValueError(f"Нотатка з назвою '{title}' вже існує.")
        note = Note(title, text, tags)
        self.data[note.title] = note
        return note

    def edit_note(self, title: str, new_text: str) -> Note:
        note = self.data.get(title.strip())
        if note is None:
            raise KeyError(f"Нотатку '{title}' не знайдено.")
        note.text = new_text.strip()
        note.updated_at = datetime.now()
        return note

    def delete_note(self, title: str) -> None:
        if title.strip() not in self.data:
            raise KeyError(f"Нотатку '{title}' не знайдено.")
        del self.data[title.strip()]

    def add_tags(self, title: str, tags: list[str]) -> Note:
        note = self.data.get(title.strip())
        if note is None:
            raise KeyError(f"Нотатку '{title}' не знайдено.")
        note.add_tags(tags)
        return note

    def remove_tag(self, title: str, tag: str) -> Note:
        note = self.data.get(title.strip())
        if note is None:
            raise KeyError(f"Нотатку '{title}' не знайдено.")
        note.remove_tag(tag)
        return note

    def search_by_title(self, query: str) -> list[Note]:
        q = query.strip().lower()
        return [note for note in self.data.values() if q in note.title.lower()]

    def search_by_tag(self, tag: str) -> list[Note]:
        t = tag.strip().lower()
        return [note for note in self.data.values() if t in note.tags]

    def sort_by_title(self) -> list[Note]:
        return sorted(self.data.values(), key=lambda note: note.title.lower())

    def sort_by_date(self) -> list[Note]:
        return sorted(self.data.values(), key=lambda note: note.created_at)
    
    def sort_by_tag(self) -> list[Note]:
        # Нотатки з тегами — перші (відсортовані за першим тегом), без тегів — в кінці
        with_tags = sorted(
            [n for n in self.data.values() if n.tags],
            key=lambda note: note.tags[0]
        )
        without_tags = [n for n in self.data.values() if not n.tags]
        return with_tags + without_tags
    
# Обробник команди add-note
def add_note_handler(args: list, notebook: NoteBook) -> str:
    if len(args) < 2:
        return "Використання: add-note <назва> <текст>"
    title = args[0]
    text = " ".join(args[1:])
    try:
        note = notebook.add_note(title, text)
        return f"Нотатку '{note.title}' додано."
    except ValueError as e:
        return str(e)
    
# Обробник команди edit-note
def edit_note_handler(args: list, notebook: NoteBook) -> str:
    if len(args) < 2:
        return "Використання: edit-note <назва> <новий текст>"
    title = args[0]
    new_text = " ".join(args[1:])
    try:
        note = notebook.edit_note(title, new_text)
        return f"Нотатку '{note.title}' оновлено."
    except KeyError as e:
        return str(e)

# Обробник команди delete-note
def delete_note_handler(args: list, notebook: NoteBook) -> str:
    if len(args) < 1:
        return "Використання: delete-note <назва>"
    title = args[0]
    try:
        notebook.delete_note(title)
        return f"Нотатку '{title}' видалено."
    except KeyError as e:
        return str(e)
    
# Обробник команди add-tags
def add_tags_handler(args: list, notebook: NoteBook) -> str:
    if len(args) < 2:
        return "Використання: add-tags <назва нотатки> <тег1> <тег2> ..."
    title = args[0]
    tags = args[1:]
    try:
        note = notebook.add_tags(title, tags)
        return f"Теги {note.tags} додано до '{note.title}'."
    except KeyError as e:
        return str(e)

# Обробник команди remove_tag
def remove_tag_handler(args: list, notebook: NoteBook) -> str:
    if len(args) < 2:
        return "Використання: remove-tag <назва нотатки> <тег>"
    title = args[0]
    tag = args[1]
    try:
        note = notebook.remove_tag(title, tag)
        return f"Тег '{tag}' видалено з '{note.title}'."
    except (KeyError, ValueError) as e:
        return str(e)
    
# Обробник команди search_by_title
def search_by_title_handler(args: list, notebook: NoteBook) -> str:
    if len(args) < 1:
        return "Використання: search-note <запит>"
    query = " ".join(args)
    results = notebook.search_by_title(query)
    if not results:
        return f"Нотаток з назвою '{query}' не знайдено."
    return "\n\n".join(str(note) for note in results)

# Обробник команди search_by_tag
def search_by_tag_handler(args: list, notebook: NoteBook) -> str:
    if len(args) < 1:
        return "Використання: search-tag <тег>"
    tag = args[0]
    results = notebook.search_by_tag(tag)
    if not results:
        return f"Нотаток з тегом '{tag}' не знайдено."
    return "\n\n".join(str(note) for note in results)

# Обробник команди sort_by_title
def sort_by_title_handler(notebook: NoteBook) -> str:
    results = notebook.sort_by_title()
    if not results:
        return "Нотаток ще немає."
    return "\n\n".join(str(note) for note in results)

# Обробник команди sort_by_date
def sort_by_date_handler(notebook: NoteBook) -> str:
    results = notebook.sort_by_date()
    if not results:
        return "Нотаток ще немає."
    return "\n\n".join(str(note) for note in results)

# Обробник команди sort_by_tag
def sort_by_tag_handler(notebook: NoteBook) -> str:
    results = notebook.sort_by_tag()
    if not results:
        return "Нотаток ще немає."
    return "\n\n".join(str(note) for note in results)

def all_notes_handler(notebook: NoteBook) -> str:
    return sort_by_date_handler(notebook)