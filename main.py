import argparse
import random
from app import *
from sort import sort


def pars_arguments():
    """
    Парсинг аргументов командной строки
    @return: считанные аргументы командной строки
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
    parser.add_argument("--reverse", "-rv", action='store_true',
                        help="sorting mode")
    parser.add_argument('--graph', "-gr", action='store_true',
                        help='show sorting graphic')
    parser.add_argument("--gif", "-g", action='store_true', help="create gif")
    args = parser.parse_args()
    return args


def create_random_list(length: int) -> list:
    """
    Создание списка случайных значений
    @param length: требуемая длина списка
    @return: созданный список
    """
    random_list = []
    for i in range(length):
        random_list.append(random.randint(-1000, 1000))
    return random_list


def read_from_file(file_name: str) -> list:
    """
    Считывание числовой последовательности из файла
    @param file_name: имя файла для чтения
    @return: считанная последовательность чисел
    """
    data = []
    with open(file_name) as file:
        try:
            data = list(map(int, file.read().replace("\n", "").split(", ")))
        except ValueError:
            print("Impossible to read data from the file. "
                  "Please, enter only comma separated integers values.")
    return data


def main() -> int:
    """
    Точка входа в программу
    @return: 0 - сортировка прошла корректно, 1 - код завершился с ошибкой
    """
    args = pars_arguments()
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
            if not array:
                return 1
        else:
            print("This filename is incorrect")
            return 1
    elif args.strings:
        array = args.strings
        if args.graph or args.gif:
            print("Please, enter integer values to see a diagram")
            print("Impossible to visualize string list")
            return 1
    else:
        array = args.digits
    if not args.graph and args.gif:
        args.graph = True
    print("Initial array: ", end="")
    print(array)
    if args.graph:
        visualize = SortVisualize(min(array), max(array), len(array), args.gif)
        sorted_array = sort(array, args.reverse, visualize=visualize,
                            gif=args.gif)
    else:
        sorted_array = sort(array, args.reverse)
    print("Sorted array: ", end="")
    print(sorted_array)
    if args.file:
        with open("output.txt", 'w') as file:
            file.write("Sorted: " + str(sorted_array))
    return 0


if __name__ == "__main__":
    main()
