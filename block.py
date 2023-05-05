import pygame


class Cell:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = (255, 255, 255)
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == (255, 0, 0)

    def is_open(self):
        return self.color == (135, 206, 235)

    def is_wall(self):
        return self.color == (0, 0, 0)

    def is_start(self):
        return self.color == (255, 165, 0)

    def is_end(self):
        return self.color == (0, 255, 0)

    def reset(self):
        self.color = (255, 255, 255)

    def make_closed(self):
        self.color = (255, 0, 0)

    def make_open(self):
        self.color = (135, 206, 235)

    def make_wall(self):
        self.color = (0, 0, 0)

    def make_start(self):
        self.color = (255, 165, 0)

    def make_end(self):
        self.color = (0, 255, 0)

    def make_path(self):
        self.color = (255, 255, 0)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i, j, gap, rows)
            grid[i].append(cell)

    return grid
