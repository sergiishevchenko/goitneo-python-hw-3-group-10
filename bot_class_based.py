from collections import UserDict
from datetime import datetime

import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        self.name = name


class Phone(Field):
    def validate(self, phone):
        try:
            return re.match(r'(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+', phone)
        except ValueError:
            raise ValueError("Incorrect phone format.")


class Birthday:
    def __init__(self, birthday):
        self.birthday = birthday

    def validate(self):
        try:
            datetime.strptime(self.birthday, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        self.phones.remove(old_phone)
        self.phones.append(new_phone)

    def find_phone(self, phone: Phone):
        if phone in self.phones:
            return phone

    def add_birthday(self, name, birthday: Birthday):
        self.birthday = birthday
        self.name = name

    def show_birthday(self, name):
        self.name = name
        if self.name:
            return self.birthday

    def remove_phone(self, phone: Phone):
        self.phones.remove(phone)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def __init__(self, data):
        self.data = data

    def add_record(self, record: Record):
        self.data.update(record)

    def find(self, name):
        if name in self.data.keys():
            return {name, self.data[name]}

    def delete(self, name):
        del self.data[name]

    def get_all_records(self):
        return self.data

    def get_birthdays_per_week(self):
        result = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
        today = datetime.today().date()

        for user in self.data:
            name = user['name']
            birthday = user['birthday']
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

        for key, value in result.items():
            if value:
                print('{}: {}'.format(key, ', '.join(value)))


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
    return inner


def change_contact_error(func):
    def inner(*args, **kwargs):
        if not args[0]:
            return 'Give me name and phone, please.'
        elif args[0][0] not in args[1].keys():
            return 'User does not exists.'
        elif len(args[0]) == 1:
            return 'Give me phone too, please.'
        else:
            return func(*args, **kwargs)
    return inner


def get_phone_error(func):
    def inner(*args, **kwargs):
        if not args[0]:
            return 'Give me name, please.'
        elif args[0][0] not in args[1].keys():
            return 'User does not exists.'
        else:
            return func(*args, **kwargs)
    return inner


def hello_command(args, contacts):
    return 'How can I help you?'


def exit_command(args, contacts):
    return 'Good bye!'


def unknown_command(args, contacts):
    return 'Unknown command'


COMMAND_HANDLER = {
    hello_command: ['hello', 'hi', 'привет'],
    exit_command: ['exit', 'bye', 'close'],
    add_contact: ['add', '+', 'добавить'],
    change_contact: ['change', 'поменять'],
    get_phone: ['phone', 'телефон'],
    get_all: ['all', 'все', 'всё']
}


def parser(user_input: str):
    for cmd, words in COMMAND_HANDLER.items():
        for word in words:
            if user_input.startswith(word):
                return cmd, user_input[len(word):].split()
    return unknown_command, []


def main():
    print('Welcome to the assistant bot!')

    contacts = {}
    while True:
        user_input = input('Enter a command: ')
        cmd, data = parser(user_input)
        print(cmd(data, contacts))
        if cmd == exit_command:
            break


if __name__ == '__main__':
    main()