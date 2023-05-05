import pygame
import argparse
from screen import draw, handle_buttons, get_clicked_pos
from block import make_grid
from search import a_star
import math
import random


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
    dragging_erase = False

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
                    elif cell.is_wall():
                        cell.reset()  # 벽을 클릭하면 벽이 사라집니다.
                        dragging_erase = True
                    else:
                        cell.make_wall()

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_start = False
                dragging_end = False
                dragging_erase = False

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
                elif dragging_erase:  # 벽을 지우는 드래그 상태일 경우
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, rows, width)
                    if 0 <= row < rows and 0 <= col < rows:
                        cell = grid[row][col]
                        if cell.is_wall():
                            cell.reset()
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

                            success, explored_nodes = a_star(lambda: draw(win, grid, rows, width, manhattan_checked, euclidean_checked), grid, start, end, heuristic)

                            if success:
                                print(f"Total explored nodes: {explored_nodes}")

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
    parser.add_argument("-o", "--obstacles",type=float, default=0.2, help="Obstacle ratio (default: 0.2)")

    args = parser.parse_args()

    ROWS = args.rows
    WIDTH = args.width
    INC_OBSTACLE_RATIO = args.obstacles

    pygame.init()
    WIN = pygame.display.set_mode((WIDTH + 200, WIDTH + 100))
    pygame.display.set_caption("A* Path Finding Visualizer")

    main(WIN, WIDTH, ROWS, INC_OBSTACLE_RATIO)


