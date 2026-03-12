from datetime import datetime, timedelta
from validation import (
    validate_name,
    validate_phone,
    validate_email,
    validate_birthday,
)

class Contact:
    """Клас для одного контакту"""
    def __init__(self, name, address="", phone="", email="", birthday=""):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday
    
    def days_to_birthday(self):
        """Скільки днів до дня народження"""
        if not self.birthday:
            return None
        
        today = datetime.now().date()
        bday = datetime.strptime(self.birthday, "%Y-%m-%d").date()
        next_bday = bday.replace(year=today.year)
        
        if next_bday < today:
            next_bday = next_bday.replace(year=today.year + 1)
        
        return (next_bday - today).days

class AddressBook:
    """Клас для книги контактів"""
    def __init__(self):
        self.contacts = []
    
    def add_contact(self, contact):
        self.contacts.append(contact)
        return True
    
    def get_all_contacts(self):
        return self.contacts
    
    def search_contacts(self, search_text):
        results = []
        search_text = search_text.lower()
        for contact in self.contacts:
            if (search_text in contact.name.lower() or 
                search_text in contact.phone or 
                search_text in contact.email.lower()):
                results.append(contact)
        return results
    
    def find_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                return contact
        return None
    
    def delete_contact(self, name):
        for i, contact in enumerate(self.contacts):
            if contact.name.lower() == name.lower():
                return self.contacts.pop(i)
        return None
    
    def get_birthdays_in_days(self, days):
        results = []
        target_date = datetime.now().date() + timedelta(days=days)
        
        for contact in self.contacts:
            if contact.birthday:
                days_to = contact.days_to_birthday()
                if days_to == days:
                    results.append(contact)
        return results


def add_contact_handler(book, args):
    """Додавання нового контакту з валідацією"""
    if len(args) < 2:
        print("❌ Потрібно вказати ім'я та телефон. Приклад: add Іван 0501234567")
        return
    
    name_input = args[0]
    phone_input = args[1]
    
    # Валідація імені
    valid, name = validate_name(name_input)
    if not valid:
        print(name)
        return
    
    # Валідація телефону
    valid, phone = validate_phone(phone_input)
    if not valid:
        print(phone)
        return
    
    # Email (необов'язковий)
    email = ""
    if len(args) > 2:
        valid, email = validate_email(args[2])
        if not valid:
            print(email)
            return
    
    # День народження (необов'язковий)
    birthday_input = input("День народження (РРРР-ММ-ДД, або Enter щоб пропустити): ")
    valid, birthday = validate_birthday(birthday_input)
    if not valid:
        print(birthday)
        return
    
    contact = Contact(name, phone=phone, email=email, birthday=birthday)
    book.add_contact(contact)
    print(f"✅ Контакт {name} додано!")

def search_contacts_handler(book, args):
    """Пошук контактів"""
    if not args:
        print("❌ Вкажи текст для пошуку. Приклад: search Іван")
        return
    
    search_text = " ".join(args)
    results = book.search_contacts(search_text)
    
    if not results:
        print(f"❌ Нічого не знайдено за запитом '{search_text}'")
    else:
        print(f"✅ Знайдено {len(results)} контактів:")
        for contact in results:
            print(f"  📌 {contact.name}")
            print(f"     📞 {contact.phone}")
            if contact.email:
                print(f"     ✉️ {contact.email}")
            if contact.address:
                print(f"     🏠 {contact.address}")
            if contact.birthday:
                days = contact.days_to_birthday()
                if days == 0:
                    print("     🎂 СЬОГОДНІ ДЕНЬ НАРОДЖЕННЯ!")
                elif days:
                    print(f"     🎂 До дня народження {days} днів")

def edit_contact_handler(book, args):
    """Редагування контакту з валідацією"""
    if not args:
        print("❌ Вкажи ім'я контакту для редагування. Приклад: edit Іван")
        return
    
    name = " ".join(args)
    contact = book.find_contact(name)
    
    if not contact:
        print(f"❌ Контакт '{name}' не знайдено")
        return
    
    print(f"\nРедагуємо контакт: {contact.name}")
    print("(Залиш поле порожнім, щоб не змінювати)")
    
    # Редагування імені
    new_name = input(f"Ім'я [{contact.name}]: ")
    if new_name:
        valid, result = validate_name(new_name)
        if valid:
            contact.name = result
        else:
            print(result)
    
    # Редагування телефону
    new_phone = input(f"Телефон [{contact.phone}]: ")
    if new_phone:
        valid, result = validate_phone(new_phone)
        if valid:
            contact.phone = result
        else:
            print(result)
    
    # Редагування email
    new_email = input(f"Email [{contact.email}]: ")
    if new_email:
        valid, result = validate_email(new_email)
        if valid:
            contact.email = result
        else:
            print(result)
    
    # Редагування дня народження
    new_birthday = input(f"День народження [{contact.birthday}]: ")
    if new_birthday:
        valid, result = validate_birthday(new_birthday)
        if valid:
            contact.birthday = result
        else:
            print(result)
    
    print(f"✅ Контакт оновлено!")

def delete_contact_handler(book, args):
    """Видалення контакту"""
    if not args:
        print("❌ Вкажи ім'я контакту для видалення. Приклад: delete Іван")
        return
    
    name = " ".join(args)
    deleted = book.delete_contact(name)
    
    if deleted:
        print(f"✅ Контакт '{name}' видалено")
    else:
        print(f"❌ Контакт '{name}' не знайдено")

def show_birthdays_handler(book, args):
    """Показати іменинників"""
    if not args:
        print("❌ Вкажи кількість днів. Приклад: birthdays 7")
        return
    
    try:
        days = int(args[0])
    except ValueError:
        print("❌ Вкажи число днів. Приклад: birthdays 7")
        return
    
    results = book.get_birthdays_in_days(days)
    
    if not results:
        print(f"📭 Немає іменинників через {days} днів")
    else:
        print(f"🎂 Іменинники через {days} днів:")
        for contact in results:
            print(f"  {contact.name} - {contact.birthday}")