import sys
import ast
from collections import UserDict

class Field:
    
    def __init__(self, value) -> None:
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name, phone=None) -> None:
        self.name = name
        self.phone = phone


class AddressBook(UserDict):

    def add_record(self, record):
        
        data = {f'{record.name.value}': record.phone.value}
        with open('phone_book.txt', 'a') as pb:
            pb.write(f"{data}" + '\n')
        return "add_record success"

    def change_record(self, new_record):
        found = False
        with open('phone_book.txt', 'r') as pb:
            lines = pb.readlines()

        with open('phone_book.txt', 'w') as pb:
            for line in lines:
                record_dict = ast.literal_eval(line)
                name = list(record_dict.keys())[0]
                if name == new_record.name.value:
                    record_dict[name] = new_record.phone.value
                    found = True
                pb.write(f"{record_dict}\n")

        if found:
            return f'<<< Change success: {new_record.name.value.capitalize()} has a new phone {new_record.phone.value}'
        else:
            return f'{new_record.name.value} is not in phone book'

    def read_file(self):
        with open('phone_book.txt', 'r') as pb:
            lines = pb.readlines()

        contacts = [f"{list(ast.literal_eval(line).keys())[0].capitalize()} : {list(ast.literal_eval(line).values())[0]}" for line in lines]

        return '\n'.join(contacts)

    def delete(self, name):
        name = str(name.value)
        with open('phone_book.txt', 'r') as pb:
            lines = pb.readlines()

        new_lines = []
        for line in lines:
            record_dict = ast.literal_eval(line)
            if list(record_dict.keys())[0] != name:
                new_lines.append(line)

        with open('phone_book.txt', 'w') as pb:
            pb.writelines(new_lines)

        return f"Delete {name.capitalize()} success"

    def search_by_name(self, name):
        with open('phone_book.txt', 'r') as pb:
            lines = pb.readlines()

        for line in lines:
            record_dict = ast.literal_eval(line)
            if name.value in record_dict:
                return f"{name.value.capitalize()} phone is {record_dict[name.value]}"

        return f"No phone number found for {name.value.capitalize()}"


def input_error(func):
    def handler(*args):
        try:
            return func(*args)

        except TypeError:
            return '<<< Please check your input\nadd "Name" "phone"\nchange "Name" "phone"\nphone "Name"\nshow all\nexit'

        except IndexError:
            return '<<< Please correct your input\nadd "Name" "phone"\nchange "Name" "phone"\nphone "Name"\nshow all\nexit'

    return handler


def is_name_occupied(name):
    with open('phone_book.txt', 'r') as pb:
        lines = pb.readlines()

    for line in lines:
        record_dict = ast.literal_eval(line)
        if name in record_dict:
            return True

    return False



@input_error
def add(*args):
    name = Name(args[0])
    phone = Phone(args[1])

    if is_name_occupied(name.value):
        return '<<<This name is occupied'
    record = Record(name,phone)
    address_book = AddressBook()
    address_book.add_record(record)
    

    return f'<<< Add success {name.value.capitalize()} {phone.value}'


@input_error
def change(*args):
    name = Name(args[0])
    new_phone = Phone(args[1])
    print(name.value)
    print(new_phone.value)

    new_record = Record(name, new_phone)
    address_book = AddressBook()
    return address_book.change_record(new_record) if True else f'{name.value} is not in phne book'


def show_all():
    address_book = AddressBook()
    return address_book.read_file()

@input_error
def delete(*args):
    name = Name(args[0])
    address_book = AddressBook()
    return address_book.delete(name)

@input_error
def phones(*args):
    name = Name(args[0])
    address_book = AddressBook()
    return address_book.search_by_name(name)


def exit_program():
    print('Good Bye')
    sys.exit(0)


def no_command(*args):
    return '\n***Unknown command***\nCommand available:\nadd "Name" "phone"\nchange "Name" "phone"\nphone "Name"\ndelete "Name"\nshow all\nexit'


command_dict = {
    'add': add,
    'change': change,
    'phone': phones,
    'show_all': show_all,
    'delete': delete,
    'exit': exit_program,
    'close': exit_program,
}


def parser(text: str) -> tuple[callable, list[str] | None]:
    text = text.lower()
    command_parts = text.split(maxsplit=1)
    command = command_parts[0]
    data = command_parts[1].strip() if len(command_parts) > 1 else None

    if command in command_dict:
        return command_dict[command], list(data.split()) if data else None
    else:
        return no_command, None


def main():
    print("Enter 'Hello' to start")
    while True:
        user_input = input('>>>')
        if user_input.lower() == 'hello':
            print('<<< Hi, how can I help you?\nCommand available:\nadd "Name" "phone"\nchange "Name" "phone"\nphone "Name"\ndelete "Name"\nshow all\nexit')
        elif user_input.lower() in ('good bye', 'exit', 'close'):
            print('Good Bye')
            break
        else:
            command, data = parser(user_input)
            if data is not None:
                result = command(*data)
            else:
                result = command()
            print(result)


if __name__ == "__main__":
    main()