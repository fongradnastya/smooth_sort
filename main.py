import argparse
import random
from app import *


def pars_arguments():
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
    parser.add_argument("--reverse", "-rv", action='store_true',
                        help="sorting mode")
    parser.add_argument('--graph', "-gr", action='store_true',
                        help='show sorting graphic')
    parser.add_argument("--gif", "-g", action='store_true', help="create gif")
    args = parser.parse_args()
    return args


def graphic_sort(array: list, reverse: bool, graphic=False, gif: bool = False):
    size_list = []
    if graphic:
        application = Application(min(array), max(array), len(array), gif)
    else:
        application = None
    if not array:
        return None
    key = lambda x: x
    cmp = lambda x, y: x < y

    def cnt_leo_numb(num):
        """Функция для вычисления числа Леонардо"""
        return 1 if num < 2 else cnt_leo_numb(num - 1) + cnt_leo_numb(
            num - 2) + 1

    def create_heap(arr: list) -> None:
        """Создание сортировочной кучи"""
        for heap_end in range(len(arr)):
            if not size_list:
                size_list.append(1)
            elif len(size_list) > 1 and size_list[-2] == size_list[-1] + 1:
                size_list[-2] = size_list[-2] + 1
                del size_list[-1]
            else:
                if size_list[-1] == 1:
                    size_list.append(0)
                else:
                    size_list.append(1)
            ida, size = fix_roots(arr, size_list, heap_end, len(size_list) - 1)
            sift_down(arr, ida, size_list[size])

    def sift_down(heap: list, root_idx: int, tree_size: int):
        """Просеивание кучи"""
        cur = root_idx
        while tree_size > 1:
            right = cur - 1
            left = cur - 1 - cnt_leo_numb(tree_size - 2)
            if application:
                application.draw_array(array, cur)
            if cmp(key(heap[left]), key(heap[cur])) != reverse and \
                    cmp(key(heap[right]), key(heap[cur])) != reverse:
                break
            elif cmp(key(heap[left]), key(heap[right])) != reverse:
                heap[cur], heap[right] = heap[right], heap[cur]

                cur = right
                tree_size = tree_size - 2
            else:
                heap[cur], heap[left] = heap[left], heap[cur]

                cur = left
                tree_size = tree_size - 1

    def fix_roots(heap: list, sizes: list, start_heap_idx: int,
                  start_size_idx: int):
        """Добавление нового элемента"""
        cur = start_heap_idx
        size_cur = start_size_idx
        while size_cur > 0:
            next_i = cur - cnt_leo_numb(sizes[size_cur])
            if cmp(key(heap[next_i]), key(heap[cur])) != reverse:
                break
            if sizes[size_cur] > 1:
                right = cur - 1
                left = right - cnt_leo_numb(sizes[size_cur] - 2)
                if cmp(key(heap[next_i]), key(heap[right])) != reverse or \
                        cmp(key(heap[next_i]), key(heap[left])) != reverse:
                    break
            temp = heap[cur]
            heap[cur] = heap[next_i]
            heap[next_i] = temp
            size_cur = size_cur - 1
            cur = next_i
        return cur, size_cur

    create_heap(array)
    for heap_size in range(len(array) - 1, -1, -1):
        if application:
            application.draw_array(array, heap_size)
        removed_size = size_list.pop()
        if removed_size > 1:
            size_list.append(removed_size - 1)
            size_list.append(removed_size - 2)
            left_idx = heap_size - cnt_leo_numb(size_list[-1]) - 1
            right_idx = heap_size - 1
            left_size_idx = len(size_list) - 2
            right_size_idx = len(size_list) - 1
            idx, size_idx = fix_roots(array, size_list, left_idx,
                                      left_size_idx)
            sift_down(array, idx, size_list[size_idx])
            idx, size_idx = fix_roots(array, size_list, right_idx,
                                      right_size_idx)
            sift_down(array, idx, size_list[size_idx])
    if gif:
        application.create_gif()
    return array


def create_random_list(length: int) -> list:
    random_list = []
    for i in range(length):
        random_list.append(random.randint(-1000, 1000))
    return random_list


def read_from_file(file_name: str):
    data = []
    with open(file_name) as file:
        try:
            data = list(map(int, file.read().replace("\n", "").split(", ")))
        except ValueError:
            print("Impossible to read data from the file. "
                  "Please, enter only comma separated integers values.")
    return data


def write_to_file(file_name: str, sorted_array: list):
    with open(file_name, 'a') as file:
        file.write("\nSorted: " + str(sorted_array))


def main() -> int:
    """
    Получение и проверка аргументов командной строки
    @return: 0 - если нет аргументов, 1 - если ошибка, 2 - если корректно
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
    else:
        array = args.digits
    if not args.graph and args.gif:
        args.graph = True
    sorted_array = graphic_sort(array, args.reverse, args.graph, args.gif)
    print(sorted_array)
    if args.file:
        write_to_file(args.file, sorted_array)
    return 0


if __name__ == "__main__":
    main()
