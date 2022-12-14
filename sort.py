from typing import Optional, Callable


def sort(array: list, reverse: bool = False, key: Optional[Callable] = None,
         cmp: Optional[Callable] = None, visualize=None,
         gif: Optional[bool] = False):
    """
    Реализация алгоритма плавной сортировки
    @param array: список значений для сортировки
    @param reverse: требуется ли отсортировать по возрастанию или убыванию
    @param key: функция вычисления порядка сортировки для элемента
    @param cmp: функция сравнения двух элементов списка
    @param visualize: объект класса SortVisualize
    @param gif: нужно ли сохранить результат работы в качестве гифки
    @return: отсортированный список
    """
    size_list = []
    if not array:
        array = []
    key = key if key is not None else lambda x: x
    cmp = cmp if cmp is not None else lambda x, y: x < y

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
            if visualize:
                visualize.draw_array(array, cur)
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
        """Изменение списка сортировочных куч"""
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
        if visualize:
            visualize.draw_array(array, heap_size)
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
    if visualize and gif:
        visualize.create_gif()
    return array
