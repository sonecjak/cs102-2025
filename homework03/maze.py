from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union


import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid: maze grid
    :param coord: coordinates where to remove wall
    :return: updated grid
    """
    x, y = coord
    index_last_col = len(grid[0]) - 1
    direction = choice(("up", "right"))
    if direction == "up":
        if x > 1:
            grid[x - 1][y] = " "
        elif y < index_last_col - 1:
            grid[x][y + 1] = " "
    else:
        if y < index_last_col - 1:
            grid[x][y + 1] = " "
        elif x > 1:
            grid[x - 1][y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows: number of rows
    :param cols: number of columns
    :param random_exit: if True - random entrance/exit, else - fixed
    :return: generated maze
    """
    grid = create_grid(rows, cols)

    for x in range(1, rows - 1, 2):
        for y in range(1, cols - 1, 2):
            grid[x][y] = " "

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))
    for current_cell in empty_cells:
        remove_wall(grid, current_cell)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in] = "X"
    grid[x_out][y_out] = "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid: maze grid
    :return: list of exit coordinates
    """
    exits = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid: maze grid with numeric labels
    :param k: current wave number
    :return: updated grid
    """
    number_rows = len(grid)
    number_cols = len(grid[0])
    next_k = k + 1
    for x in range(number_rows):
        for y in range(number_cols):
            if grid[x][y] == k:
                neighbors = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
                for coord_x, coord_y in neighbors:
                    if 0 <= coord_x < number_rows and 0 <= coord_y < number_cols and grid[coord_x][coord_y] == 0:
                        grid[coord_x][coord_y] = next_k
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    :param grid: maze grid with numeric labels
    :param exit_coord: exit coordinates
    :return: path coordinates from entrance to exit or None
    """
    number_rows = len(grid)
    number_cols = len(grid[0])
    x, y = exit_coord
    k = int(grid[x][y])
    path = [(x, y)]
    while grid[x][y] != 1:
        k -= 1
        if k < 1:
            break
        neighbors = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        for coord_x, coord_y in neighbors:
            if 0 <= coord_x < number_rows and 0 <= coord_y < number_cols and grid[coord_x][coord_y] == k:
                path.append((coord_x, coord_y))
                x, y = coord_x, coord_y
                break
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid: maze grid
    :param coord: exit coordinates
    :return: True if exit is surrounded, False otherwise
    """
    number_rows = len(grid)
    number_cols = len(grid[0])
    x, y = coord
    if x in (0, number_rows - 1) and y in (0, number_cols - 1):
        return True
    if x == 0 and grid[x + 1][y] != " ":
        return True
    if x == number_rows - 1 and grid[x - 1][y] != " ":
        return True
    if y == 0 and grid[x][y + 1] != " ":
        return True
    if y == number_cols - 1 and grid[x][y - 1] != " ":
        return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    :param grid: maze grid
    :return: tuple of (grid with numeric labels, path or None)
    """
    grid = deepcopy(grid)
    exits = get_exits(grid)
    if len(exits) == 1:
        return grid, exits[0]
    for possible_exit in exits:
        if encircled_exit(grid, possible_exit):
            return grid, None
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == " ":
                grid[x][y] = 0
    x_enter, y_enter = exits[0]
    grid[x_enter][y_enter] = 1
    x_exit, y_exit = exits[1]
    grid[x_exit][y_exit] = 0
    k = 1
    while grid[x_exit][y_exit] == 0:
        make_step(grid, k)
        k += 1
        if k > len(grid) * len(grid[0]):
            return grid, None
    path = shortest_path(grid, (x_exit, y_exit))
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """
    :param grid: maze grid
    :param path: path coordinates
    :return: grid with path marked
    """
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))