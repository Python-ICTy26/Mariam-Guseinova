import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for i in range(self.rows):
            string = []
            if randomize:
                for f in range(self.cols):
                    string.append(random.randint(0, 1))
            else:
                for f in range(self.cols):
                    string.append(0)
            grid.append(string)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        for x, y in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            if 0 <= cell[0] + x < self.rows and 0 <= cell[1] + y < self.cols:
                neighbours.append(self.curr_generation[cell[0] + x][cell[1] + y])
        return neighbours

    def get_next_generation(self) -> Grid:
        next_generation = []
        for x in range(self.rows):
            list_ = []
            for y in range(self.cols):
                neighbours = self.get_neighbours((x, y))
                if self.curr_generation[x][y] == 1:
                    if sum(neighbours) < 2 or sum(neighbours) > 3:
                        list_.append(0)
                    else:
                        list_.append(1)
                else:
                    if sum(neighbours) == 3:
                        list_.append(1)
                    else:
                        list_.append(0)
            next_generation.append(list_)
        return next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            return bool(self.generations >= self.max_generations)
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return bool(self.curr_generation != self.prev_generation)

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        number_of_rows = 0
        grid_from_file = []
        with open(filename) as file:
            for row in file:
                if row != "\n":
                    grid_from_file += [[int(element) for element in row if element in "01"]]
                    number_of_rows += 1
        number_of_columns = len(grid_from_file[0])

        game = GameOfLife((number_of_rows, number_of_columns))
        game.curr_generation = grid_from_file
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        list_of_values = []
        for row in self.curr_generation:
            for col in row:
                list_of_values += [str(col)]
            list_of_values += "\n"
        with open(filename, "w") as file:
            file.write("".join(list_of_values))
