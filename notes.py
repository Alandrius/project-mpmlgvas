from datetime import datetime
from collections import UserDict


class Note:
    def __init__(self, title: str, text: str):
        self.title: str = title.strip()
        self.text: str = text.strip()
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = self.created_at

    def __str__(self) -> str:
        return (
            f"[{self.title}]\n"
            f"   Текст   : {self.text}\n"
            f"   Створено: {self.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            f"   Змінено : {self.updated_at.strftime('%d.%m.%Y %H:%M')}"
        )

class NoteBook(UserDict):
    def add_note(self, title: str, text: str) -> Note:
        if title.strip() in self.data:
            raise ValueError(f"Нотатка з назвою '{title}' вже існує.")
        note = Note(title, text)
        self.data[note.title] = note
        return note
    
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