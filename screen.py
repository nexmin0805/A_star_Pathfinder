import pygame


def draw(win, grid, rows, width, manhattan_checked, euclidean_checked):
    win.fill((255, 255, 255))

    for row in grid:
        for cell in row:
            cell.draw(win)

    draw_grid(win, rows, width)
    draw_buttons(win, width, manhattan_checked, euclidean_checked)
    pygame.display.update()


# 그리드 생성
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, (128, 128, 128), (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, (128, 128, 128), (j * gap, 0), (j * gap, width))


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


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def handle_buttons(pos, width):
    x, y = pos
    if 10 <= x <= 200 and width + 25 <= y <= width + 75:
        return "start"
    elif 240 <= x <= 410 and width + 25 <= y <= width + 75:
        return "random_walls"
    elif 450 <= x <= 600 and width + 25 <= y <= width + 75:
        return "reset"
    elif (650 <= x <= 770 and 80 <= y <= 110) or (625 <= x <= 640 and 85 <= y <= 100):
        return "manhattan"
    elif (650 <= x <= 770 and 150 <= y <= 180) or (625 <= x <= 640 and 155 <= y <= 170):
        return "euclidean"
    return None
