from classes import Name, Phone, Record, AddressBook, Birthday


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Give me name and phone please."
        except KeyError:
            return 'User does not exists.'
    return inner


def hello_command(args, contacts):
    return 'How can I help you?'


def exit_command(args, contacts):
    return 'Good bye!'


def unknown_command(args, contacts):
    return 'Unknown command'


@input_error
def add_contact(args, contacts: AddressBook):
    name = Name(args[0])
    phone = Phone(args[1])

    if phone.validate():
        contacts.add_record(Record(name, phone))
        return 'Contact added.'
    return 'Incorrect phone format.'


@input_error
def change_contact(args, contacts: AddressBook):
    name = Name(args[0])
    new_phone = Phone(args[1])

    if new_phone.validate():
        old_record = contacts.find(name)
        if old_record:
            old_phone = old_record.phones[0]
            old_record.edit_phone(old_phone, new_phone)
            return 'Contact changed.'
        return 'User does not exists.'
    return 'Incorrect phone format.'


@input_error
def get_phone(args, contacts: AddressBook):
    name = args
    return contacts[name[0]]


def get_all(args, contacts: AddressBook):
    return contacts


@input_error
def add_birthday(args, contacts: AddressBook):
    name = Name(args[0])
    birthday = Birthday(args[1])

    if birthday.validate():
        record = contacts.find(name)
        if record:
            record.add_birthday(name, birthday)
            return 'Birthday added.'
        return 'User does not exists.'
    return 'Incorrect data format, should be DD.MM.YYYY'


@input_error
def get_birthday(args, contacts: AddressBook):
    name = Name(args[0])
    record = contacts.find(name)
    if record:
        return record.show_birthday(name.value)


def get_birthdays_per_week(args, contacts: AddressBook):
    return contacts.get_birthdays_per_week()


COMMAND_HANDLER = {
    add_contact: ['add', '+', 'добавить'],
    change_contact: ['change', 'поменять'],
    get_phone: ['phone', 'телефон'],
    get_all: ['all', 'все', 'всё'],
    add_birthday: ['birth'],
    get_birthday: ['show'],
    get_birthdays_per_week: ['week'],
    hello_command: ['hello', 'hi', 'привет'],
    exit_command: ['exit', 'bye', 'close'],
}


def parser(user_input: str):
    for cmd, words in COMMAND_HANDLER.items():
        for word in words:
            if user_input.startswith(word):
                return cmd, user_input[len(word):].split()
    return unknown_command, []


def main():
    print('Welcome to the assistant bot!')

    contacts = AddressBook()
    while True:
        user_input = input('Enter a command: ')
        cmd, data = parser(user_input)
        print(cmd(data, contacts))
        if cmd == exit_command:
            break


if __name__ == '__main__':
    main()