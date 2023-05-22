import pygame
import math
from queue import PriorityQueue


#거리 계산
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
            return True, count

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


    # 경로가 발견되지 않았다는 메시지를 출력
    print("Path not found.")

    return False, count


def no_solution_path(came_from, lowest_f_node, draw):
    current = lowest_f_node
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()