from datetime import datetime, timedelta

class Contact:
    """Клас для одного контакту"""
    def __init__(self, name, address="", phone="", email="", birthday=""):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday  # формат: "YYYY-MM-DD"
    
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
        """Додати контакт"""
        self.contacts.append(contact)
        return True
    
    def get_all_contacts(self):
        """Отримати всі контакти"""
        return self.contacts
    
    def search_contacts(self, search_text):
        """Пошук контактів за ім'ям, телефоном або email"""
        results = []
        search_text = search_text.lower()
        for contact in self.contacts:
            if (search_text in contact.name.lower() or 
                search_text in contact.phone or 
                search_text in contact.email.lower()):
                results.append(contact)
        return results
    
    def find_contact(self, name):
        """Знайти контакт за точним ім'ям"""
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                return contact
        return None
    
    def delete_contact(self, name):
        """Видалити контакт за ім'ям"""
        for i, contact in enumerate(self.contacts):
            if contact.name.lower() == name.lower():
                return self.contacts.pop(i)
        return None
    
    # 👇 НОВИЙ МЕТОД ДЛЯ ДНІВ НАРОДЖЕННЯ
    def get_birthdays_in_days(self, days):
        """Повертає список контактів, у яких день народження через вказану кількість днів"""
        results = []
        target_date = datetime.now().date() + timedelta(days=days)
        
        for contact in self.contacts:
            if contact.birthday:
                days_to = contact.days_to_birthday()
                if days_to == days:
                    results.append(contact)
        
        return results