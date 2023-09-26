from collections import UserDict
from datetime import datetime
from itertools import chain

import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    ...


class Phone(Field):

    def validate(self):
        return re.match(r'(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', self.value)


class Birthday(Field):

    def validate(self):
        pattern = "^\d{2}.\d{2}.\d{4}$"
        return re.match(pattern, self.value)


class Record:
    def __init__(self, name: Name, phone: Phone):
        self.name = name
        self.phones = [phone]

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        self.phones.remove(old_phone)
        self.phones.append(new_phone)

    def find_phone(self, name: Name):
        self.name = name
        if self.name:
            return self.phones

    def add_birthday(self, name: Name, birthday: Birthday):
        self.birthday = birthday
        self.name = name

    def show_birthday(self, name: Name):
        self.name = name
        if self.name:
            return self.birthday.value

    def remove_phone(self, phone: Phone):
        self.phones.remove(phone)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self[record.name.value] = record

    def find(self, name: Name):
        if name.value in list(self.keys()):
            return self[name.value]

    def delete(self, name):
        del self.data[name]

    def get_all_records(self):
        return self.data

    def get_birthdays_per_week(self):
        result = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
        today = datetime.today().date()
        for key, value in self.items():
            name = key
            birthday = datetime.strptime(value.birthday.value, '%d.%m.%Y').date()
            if (birthday.month == 2 and birthday.day == 29):
                day = birthday.day - 1
                birthday_this_year = birthday.replace(year=today.year, day=day)
            else:
                birthday_this_year = birthday.replace(year=today.year)
            delta_days = (birthday_this_year - today).days
            if birthday_this_year >= today and delta_days < 7:
                if birthday.strftime('%A') in result.keys():
                    result[birthday.strftime('%A')].append(name)
                else:
                    result['Monday'].append(name)

        return list(chain(*result.values()))
