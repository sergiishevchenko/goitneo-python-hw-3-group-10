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


@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return 'Contact added.'


@change_contact_error
def change_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return 'Contact changed.'


def get_all(args, contacts):
    return contacts


@get_phone_error
def get_phone(args, contacts):
    name = args
    return contacts[name[0]]


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