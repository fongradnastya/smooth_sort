import random
from typing import Optional, Callable
from app import *


def count_leonardo_numb(numb):
    """Функция для вычисления числа Леонардо"""
    if numb < 2:
        return 1
    return count_leonardo_numb(numb - 1) + count_leonardo_numb(numb - 2) + 1


def smooth_sort(array: list, reverse: bool = False,
                key: Optional[Callable] = None,
                cmp: Optional[Callable] = None) -> list:
    """
    Реализация алгоритма плавной сортировки
    @param array: список значений для сортировки
    @param reverse: требуется ли отсортировать по возрастанию или убыванию
    @param key: функция вычисления порядка сортировки для элемента
    @param cmp: функция сравнения двух элементов списка
    @return:
    """
    key = key if key is not None else lambda x: x
    cmp = cmp if cmp is not None else lambda x, y: x < y
    size_list = []
    application = Application()

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
            idx, size_idx = fix_roots(arr, size_list, heap_end,
                                      len(size_list) - 1)
            sift_down(arr, idx, size_list[size_idx])

    def sift_down(heap: list, root_idx: int, tree_size: int):
        """Просеивание кучи"""
        cur = root_idx
        while tree_size > 1:
            right = cur - 1
            left = cur - 1 - count_leonardo_numb(tree_size - 2)
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
            next_i = cur - count_leonardo_numb(sizes[size_cur])
            if cmp(key(heap[next_i]), key(heap[cur])) != reverse:
                break
            if sizes[size_cur] > 1:
                right = cur - 1
                left = right - count_leonardo_numb(sizes[size_cur] - 2)
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
        print(array)
        application.draw_array_col(array, 100, 100, heap_size)
        removed_size = size_list.pop()
        if removed_size > 1:
            size_list.append(removed_size - 1)
            size_list.append(removed_size - 2)
            left_idx = heap_size - count_leonardo_numb(size_list[-1]) - 1
            right_idx = heap_size - 1
            left_size_idx = len(size_list) - 2
            right_size_idx = len(size_list) - 1
            idx, size_idx = fix_roots(array, size_list, left_idx,
                                      left_size_idx)
            sift_down(array, idx, size_list[size_idx])
            idx, size_idx = fix_roots(array, size_list, right_idx,
                                      right_size_idx)
            sift_down(array, idx, size_list[size_idx])
    return array


if __name__ == "__main__":
    data = []
    for i in range(0, 100):
        data.append(random.randint(1, 100))
    sorted_arr = smooth_sort(data)
    print(sorted_arr)
