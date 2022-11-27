import pygame as pg


class Application:

    def __init__(self):
        pg.init()
        self.width, self.height = 800, 600
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("MergeSort visualize")

    def draw_array_col(self, array: list, max_el: int, length: int, red: int):
        """
        Отрисовка нового состояния массива
        @param array: массив
        @param max_el: максимальный элемент массива
        @param length: длина массива
        @param red: текущее положение изменяемого элемента
        """
        norm_x = self.width / length
        norm_w = norm_x if norm_x > 1 else 1
        if red == 0:
            self.screen.fill((0, 0, 0))
        else:
            self.screen.fill((0, 0, 0), rect=(0, 0, (red + 1) * norm_x,
                                              self.height))
        h_caf = (self.height - 100) / max_el

        for index, value in enumerate(array):
            norm_h = value * h_caf
            norm_y = self.height - norm_h
            if index != red or value == max_el:
                cur_color = (0, 0, 0)
            else:
                cur_color = (255, 0, 0)
            if red != 0 and index == red + 1:
                break
            pg.draw.rect(self.screen, cur_color, (norm_x * index, norm_y,
                                                  norm_w, norm_h))

