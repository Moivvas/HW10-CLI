import sys
import ast
from collections import UserDict


class Field:
    
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name, phone=None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
    
    def add_phone(self, phone):
        self.phones.append(phone)
    
    def add_phones(self, phones):
        self.phones.extend(phones)
    
    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone.value:
                self.phones[idx] = new_phone
                return f"phone {old_phone} change to phone {new_phone}"
        return f"Contact {self.name} has no phone {old_phone}"
    
    def __str__(self):
        return f"{str(self.name)}:{','.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[str(record.name)] = record        
        # data = {f'{record.name.value}': record.phone.value}
        # with open('phone_book.txt', 'a') as pb:
        #     pb.write(f"{data}" + '\n')
        return "add record success"

    def show_all(self):
        return "\n".join(str(rec) for rec in self.values())

    def load_data(self, file):
        with open(file) as f:
            lines = f.readlines()
        for line in lines:
            line = line.replace("\n", "")
            raw_name, raw_phones = line.split(":")
            name = Name(raw_name)
            phones = [Phone(p) for p in raw_phones.split(",")]
            rec = Record(name)
            rec.add_phones(phones)
            self.add_record(rec)
    
    def save_data(self, file):
        with open(file, "w") as f:
            f.write(self.show_all())
            
ab = AddressBook()
filename = "phone_book.txt"

def input_error(func):
    def handler(*args):
        return_text = """<<< Please check your input
        add "Name" "phone"
        change "Name" "phone"
        phone "Name"
        show all
        exit"""
        try:
            return func(*args)

        except TypeError:
            return return_text

        except IndexError:
            return return_text

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

    # if is_name_occupied(name.value):
    #     return '<<<This name is occupied'
    record = Record(name,phone)
    # address_book = AddressBook()
    return ab.add_record(record)
    

    # return f'<<< Add success {name.value.capitalize()} {phone.value}'


@input_error
def change(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    # print(name.value)
    # print(new_phone.value)

    rec = ab.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    # address_book = AddressBook()
    # return address_book.change_record(new_record) if True else f'{name.value} is not in phne book'
    return f"Address book has no contact with name {name}"

def show_all(*args):
    # address_book = AddressBook()
    return ab.show_all()

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


def exit_program(*args):
    return 'Good Bye'
    # sys.exit(0)


def no_command(*args):
    return '\n***Unknown command***\nCommand available:\nadd "Name" "phone"\nchange "Name" "phone"\nphone "Name"\ndelete "Name"\nshow all\nexit'


def hello_command(*args):
    return '<<< Hi, how can I help you?\nCommand available:\nadd "Name" "phone"\nchange "Name" "phone"\nphone "Name"\ndelete "Name"\nshow all\nexit'


command_dict = {
    'add': add,
    'change': change,
    'phone': phones,
    'show_all': show_all,
    'delete': delete,
    'exit': exit_program,
    'close': exit_program,
    'hello': hello_command,
}


def parser(text: str) -> tuple[callable, list[str] | list[None]]:
    text = text.lower()
    command_parts = text.split(maxsplit=1)
    command = command_parts[0]
    data = command_parts[1].strip() if len(command_parts) > 1 else []

    if command in command_dict:
        return command_dict[command], list(data.split()) if data else []
    else:
        return no_command, []


def main():
    ab.load_data(filename)
    print("Enter 'Hello' to start")
    while True:
        user_input = input('>>>')
        # if user_input.lower() == 'hello':
        #     print()
        # # elif user_input.lower() in ('good bye', 'exit', 'close'):
        # #     print('Good Bye')
        # #     break
        # else:
        command, data = parser(user_input)
        # if data is not None:
        #     result = command(*data)
        # else:
        #     result = command()
        print(command(*data))
        ab.save_data(filename)
        if command == exit_program:
            break


if __name__ == "__main__":
    main()