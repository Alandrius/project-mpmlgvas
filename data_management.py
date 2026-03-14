import pickle

from contacts import AddressBook
from notes import NoteBook


DATA_FILE = "assistant_data.pkl"


def save_data(book, notebook, filename=DATA_FILE):
    """Save contacts and notes to disk."""
    data = {
        "book": book,
        "notebook": notebook,
    }
    with open(filename, "wb") as file:
        pickle.dump(data, file)


def load_data(filename=DATA_FILE):
    """Load contacts and notes from disk."""
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
            book = data.get("book", AddressBook())
            notebook = data.get("notebook", NoteBook())
            return book, notebook
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return AddressBook(), NoteBook()
