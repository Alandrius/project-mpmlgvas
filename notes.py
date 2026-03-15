from datetime import datetime
from collections import UserDict
from typing import Optional
from validation import (
    input_error,
    require_args,
    validate_note_title,
    validate_note_text,
    validate_tags,
)


class Note:
    def __init__(self, title: str, text: str, tags: Optional[list[str]] = None):
        valid, clean_title = validate_note_title(title)
        if not valid:
            raise ValueError(clean_title)

        valid, clean_text = validate_note_text(text)
        if not valid:
            raise ValueError(clean_text)

        valid, clean_tags = validate_tags(tags or [])
        if not valid:
            raise ValueError(clean_tags)

        self.title: str = clean_title
        self.text: str = clean_text
        self.tags: list[str] = clean_tags
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = self.created_at

    def add_tags(self, tags: list[str]) -> None:
        valid, clean_tags = validate_tags(tags)
        if not valid:
            raise ValueError(clean_tags)
        for tag in clean_tags:
            if tag not in self.tags:
                self.tags.append(tag)
        self.updated_at = datetime.now()

    def remove_tag(self, tag: str) -> None:
        valid, clean_tags = validate_tags([tag])
        if not valid:
            raise ValueError(clean_tags)
        if not clean_tags:
            raise ValueError("❌ Тег не може бути порожнім")
        clean_tag = clean_tags[0]
        if clean_tag not in self.tags:
            raise ValueError(f"Тег '{tag}' не знайдено в нотатці.")
        self.tags.remove(clean_tag)
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

    def add_note(self, title: str, text: str, tags: Optional[list[str]] = None) -> Note:
        valid, clean_title = validate_note_title(title)
        if not valid:
            raise ValueError(clean_title)

        valid, clean_text = validate_note_text(text)
        if not valid:
            raise ValueError(clean_text)

        valid, clean_tags = validate_tags(tags or [])
        if not valid:
            raise ValueError(clean_tags)

        if clean_title in self.data:
            raise ValueError(f"Нотатка з назвою '{clean_title}' вже існує.")

        note = Note(clean_title, clean_text, clean_tags)
        self.data[note.title] = note
        return note

    def edit_note(self, title: str, new_text: str) -> Note:
        valid, clean_title = validate_note_title(title)
        if not valid:
            raise ValueError(clean_title)

        valid, clean_text = validate_note_text(new_text)
        if not valid:
            raise ValueError(clean_text)

        note = self.data.get(clean_title)
        if note is None:
            raise KeyError(f"Нотатку '{clean_title}' не знайдено.")
        note.text = clean_text
        note.updated_at = datetime.now()
        return note

    def delete_note(self, title: str) -> None:
        valid, clean_title = validate_note_title(title)
        if not valid:
            raise ValueError(clean_title)
        if clean_title not in self.data:
            raise KeyError(f"Нотатку '{clean_title}' не знайдено.")
        del self.data[clean_title]

    def add_tags(self, title: str, tags: list[str]) -> Note:
        valid, clean_title = validate_note_title(title)
        if not valid:
            raise ValueError(clean_title)
        note = self.data.get(clean_title)
        if note is None:
            raise KeyError(f"Нотатку '{clean_title}' не знайдено.")
        note.add_tags(tags)
        return note

    def remove_tag(self, title: str, tag: str) -> Note:
        valid, clean_title = validate_note_title(title)
        if not valid:
            raise ValueError(clean_title)
        note = self.data.get(clean_title)
        if note is None:
            raise KeyError(f"Нотатку '{clean_title}' не знайдено.")
        note.remove_tag(tag)
        return note

    def search_by_title(self, query: str) -> list[Note]:
        q = query.strip().lower()
        return [note for note in self.data.values() if q in note.title.lower()]

    def search_by_tag(self, tag: str) -> list[Note]:
        # Шукає нотатки де конкретний тег точно є у списку
        t = tag.strip().lower()
        return [note for note in self.data.values() if t in note.tags]

    def sort_by_title(self) -> list[Note]:
        return sorted(self.data.values(), key=lambda note: note.title.lower())

    def sort_by_date(self) -> list[Note]:
        # Сортує за датою оновлення (новіші перші)
        return sorted(self.data.values(), key=lambda note: note.updated_at, reverse=True)

    def sort_by_tag(self) -> list[Note]:
        # Нотатки з тегами — перші (відсортовані за першим тегом), без тегів — в кінці
        with_tags = sorted(
            [n for n in self.data.values() if n.tags],
            key=lambda note: note.tags[0]
        )
        without_tags = [n for n in self.data.values() if not n.tags]
        return with_tags + without_tags

