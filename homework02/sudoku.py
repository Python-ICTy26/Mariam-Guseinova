import pathlib
import typing as tp
from random import randint

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    matrix = []
    for i in range(len(values) // n):
        stroka = []
        stroka += values[i * n : n * (i + 1)]
        matrix.append(stroka)
    return matrix


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    number = pos[1]
    col = []
    for i in range(len(grid)):
        col.append(grid[i][number])
    return col


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    row, col = pos[0] - (pos[0] % 3), pos[1] - (pos[1] % 3)
    square = []
    for j in range(row, row + 3):
        for i in range(col, col + 3):
            square.append(grid[j][i])
    return square


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    for i in range(len(grid)):
        if "." in grid[i]:
            position = (i, grid[i].index("."))
            return position
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    block = get_block(grid, pos)
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    variants = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
    our = set(block + row + col)
    result = variants - our
    return result


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    empty_position = find_empty_positions(grid)
    if not empty_position:
        return grid
    else:
        possible_values = find_possible_values(grid, empty_position)
    for answer in possible_values:
        grid[empty_position[0]][empty_position[1]] = answer
        solution = solve(grid)
        if solution:
            return solution
    grid[empty_position[0]][empty_position[1]] = "."
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    for i in range(9):
        num = solution[i][i]
        if (
            get_row(solution, (i, i)).count(num)
            == get_col(solution, (i, i)).count(num)
            == get_block(solution, (i, i)).count(num)
            == 1
        ):
            if (
                "." not in get_row(solution, (i, i))
                and "." not in get_col(solution, (i, i))
                and "." not in get_block(solution, (i, i))
            ):
                continue
            else:
                return False
        else:
            return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    grid = [["." for i in range(9)] for j in range(9)]
    grid = solve(grid)
    if N > 81:
        N = 81
    propuski = 81 - N
    for k in range(propuski):
        row = randint(0, 8)
        col = randint(0, 8)
        while grid[row][col] == ".":
            row = randint(0, 8)
            col = randint(0, 8)
        grid[row][col] = "."
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
