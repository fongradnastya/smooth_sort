import os
import pygame as pg
from PIL import Image


class SortVisualize:
    """
    Класс для визуализации сортировки
    """
    class GifCreator:
        """
        Класс для хранения информации о создаваемой гифке
        """
        def __init__(self, directory="gif"):
            """
            Инициализация новой гифки
            @param directory: директория для сохранения гифки
            """
            self.directory = ""
            self.frames = []
            self.frames_cnt = 0
            self.gif_number = 1
            self.path = self._create_path(directory)

        def _create_path(self, directory):
            """
            Создание относительного пути до гифки
            @param directory: директория, в которую планируется сохранение
            @return: относительный путь до гифки
            """
            if os.path.exists(directory):
                self.directory = directory
            path = f"{self.directory}\\gif{self.gif_number}.gif"
            while os.path.exists(path):
                self.gif_number += 1
                path = f"{self.directory}\\gif{self.gif_number}.gif"
            return path

    def __init__(self, min_value, max_value, length, gif=False):
        """
        Инициализация визуализатора сортировки
        @param min_value: минимальное значение сортируемого массива
        @param max_value: максимальное значение сортируемого массива
        @param length: длина сортируемого массива
        @param gif: нужно ли сохранить визуализацию в гифке
        """
        pg.init()
        self._width, self._height = 800, 600
        self._min_value = int(min_value)
        self._max_value = max_value
        self._gif = None
        if gif:
            self._gif = self.GifCreator()
        self._length = length
        self.screen = pg.display.set_mode((self._width, self._height))
        pg.display.set_caption("MergeSort visualize")
        self.bg_color = (255, 200, 200)
        self.screen.fill(self.bg_color)

    def draw_array(self, array: list, red: int):
        """
        Отрисовка нового состояния массива
        @param array: массив
        @param red: текущее положение изменяемого элемента
        """
        norm_x = self._width / self._length
        norm_w = norm_x if norm_x > 1 else 1
        if self._max_value != self._min_value:
            h_caf = (self._height - 200) / (self._max_value - self._min_value)
        else:
            h_caf = self._height - 100
        for index, value in enumerate(array):
            norm_h = abs(value) * h_caf
            zero_h = self._count_zero_height(h_caf)
            if value > 0:
                norm_y = self._height - norm_h - (self._height - zero_h)
            else:
                norm_y = zero_h
            if index != red:
                if index % 2:
                    cur_color = (140, 140, 200)
                else:
                    cur_color = (160, 160, 220)
            else:
                cur_color = (255, 0, 0)
            pg.draw.rect(self.screen, self.bg_color, (
                norm_x * index, 0, norm_w, self._height))
            sqrt_h = norm_w if norm_w < 80 else 80
            sqrt_y = norm_y - sqrt_h if value > 0 else norm_y + norm_h
            pg.draw.rect(self.screen, (255, 255, 255),
                         (norm_x * index, sqrt_y, norm_w, sqrt_h))
            pg.draw.rect(self.screen, cur_color, (norm_x * index, norm_y,
                                                  norm_w, norm_h))
            pg.draw.line(self.screen, (255, 255, 255),
                         (0, zero_h), (self._width, zero_h), 2)
            pg.display.update()
        if self._gif:
            self._add_frame(pg.image.tostring(self.screen, "RGBA"))
        pg.time.wait(50)

    def _count_zero_height(self, h_caf):
        """
        Вычисление числа пикселей, которому соответствует нулевое значение
        графика
        @return: высота в пикселях
        """
        norm_min = self._min_value * h_caf
        zero_h = self._height - 1 + norm_min - 50
        return zero_h

    def _add_frame(self, data):
        """
        Добавляет новый кадр в гифку
        @param data: строковое представление сохраняемого изображения
        """
        image = Image.frombytes("RGBA", (self._width, self._height), data)
        self._gif.frames_cnt += 1
        self._gif.frames.append(image)

    def create_gif(self):
        """
        Создание гифки и сохранение её в директории
        """
        print("Please, wait, started gif creation")
        self._gif.frames[0].save(self._gif.path, save_all=True,
                                 append_images=self._gif.frames[1:],
                                 optimize=True,
                                 duration=100,
                                 loop=0)
        print(f"Gif was successfully saved "
              f"in '{self._gif.directory}' directory")
        self._gif.frames[0].close()
        self._gif.frames.clear()
        self._gif.frames_count = 0
        self._gif.gif_number += 1
