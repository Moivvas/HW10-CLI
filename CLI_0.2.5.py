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
    
    def delete_rec(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
            return f"Phone {phone} deleted"
        return f"Contact {self.name} has no phone {phone}"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[str(record.name)] = record
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
    
    def delete_record(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record {name} deleted"
        return f"No record found with name {name}"

    def search(self, search_field):
            results = []
            for record in self.values():
                if isinstance(search_field, Name) and search_field.value.lower() in record.name.value.lower():
                    phones = ', '.join(str(phone) for phone in record.phones)
                    results.append(f"{record.name} : {phones}")
                elif isinstance(search_field, Phone) and any(search_field.value == phone.value for phone in record.phones):
                    results.append(f"{record.name} : {search_field.value}")
            if results:
                return '\n'.join(results)
            return "No matching records found."


ab = AddressBook()
filename = "phone_book.txt"


def input_error(func):
    def handler(*args):
        return_text = """<<<Please check your input
        add "Name" "phone"
        change "Name" "old_phone" "new_phone"
        search "Field"
        show_all
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
    record = Record(name,phone)
    return ab.add_record(record)


@input_error
def change(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec = ab.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"Address book has no contact with name {name}"


def show_all(*args):
    return ab.show_all()


@input_error
def delete(*args):
    if len(args) != 1:
        return """<<< Please check your input <<< delete "Name" >>>"""
    name = Name(args[0])
    rec = ab.get(str(name))
    if rec:
        ab.delete_record(str(name))
        return f"Record {name} deleted"
    return f"Address book has no contact with name {name}"


@input_error
def search(*args):
    if args and args[0].isdigit():
        search_field = Phone(args[0])
    else:
        search_field = Name(args[0]) if args else None
    
    if search_field:
        return ab.search(search_field)
    return 'Please provide a search term'


def exit_program(*args):
    return 'Good Bye'


def no_command(*args):
    return '\n***Unknown command***\nCommand available:\nadd "Name" "phone"\nchange "Name" "old_phone" "new_phone"\nsearch "Field"\ndelete "Name"\nshow_all\nexit'


def hello_command(*args):
    return '<<< Hi, how can I help you?\nCommand available:\nadd "Name" "phone"\nchange "Name" "old_phone" "new_phone"\nsearch "Field"\ndelete "Name"\nshow_all\nexit'


command_dict = {
    'add': add,
    'change': change,
    'search': search,
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
        command, data = parser(user_input)
        print(command(*data))
        ab.save_data(filename)
        if command == exit_program:
            break


if __name__ == "__main__":
    main()