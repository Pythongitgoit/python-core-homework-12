from classes import *


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params."
        except KeyError:
            return "Unknown record_id."
        except ValueError:
            return "Error: Invalid value format."

    return inner


def parse_command(command: str):
    parts = command.split()
    if len(parts) < 1:
        return None, []
    action = parts[0].lower()
    args = parts[1:]
    return action, args


@user_error
def main():
    book = AddressBook()
    book.load_from_json()

    while True:
        user_input = input(
            f"{BLUE}Enter a command {RESET}(add/show(2)/find/edit/delete/exit(6)): "
        ).strip()

        if user_input == "exit" or user_input == "6":
            book.save_to_json()

            print(f"\u001b[0m\u001b[7m Goodbye! \u001b[0m")
            break

        action, args = parse_command(user_input)

        if action == "add":
            if len(args) >= 2:
                name = args[0]
                phone1 = args[1]
                phone2 = args[2] if len(args) > 2 else None
                birthday = args[3] if len(args) > 3 else None

                book.add_contact(name, phone1, phone2, birthday)
                book.save_to_json()
            else:
                print(f"Invalid arguments for {RED}'add'{RESET} command.")

        elif action == "show" or action == "2":
            page_size = input(f"{BLUE}Enter the number of records to display: {RESET}")
            try:
                page_size = int(page_size)
                for page in book.iterator(page_size):
                    for record in page:
                        print(record)
                    show_more = input(
                        f"{BLUE}Show more? Press(2) to continue or Press any key to return to the main menu:{RESET} "
                    )
                    if show_more.lower() != "2":
                        break
            except ValueError:
                print(f"{RED}Invalid number. Please enter a valid number.{RESET}")

        elif action == "edit":
            if len(args) == 3:
                name = args[0]
                old_phone = args[1]
                new_phone = args[2]

                record = book.find(name)

                if record:
                    try:
                        record.edit_phone(old_phone, new_phone)
                        print(
                            f"Phone number for {GREEN}'{name}'{RESET} edited successfully."
                        )
                    except ValueError as e:
                        print(str(e))
                else:
                    print(f"Contact {RED}'{name}'{RESET} not found.")
            else:
                print(f"{RED}Invalid arguments for 'edit' command.{RESET}")

        elif action == "find":
            if len(args) == 1:
                search_query = args[0]
                book.find_contact(search_query)
            else:
                print(f"{RED}Invalid arguments for 'find' command.{RESET}")

        elif action == "delete":
            if len(args) == 1:
                name = args[0]
                book.delete_contact(name)
            else:
                print(f"{RED}Invalid arguments for 'delete' command.{RESET}")

        else:
            print(f"{RED}Unknown command. Try again.{RESET}")


if __name__ == "__main__":
    main()
