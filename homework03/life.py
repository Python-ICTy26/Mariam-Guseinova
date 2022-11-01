import pathlib
import random
import typing as tp

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
        if randomize:
            grid = [[random.choice([0, 1]) for col in range(self.cols)] for row in range(self.rows)]
        else:
            grid = [[0 for col in range(self.cols)] for row in range(self.rows)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        cells_list = []
        row, col = cell
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (
                    ((y != x) or (x + y != 0))
                    and (0 <= row + x < self.rows)
                    and (0 <= col + y < self.cols)
                ):
                    cells_list += [self.curr_generation[row + x][col + y]]
        return cells_list

    def get_next_generation(self) -> Grid:
        new_generation = self.create_grid()
        for col in range(self.cols):
            for row in range(self.rows):
                if sum(self.get_neighbours((row, col))) == 3:
                    new_generation[row][col] = 1
                elif (
                    sum(self.get_neighbours((row, col))) == 2
                    and self.curr_generation[row][col] == 1
                ):
                    new_generation[row][col] = 1
                else:
                    new_generation[row][col] = 0
        return new_generation

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

        gof = GameOfLife((number_of_rows, number_of_columns))
        gof.curr_generation = grid_from_file
        return gof

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
