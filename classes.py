from collections import UserDict
from datetime import datetime
from itertools import chain

import re
import pickle


class IsCorrectPhoneFormat(Exception):
    pass


class IsCorrectDateFormat(Exception):
    pass


class IsRecordInContacts(Exception):
    pass


class IsBirthdayInRecord(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    ...


class Phone(Field):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if re.match(r'(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', new_value):
            self._value = new_value
        else:
            raise IsCorrectPhoneFormat('Incorrect phone format: should be 10-digit number.')

    def __repr__(self):
        return self._value


class Birthday(Field):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if re.match(r'\d{2}.\d{2}.\d{4}', new_value):
            self._value = new_value
        else:
            raise IsCorrectPhoneFormat('Incorrect date format: should be DD.MM.YYYY.')

    def __repr__(self):
        return self._value


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

    def show_birthday(self):
        if self.birthday:
            return self.birthday.value
        else:
            raise IsBirthdayInRecord('There is no birthday in Record. You do not add the birthday to Record.')

    def remove_phone(self, phone: Phone):
        self.phones.remove(phone)

    def __repr__(self):
        return f'Record | {self.name}:{self.phones}'


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self[record.name.value] = record

    def find(self, name: Name):
        if name.value in list(self.keys()):
            return self[name.value]
        else:
            raise IsRecordInContacts('Record does not exists.')

    def delete(self, name):
        del self[name.value]

    def get_birthdays_per_week(self):
        result = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
        today = datetime.today().date()

        for key, value in self.items():
            name = key
            birthday = datetime.strptime(value.birthday.value, '%d.%m.%Y').date()

            if (birthday.month == 2 and birthday.day == 29):
                day = birthday.day - 1
                birthday_this_year = birthday.replace(year=today.year, day=day)
            birthday_this_year = birthday.replace(year=today.year)

            delta_days = (birthday_this_year - today).days
            if birthday_this_year >= today and delta_days < 7:
                if birthday.strftime('%A') in result.keys():
                    result[birthday.strftime('%A')].append(name)
                result['Monday'].append(name)

        return list(chain(*result.values()))

    def dump(self, file):
        with open(file, 'wb') as fh:
            pickle.dump(self, fh)

    def load(self, file):
        try:
            with open(file, 'rb') as fh:
                dt = pickle.load(fh)
                self.update(dt)
            return True
        except:
            return False