# Обробники команд
@input_error
def add_note_handler(notebook: NoteBook, args: list) -> str:
    """Додає нотатку. Якщо args порожній, запитує назву та текст у користувача."""
    if not args:
        title = input("Назва нотатки: ").strip()
        text = input("Текст нотатки: ").strip()
    else:
        title = args[0]
        text = " ".join(args[1:])
    note = notebook.add_note(title, text)
    return f"✅ Нотатку '{note.title}' додано."

@input_error
def edit_note_handler(notebook: NoteBook, args: list) -> str:
    """Редагує нотатку. Якщо args порожній, запитує назву та текст у користувача."""
    if not args:
        title = input("Назва нотатки для редагування: ").strip()
    else:
        title = " ".join(args)
    new_text = input("Новий текст: ").strip()
    note = notebook.edit_note(title, new_text)
    return f"✅ Нотатку '{note.title}' оновлено."

@input_error
@require_args(1, "Використання: delete-note <назва>", args_index=1)
def delete_note_handler(notebook: NoteBook, args: list) -> str:
    title = " ".join(args)
    notebook.delete_note(title)
    return f"✅ Нотатку '{title}' видалено."

@input_error
def add_tags_handler(notebook: NoteBook, args: list) -> str:
    """Додає теги до нотатки. Якщо args порожній, запитує назву та текст у користувача."""
    if not args:
        title = input("Назва нотатки: ").strip()
    else:
        title = " ".join(args)
    raw = input("Теги (через пробіл): ").strip()
    tags = raw.split() if raw else []
    if not tags:
        return "❌ Теги не можуть бути порожніми."
    note = notebook.add_tags(title, tags)
    return f"✅ Теги {note.tags} додано до '{note.title}'."

@input_error
def remove_tag_handler(notebook: NoteBook, args: list) -> str:
    """Видаляє тег з нотатки. Якщо args порожній, запитує назву та текст у користувача."""
    if not args:
        title = input("Назва нотатки: ").strip()
    else:
        title = " ".join(args)
    tag = input("Тег для видалення: ").strip()
    if not tag:
        return "❌ Тег не може бути порожнім."
    note = notebook.remove_tag(title, tag)
    return f"✅ Тег '{tag}' видалено з '{note.title}'."

@input_error
@require_args(1, "Використання: search-note <запит>", args_index=1)
def search_by_title_handler(notebook: NoteBook, args: list):
    query = " ".join(args)
    results = notebook.search_by_title(query)
    if not results:
        return f"📭 Нотаток з назвою '{query}' не знайдено."
    return results

@input_error
@require_args(1, "Використання: search-tag <тег>", args_index=1)
def search_by_tag_handler(notebook: NoteBook, args: list):
    tag = args[0]
    results = notebook.search_by_tag(tag)
    if not results:
        return f"📭 Нотаток з тегом '{tag}' не знайдено."
    return results

def sort_by_title_handler(notebook: NoteBook, args: list):
    results = notebook.sort_by_title()
    if not results:
        return "📭 Нотаток ще немає."
    return results

def sort_by_date_handler(notebook: NoteBook, args: list):
    results = notebook.sort_by_date()
    if not results:
        return "📭 Нотаток ще немає."
    return results

def sort_by_tag_handler(notebook: NoteBook, args: list):
    results = notebook.sort_by_tag()
    if not results:
        return "📭 Нотаток ще немає."
    return results

def all_notes_handler(notebook: NoteBook, args: list):
    return sort_by_date_handler(notebook, args)