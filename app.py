import time

import pygame as pg


class Application:

    def __init__(self, max_value, length, gif=None):
        """
        Инициализация графического приложения
        """
        pg.init()
        self._width, self._height = 800, 600
        self._max_value = max_value
        self._length = length
        self.screen = pg.display.set_mode((self._width, self._height))
        pg.display.set_caption("MergeSort visualize")

    @property
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, max_value):
        self._max_value = max_value

    def draw_array_col(self, array: list, red: int):
        """
        Отрисовка нового состояния массива
        @param array: массив
        @param red: текущее положение изменяемого элемента
        """
        norm_x = self._width / self._length
        norm_w = norm_x if norm_x > 1 else 1
        self.screen.fill((0, 0, 0))
        h_caf = (self._height - 100) / self.max_value

        for index, value in enumerate(array):
            norm_h = value * h_caf
            norm_y = self._height - norm_h
            if index != red:
                cur_color = (100, 100, 100)
            else:
                cur_color = (255, 0, 0)
            pg.draw.rect(self.screen, cur_color, (norm_x * index, norm_y,
                                                  norm_w, norm_h))
            pg.display.update()
        time.sleep(0.1)
