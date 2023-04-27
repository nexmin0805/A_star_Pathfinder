import pygame
import math
from queue import PriorityQueue
import random
import argparse


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


def h(p1, p2, heuristic):
    x1, y1 = p1
    x2, y2 = p2
    if heuristic == 'manhattan':
        return abs(x1 - x2) + abs(y1 - y2)
    elif heuristic == "euclidean":
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def a_star(draw, grid, start, end, heuristic_func):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = h(start.get_pos(), end.get_pos(), heuristic_func)

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos(), heuristic_func)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

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


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, (128, 128, 128), (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, (128, 128, 128), (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width, manhattan_checked, euclidean_checked):
    win.fill((255, 255, 255))

    for row in grid:
        for cell in row:
            cell.draw(win)

    draw_grid(win, rows, width)
    draw_buttons(win, width, manhattan_checked, euclidean_checked)
    pygame.display.update()

    draw_grid(win, rows, width)
    draw_buttons(win, width, manhattan_checked, euclidean_checked)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def draw_buttons(win, width, manhattan_checked, euclidean_checked):
    start_button = pygame.Rect(10, width + 25, 190, 50)
    pygame.draw.rect(win, (135, 206, 235), start_button)
    win.blit(pygame.font.Font(None, 28).render("Start A* Search", True, (0, 0, 0)), (30, width + 39))

    random_walls_button = pygame.Rect(240, width + 25, 170, 50)
    pygame.draw.rect(win, (135, 206, 235), random_walls_button)
    win.blit(pygame.font.Font(None, 28).render("Random Walls", True, (0, 0, 0)), (260, width + 39))

    reset_button = pygame.Rect(450, width + 25, 150, 50)
    pygame.draw.rect(win, (135, 206, 235), reset_button)
    win.blit(pygame.font.Font(None, 28).render("Reset", True, (0, 0, 0)), (500, width + 39))

    manhattan_button = pygame.Rect(650, 80, 120, 30)
    pygame.draw.rect(win, (255, 255, 0), manhattan_button)
    win.blit(pygame.font.Font(None, 28).render("Manhattan", True, (0, 0, 0)), (660, 85))

    euclidean_button = pygame.Rect(650, 150, 120, 30)
    pygame.draw.rect(win, (255, 255, 0), euclidean_button)
    win.blit(pygame.font.Font(None, 28).render("Euclidean", True, (0, 0, 0)), (660, 155))

    win.blit(pygame.font.Font(None, 40).render("Hueristic", True, (0, 0, 0)), (640, 30))

    manhattan_checkbox = pygame.Rect(625, 85, 15, 15)
    pygame.draw.rect(win, (0, 0, 0) if manhattan_checked else (255, 255, 255), manhattan_checkbox)
    pygame.draw.rect(win, (0, 0, 0), manhattan_checkbox, 1)  # Add a border with width 1
    if manhattan_checked:
        pygame.draw.rect(win, (0, 0, 0), (626, 86, 13, 13))

    euclidean_checkbox = pygame.Rect(625, 155, 15, 15)
    pygame.draw.rect(win, (0, 0, 0) if euclidean_checked else (255, 255, 255), euclidean_checkbox)
    pygame.draw.rect(win, (0, 0, 0), euclidean_checkbox, 1)  # Add a border with width 1
    if euclidean_checked:
        pygame.draw.rect(win, (0, 0, 0), (626, 156, 13, 13))


def handle_buttons(pos, width):
    x, y = pos
    if 10 <= x <= 200 and width + 10 <= y <= width + 60:
        return "start"
    elif 240 <= x <= 410 and width + 10 <= y <= width + 60:
        return "random_walls"
    elif 450 <= x <= 600 and width + 10 <= y <= width + 60:
        return "reset"
    elif (650 <= x <= 770 and 80 <= y <= 110) or (625 <= x <= 640 and 85 <= y <= 100):
        return "manhattan"
    elif (650 <= x <= 770 and 150 <= y <= 180) or (625 <= x <= 640 and 155 <= y <= 170):
        return "euclidean"
    return None


def main(win, width, rows, inc_obstacle_ratio):
    grid = make_grid(rows, width)
    heuristic = "manhattan"

    START_ROW, START_COL = 2, math.ceil(rows / 2)
    END_ROW, END_COL = rows - 3, math.ceil(rows / 2)

    start = grid[START_ROW][START_COL]
    end = grid[END_ROW][END_COL]

    start.make_start()
    end.make_end()

    run = True
    started = False

    manhattan_checked = True
    euclidean_checked = False

    dragging_start = False  # Initialize dragging_start
    dragging_end = False  # Initialize dragging_end

    while run:
        draw(win, grid, rows, width, manhattan_checked, euclidean_checked)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                if 0 <= row < rows and 0 <= col < rows:
                    cell = grid[row][col]
                else:
                    cell = None

                if cell:
                    if cell == start:
                        dragging_start = True
                    elif cell == end:
                        dragging_end = True
                    elif not cell.is_wall():
                        cell.make_wall()

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_start = False
                dragging_end = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging_start or dragging_end:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, rows, width)
                    if 0 <= row < rows and 0 <= col < rows:
                        new_cell = grid[row][col]
                        if new_cell != start and new_cell != end and not new_cell.is_wall():
                            if dragging_start:
                                start.reset()
                                start = new_cell
                                start.make_start()
                            elif dragging_end:
                                end.reset()
                                end = new_cell
                                end.make_end()
                else:
                    if pygame.mouse.get_pressed()[0]:  # Left Mouse Button
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, rows, width)
                        if 0 <= row < rows and 0 <= col < rows:
                            cell = grid[row][col]
                            if cell != start and cell != end and not cell.is_wall():  # Add condition to exclude start and end points
                                cell.make_wall()

            if pygame.mouse.get_pressed()[0]:  # Left Mouse Button
                pos = pygame.mouse.get_pos()
                button_action = handle_buttons(pos, width)
                if button_action:
                    if button_action == "start":
                        if not started and start and end:
                            for row in grid:
                                for cell in row:
                                    cell.update_neighbors(grid)

                            a_star(lambda: draw(win, grid, rows, width, manhattan_checked, euclidean_checked), grid,
                                   start, end, heuristic)

                            started = False
                    elif button_action == "random_walls":
                        num_walls = int(rows * rows * inc_obstacle_ratio)
                        for _ in range(num_walls):
                            row = random.randint(0, rows - 1)
                            col = random.randint(0, rows - 1)
                            if grid[row][col] != start and grid[row][col] != end:
                                grid[row][col].make_wall()

                    elif button_action == "reset":
                        for row in grid:
                            for cell in row:
                                if cell != start and cell != end:
                                    cell.reset()


                    elif button_action == "manhattan":
                        heuristic = "manhattan"
                        manhattan_checked = True
                        euclidean_checked = False

                    elif button_action == "euclidean":
                        heuristic = "euclidean"
                        manhattan_checked = False
                        euclidean_checked = True

                    else:
                        row, col = get_clicked_pos(pos, rows, width)
                        if 0 <= row < rows and 0 <= col < rows:
                            cell = grid[row][col]
                        else:
                            cell = None

                        if cell and cell != start and cell != end:  # Add condition to exclude start and end points
                            if cell.is_wall():
                                cell.reset()
                            else:
                                cell.make_wall()

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interactive A* Pathfinding Visualizer")
    parser.add_argument("-r", "--rows", type=int, default=30, help="Number of rows (default: 30)")
    parser.add_argument("-w", "--width", type=int, default=600, help="Window width (default: 600)")
    parser.add_argument("-o", "--obstacles", type=float, default=0.2, help="Obstacle ratio (default: 0.2)")

    args = parser.parse_args()

    ROWS = args.rows
    WIDTH = args.width
    INC_OBSTACLE_RATIO = args.obstacles

    pygame.init()
    WIN = pygame.display.set_mode((WIDTH + 200, WIDTH + 100))
    pygame.display.set_caption("A* Path Finding Visualizer")

    main(WIN, WIDTH, ROWS, INC_OBSTACLE_RATIO)