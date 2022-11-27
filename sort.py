import random
from typing import Optional, Callable
from app import *


def count_leonardo_numb(k):
    if k < 2:
        return 1
    return count_leonardo_numb(k - 1) + count_leonardo_numb(k - 2) + 1


def smooth_sort(array):
    def create_heap(arr: list) -> list:
        size_list = []
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
            idx, size_idx = _fix_roots(arr, size_list,
                                       heap_end, len(size_list) - 1)
            _sift_down(arr, idx, size_list[size_idx])
        print(size_list)
        return size_list

    size_list = create_heap(array)
    for heap_size in range(len(array) - 1, -1, -1):
        print(array)
        removed_size = size_list.pop()
        if removed_size > 1:
            size_list.append(removed_size - 1)
            size_list.append(removed_size - 2)
            left_idx = heap_size - count_leonardo_numb(size_list[-1]) - 1
            right_idx = heap_size - 1
            left_size_idx = len(size_list) - 2
            right_size_idx = len(size_list) - 1
            idx, size_idx = _fix_roots(array, size_list, left_idx,
                                       left_size_idx)
            _sift_down(array, idx, size_list[size_idx])
            idx, size_idx = _fix_roots(array, size_list, right_idx,
                                       right_size_idx)
            _sift_down(array, idx, size_list[size_idx])
    return array


def _fix_roots(heap, sizes, start_heap_idx, start_size_idx):
    """Добавление нового элемента"""
    cur = start_heap_idx
    size_cur = start_size_idx
    while size_cur > 0:
        next_i = cur - count_leonardo_numb(sizes[size_cur])
        if heap[next_i] <= heap[cur]:
            break
        if sizes[size_cur] > 1:
            right = cur - 1
            left = right - count_leonardo_numb(sizes[size_cur] - 2)
            if heap[next_i] <= heap[right] or heap[next_i] <= heap[left]:
                break
        temp = heap[cur]
        heap[cur] = heap[next_i]
        heap[next_i] = temp
        size_cur = size_cur - 1
        cur = next_i
    return cur, size_cur


def _sift_down(heap: list, root_idx: int, tree_size: int,
               key: Optional[Callable] = None, cmp: Optional[Callable] = None):
    """Просеивание"""
    key = key if key is not None else lambda x: x
    cmp = cmp if cmp is not None else lambda x, y: x > y
    cur = root_idx
    while tree_size > 1:
        right = cur - 1
        left = cur - 1 - count_leonardo_numb(tree_size - 2)
        if cmp(key(heap[cur]), key(heap[left])) and \
                cmp(key(heap[cur]), key(heap[right])):
            break
        elif cmp(key(heap[right]), key(heap[left])):
            heap[cur], heap[right] = heap[right], heap[cur]
            cur = right
            tree_size = tree_size - 2
        else:
            heap[cur], heap[left] = heap[left], heap[cur]
            cur = left
            tree_size = tree_size - 1


if __name__ == "__main__":
    data = []
    for i in range(0, 100):
        data.append(random.randint(1, 100))
    application = Application()
    sorted_arr = smooth_sort(data)
    print(sorted_arr)
