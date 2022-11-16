import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for i in range(self.cell_height):
            string = []
            if randomize:
                for f in range(self.cell_width):
                    string.append(random.randint(0, 1))
            else:
                for f in range(self.cell_width):
                    string.append(0)
            grid.append(string)
        return grid

    def draw_grid(self) -> None:
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                if self.grid[row][col] == 1:
                    color = "green"
                else:
                    color = "white"
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(color),
                    (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size),
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        for x, y in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            if 0 <= cell[0] + x < self.cell_height and 0 <= cell[1] + y < self.cell_width:
                neighbours.append(self.grid[cell[0] + x][cell[1] + y])
        return neighbours

    def get_next_generation(self) -> Grid:
        next_generation = []
        for x in range(self.cell_height):
            list_ = []
            for y in range(self.cell_width):
                neighbours = self.get_neighbours((x, y))
                if self.grid[x][y] == 1:
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
