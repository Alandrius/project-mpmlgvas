## goit-pycore-personal-assistant

### Project structure and main classes

- **`assistant.py`**
  - Тут буде логіка запуску застосунку, обробка команд і взаємодія з контактами та нотатками.

- **`contacts.py`**
  - **`Contact`**: сутність контакту (ім’я, телефони, email, адреса, день народження тощо).
  - **`AddressBook`**: книга контактів, яка відповідатиме за зберігання, пошук, редагування та видалення контактів.

- **`notes.py`**
  - **`Note`**: сутність текстової нотатки.
  - **`Notebook`**: колекція нотаток, яка надаватиме інтерфейс для додавання, пошуку, редагування та видалення нотаток.

- **`validation.py`**
  - **`input_error`**: декоратор для обробки помилок.

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
