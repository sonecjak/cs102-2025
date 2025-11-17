import pathlib
import typing as tp
import random

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "")
                for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    result = []
    for i in range(0, len(values), n):
        result.append(values[i : i + n])
    return result


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    result = []
    for i in range(len(grid)):
        result.append(grid[i][pos[1]])
    return result


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    n = len(grid)
    block_size = int(n**0.5)

    block_row = (row // block_size) * block_size
    block_col = (col // block_size) * block_size

    result = []
    for i in range(block_row, block_row + block_size):
        for j in range(block_col, block_col + block_size):
            result.append(grid[i][j])
    return result


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ".":
                return (i, j)
    return None


def find_possible_values(
    grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    n = len(grid)
    all_values = set(str(i) for i in range(1, n + 1))
    used_values = set()
    used_values.update(get_row(grid, pos))
    used_values.update(get_col(grid, pos))
    used_values.update(get_block(grid, pos))
    used_values.discard(".")
    return all_values - used_values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    empty_pos = find_empty_positions(grid)

    if not empty_pos:
        return grid

    row, col = empty_pos

    possible_values = find_possible_values(grid, (row, col))

    for value in possible_values:
        grid[row][col] = value

        if solve(grid):
            return grid

        grid[row][col] = "."

    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    # TODO: Add doctests with bad puzzles
    n = len(solution)
    expected_numbers = set(str(i) for i in range(1, n + 1))

    for row in range(n):
        row_values = get_row(solution, (row, 0))
        if set(row_values) != expected_numbers:
            return False

    for col in range(n):
        col_values = get_col(solution, (0, col))
        if set(col_values) != expected_numbers:
            return False

    block_size = 3
    for start_row in range(0, n, block_size):  # 0, 3, 6
        for start_col in range(0, n, block_size):  # 0, 3, 6
            block_values = get_block(solution, (start_row, start_col))
            if set(block_values) != expected_numbers:
                return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """

    size = 9
    total_cells = size * size

    N = max(0, min(N, total_cells))

    full_solution = [
        ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
        ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
        ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
        ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
        ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
        ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
        ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
        ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
        ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ]

    if N == total_cells:
        result = []
        for row in full_solution:
            result.append(row.copy())
        return result

    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(".")
        grid.append(row)

    if N == 0:
        return grid

    positions = []
    for i in range(size):
        for j in range(size):
            positions.append((i, j))

    random.shuffle(positions)

    for i in range(N):
        row, col = positions[i]
        grid[row][col] = full_solution[row][col]

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
