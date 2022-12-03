import argparse
import os
import random
from typing import Optional
import sort


def started_parser():
    """
    Инициализация парсинга аргументов командной строки
    """
    parser = argparse.ArgumentParser(description="collection of parameters")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--strings", "-s", nargs='+', type=str,
                       help="strings to sort")
    group.add_argument("--digits", "-d", nargs='+', type=int,
                       help="numbers to sort")
    group.add_argument("--random", "-rd", type=int,
                       help="length of random list")
    group.add_argument("--file", "-f", type=str, help="file path")
    parser.add_argument("--reverse", "-rv",  action='store_true',
                        help="sorting mode")
    parser.add_argument('--graph', "-gr", action='store_true',
                        help='show sorting graphic')
    parser.add_argument("--gif", "-g", action='store_true', help="create gif")
    args = parser.parse_args()
    print(args)
    parse_arguments(args)


def create_random_list(length: int) -> list:
    random_list = []
    for i in range(length):
        random_list.append(random.randint(-1000, 1000))
    return random_list


def read_from_file(file_name: str):
    pass


def parse_arguments(args) -> int:
    """
    Получение и проверка аргументов командной строки
    :param args: аргументы командной строки
    :return: 0 - если нет аргументов, 1 - если ошибка, 2 - если корректно
    """
    if args.random:
        if args.random > 0:
            array = create_random_list(args.random)
            print(array)
        else:
            print("Impossible to create an array with negative length")
            return 1
    elif args.file:
        if os.path.exists(args.file):
            array = read_from_file(args.file)
        else:
            print("This filename is incorrect")
            return 1
    elif args.strings:
        array = args.strings
    else:
        array = args.digits
    sorted_array = sort.smooth_sort(array, args.reverse)
    print(sorted_array)
    return 2


if __name__ == "__main__":
    started_parser()
