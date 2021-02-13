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
        self.n_generation = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid_matrix = []
        if randomize:
            for i in range(self.rows):
                append_list = []
                for j in range(self.cols):
                    append_list.append(random.randint(0, 1))
                grid_matrix.append(append_list)
        else:
            grid_matrix = [[0] * self.cols for j in range(self.rows)]
        return grid_matrix


    def get_neighbours(self, cell: Cell) -> Cells:
        neighbors = []
        relatives_util = [[-1, -1], [1, 1], [0, 1], [1, 0], [-1, 1], [1, -1], [-1, 0], [0, -1]]
        for el in relatives_util:
            el[0] += cell[0]
            el[1] += cell[1]
        for el in relatives_util:
            i, j = el
            try:
                if i >= 0 and j >= 0:
                    neighbors.append(self.curr_generation[i][j])
            except IndexError:
                pass
        return neighbors

    def get_next_generation(self) -> Grid:
        new_greed = self.create_grid(False)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.curr_generation[i][j]:
                    if sum(self.get_neighbours((i, j))) in [2, 3]:
                        new_greed[i][j] = 1
                elif sum(self.get_neighbours((i, j))) == 3:
                    new_greed[i][j] = 1
        return new_greed

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.n_generation += 1

    @property
    def is_max_generations_exceed(self) -> bool:
        if self.n_generation > self.max_generations:
            return False
        else:
            return True

    @property
    def is_changing(self) -> bool:
        if self.prev_generation == self.curr_generation:
            return False
        else:
            return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        restored_grid = []
        with open(filename) as f:
            for line in f:
                restored_grid.append([int(el) for el in list(line.replace('\n', ''))])
        new_game = GameOfLife((len(restored_grid),len(restored_grid[0])))
        new_game.curr_generation = restored_grid
        return new_game

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, 'w') as f:
            for row in self.curr_generation:
                f.writelines(''.join(str(e) for e in row) + "\n")
