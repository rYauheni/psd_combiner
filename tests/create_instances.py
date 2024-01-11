import os
import random
import string

from c_converter.currencies import CURRENCIES_SYMBOLS


def create_directories():
    current_directory = os.getcwd()
    instances_directory = os.path.join(current_directory, 'instances')
    common_instances_directory = os.path.join(instances_directory, 'common_instances')

    if not os.path.exists(instances_directory):
        os.mkdir(instances_directory)

    if not os.path.exists(common_instances_directory):
        os.mkdir(common_instances_directory)


def generate_filename(length=16, extension=".txt"):
    characters = string.ascii_letters + string.digits
    random_name = ''.join(random.choice(characters) for _ in range(length))
    filename = random_name + extension

    return filename


def generate_amount():
    integer_part = random.randint(0, 10_000)
    fractional_part = 0
    if not random.randint(0, 9):
        fractional_part = round(random.random(), 2)
    amount = integer_part + fractional_part

    return amount


def generate_currency():
    currencies = CURRENCIES_SYMBOLS
    currency = random.choice(currencies)

    return currency


def generate_re_entry():
    re_entry = ''
    if not random.randint(0, 9):
        quantity = random.randint(1, 12)
        re_entry = f'made {quantity} re-entries and '

    return re_entry


def create_instances(quantity=22_000):
    create_directories()
    directory_path = os.path.join(os.getcwd(), "instances", "common_instances")

    for i in range(quantity):
        if i % 1_000 == 0:
            print(i)

        file_name = generate_filename()

        file_path = os.path.join(directory_path, file_name)

        bi = generate_amount()
        tr = generate_amount()
        c = generate_currency()
        re = generate_re_entry()

        content = f"Tournament #104197479, WSOP Online: {c}{bi} Bounty Hunters Daily Deepstack, Hold'em No Limit\n" \
                  f"Buy-in: {c}{bi}+{c}0+{c}0\n" \
                  f"7016 Players\n" \
                  f"Total Prize Pool: {c}350,800\n" \
                  f"Tournament started 2023/09/23 18:30:00\n" \
                  f"3481th : Hero, {c}0\n" \
                  f"You finished the tournament in 3481th place.\n" \
                  f"You {re}received a total of {c}{tr}.\n\n\n"

        with open(file_path, "w", encoding='utf-8') as file:
            file.write(content)


def main():
    create_instances()


if __name__ == '__main__':
    main()
