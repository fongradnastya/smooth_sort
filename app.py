import time
import os
import pygame as pg
from PIL import Image


class Application:

    class GifCreator:
        def __init__(self, directory="gif"):
            self.directory = ""
            self.frames = []
            self.frames_cnt = 0
            self.gif_number = 1
            self.path = self.create_path(directory)

        def create_path(self, directory):
            if os.path.exists(directory):
                self.directory = directory
            path = f"{self.directory}\\gif{self.gif_number}.gif"
            while os.path.exists(path):
                self.gif_number += 1
                path = f"{self.directory}\\gif{self.gif_number}.gif"
            return path


    def __init__(self, max_value, length, gif=False):
        """
        Инициализация графического приложения
        """
        pg.init()
        self._width, self._height = 800, 600
        self._max_value = max_value
        if gif:
            self._gif = self.GifCreator()
        else:
            self._gif = None
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
            if self._gif:
                self._add_frame(pg.image.tostring(self.screen, "RGBA"))

    def _add_frame(self, data):
        image = Image.frombytes("RGBA", (self._width, self._height), data)
        self._gif.frames_cnt += 1
        self._gif.frames.append(image)

    def create_gif(self):
        """
        Метод сохранения гифки в директорию
        """
        self._gif.frames[0].save(self._gif.path, save_all=True,
                                 append_images=self._gif.frames[1:],
                                 optimize=True,
                                 duration=20,
                                 loop=1)
        print(f"Gif was saved in {self._gif.directory} directory")
        self._gif.frames[0].close()
        self._gif.frames.clear()
        self._gif.frames_count = 0
        self._gif.gif_number += 1
