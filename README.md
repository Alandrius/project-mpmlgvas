## goit-pycore-personal-assistant

### Project structure and main classes

- **`assistant.py`**
  - Application launcher and main command loop; routes commands to contacts and notes.

- **`contacts.py`**
  - **`Contact`**: a contact entity (name, phone, email, address, birthday, etc.).
  - **`AddressBook`**: contact storage, search, edit, and delete functionality.

- **`notes.py`**
  - **`Note`**: a note entity.
  - **`Notebook`**: note collection with add/search/edit/delete operations.

- **`validation.py`**
  - **`input_error`**: decorator for consistent CLI error handling.

### Run unit tests

Project has basic unit tests for main flows in:

- `tests/test_validation.py`
- `tests/test_contacts.py`
- `tests/test_notes.py`

Run all tests:

```bash
# from project root
python3 -m unittest discover -s tests -p "test_*.py"
```

Run one file (example):

```bash
python3 -m unittest tests/test_contacts.py
```

Expected result: all tests pass (`OK`).

---

## Running the assistant

From the project root, run:

```bash
python assistant.py
```

The app starts with a help screen showing all available commands.

### Common commands

Once running, you can use commands such as:

- `add` / `add-contact` — add a contact
- `search` / `search-contact` — search contacts
- `edit` / `edit-contact` — edit a contact
- `delete` / `delete-contact` — delete a contact
- `birthdays` / `bday` — list upcoming birthdays
- `show-all` / `contacts` — show all contacts

- `add-note` — add a note (interactive)
- `edit-note` — edit a note
- `delete-note` — delete a note
- `add-tags` — add tags to a note
- `remove-tag` — remove a tag from a note
- `all-notes` — list notes
- `search-note` — search notes by title
- `search-tag` — search notes by tag
- `sort-notes-title` — sort notes by title
- `sort-notes-date` — sort notes by date
- `sort-notes-tag` — sort notes by tag

- `close` / `exit` — exit the app

## Dependencies

This project optionally uses:

- `colorama` (for colored CLI output)
- `tabulate` (for table formatting)

If you want those features, install them with:

```bash
pip install colorama tabulate
```
