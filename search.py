import numpy as np
import pygame
from pygame.locals import * # for mouse stuff
import time
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from collections import deque

pygame.font.init()
font = pygame.font.Font('fonts/PressStart2P.ttf', 8)

WIN_SIZE = (600, 700)
GRID_WIDTH = 20
GRID_LENGTH = 25
GRID_SQUARE_LENGTH = 20
STEP_DELAY = .005
OFFSETS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# preset colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHT_GREEN = (66, 255, 0)
GREEN = (0, 255, 0)
BRIGHT_RED = (254, 27, 7)
PURPLE = (128, 0, 128)
LIGHT_GREY = (155, 155, 155)
DARK_GREY = (55, 55, 55)
LIGHTER_GREY = (200, 200, 200)


class Grid:
    def __init__(self, width, length, left, top, square_length, start, end, screen):
        self.width = width
        self.length = length
        self.grid = [[0] * width for _ in range(length)]
        self.rect_grid = [[None] * width for _ in range(length)]
        for i in range(length):
            for j in range(width):
                r_left = left + square_length * i + 1
                r_top = top + square_length * j + 1
                r = pygame.Rect(r_left, r_top, square_length - 2, square_length - 2)
                # the +1 and -2 in the above lines is to add 1px padding around each square
                # will be changed later to customizable width
                self.rect_grid[i][j] = r
        self.width = width
        self.length = length
        self.left = left
        self.top = top
        self.start = start
        self.square_length = square_length
        self.end = end
        self.screen = screen

    def change(self, i, j, val):
        self.grid[i][j] = self.grid[i][j] + val if self.grid[i][j] + val >= 0 else 0

    def bfs(self):
        self.clear_non_obstructed()
        pygame.display.flip()
        visited = [[False] * self.width for _ in range(self.length)]
        visited[self.start[0]][self.start[1]] = True
        queue = deque()
        queue.append(self.start)
        parent = {self.start: None}
        while len(queue) > 0:
            time.sleep(STEP_DELAY)
            v = queue.popleft()
            pygame.draw.rect(self.screen, BRIGHT_GREEN, self.rect_grid[v[0]][v[1]])
            pygame.display.update(self.rect_grid[v[0]][v[1]])
            if v == self.end:
                break
            for o in OFFSETS:
                u = (v[0] + o[0], v[1] + o[1])
                if 0 <= u[0] < self.length and 0 <= u[1] < self.width and not visited[u[0]][u[1]] and not self.grid[u[0]][u[1]]:
                    parent[u] = v
                    visited[u[0]][u[1]] = True
                    queue.append(u)
            # time.sleep(STEP_DELAY)
            # pygame.draw.rect(self.screen, BRIGHT_GREEN, self.rect_grid[v[0]][v[1]])
            # pygame.display.update(self.rect_grid[v[0]][v[1]])
        if self.end in parent:
            time.sleep(0.500)
            v = self.end
            while v:
                pygame.draw.rect(self.screen, PURPLE, self.rect_grid[v[0]][v[1]])
                pygame.display.update(self.rect_grid[v[0]][v[1]])
                v = parent[v]
                time.sleep(STEP_DELAY * 5)
        else:
            print('no path exists from {0} to {1}'.format(self.start, self.end))
        print('bfs complete')

    # TODO
    def djikstra(self):
        pass

    def draw_to_screen(self, color=WHITE):
        outer_border = pygame.Rect(self.left - 4, self.top - 4, self.length*self.square_length + 8, self.width*self.square_length + 8)
        pygame.draw.rect(self.screen, LIGHT_GREY, outer_border)
        inner_border = pygame.Rect(self.left - 2, self.top - 2, self.length *self.square_length + 4, self.width*self.square_length + 4)
        pygame.draw.rect(self.screen, BLACK, inner_border)

        pygame.draw.rect(self.screen, BLACK, pygame.Rect(self.left - 3*self.square_length-2, self.top, 3*self.square_length+1, self.square_length+1))
        screen.blit(font.render('Start', True, WHITE), (self.left - 44, self.top+7))
        pygame.draw.rect(self.screen, BLACK, pygame.Rect(self.left + (self.length)*self.square_length, self.top + (self.width-1)*self.square_length, self.square_length*3, self.square_length))
        screen.blit(font.render('End', True, WHITE), (self.left+(self.length)*self.square_length+6, self.top+(self.width-1)*self.square_length+7))
        for row in self.rect_grid:
            for rect in row:
                pygame.draw.rect(self.screen, color, rect)

    def clear(self):
        for row in self.rect_grid:
            for rect in row:
                pygame.draw.rect(self.screen, WHITE, rect)

    def clear_non_obstructed(self):
        for i, row in enumerate(self.rect_grid):
            for j, rect in enumerate(row):
                if not self.grid[i][j]:
                    pygame.draw.rect(self.screen, WHITE, rect)

    def find_rect(self, x_pos, y_pos):
        # binary search would be more efficient, but
        # this function will not be a bottleneck in performance
        for i in range(self.length):
            r = self.rect_grid[i][0]
            if r.left <= x_pos <= r.left + r.width:
                for j in range(self.width):
                    r = self.rect_grid[i][j]
                    if r.top <= y_pos <= r.top + r.height:
                        return (r, i, j)
                return None
        return None

# clearly hardcoded
def draw_header(screen, left, top, width, height, padding):
    pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(left-padding, top-padding, width+2*padding, height+2*padding))
    pygame.draw.rect(screen, BLACK, pygame.Rect(left, top, width, height))
    big_font = pygame.font.Font('fonts/PressStart2P.ttf', 30)
    screen.blit(big_font.render('MAZE SOLVER v1.0', True, WHITE), (left+10, top+15))

def draw_info(screen, left, top, width, height, padding):
    pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(left-padding, top-padding, width+2*padding, height+2*padding))
    pygame.draw.rect(screen, WHITE, pygame.Rect(left, top, width, height))

    pygame.draw.rect(screen, LIGHTER_GREY, pygame.Rect(left + 10, top + 10, width //2 - 20, height - 20))

    pygame.draw.rect(screen, BLACK, pygame.Rect(left + 20, top + 20, GRID_SQUARE_LENGTH, GRID_SQUARE_LENGTH))
    pygame.draw.rect(screen, WHITE, pygame.Rect(left + 21, top + 21, GRID_SQUARE_LENGTH-2, GRID_SQUARE_LENGTH-2))
    screen.blit(font.render('= Available square', True, BLACK), (left + 50, top + 27))

    pygame.draw.rect(screen, BLACK, pygame.Rect(left + 20, top + 50, GRID_SQUARE_LENGTH, GRID_SQUARE_LENGTH))
    pygame.draw.rect(screen, BRIGHT_RED, pygame.Rect(left + 21, top + 51, GRID_SQUARE_LENGTH-2, GRID_SQUARE_LENGTH-2))
    screen.blit(font.render('= Unavailable square', True, BLACK), (left + 50, top + 57))

    pygame.draw.rect(screen, BLACK, pygame.Rect(left + 20, top + 80, GRID_SQUARE_LENGTH, GRID_SQUARE_LENGTH))
    pygame.draw.rect(screen, BRIGHT_GREEN, pygame.Rect(left + 21, top + 81, GRID_SQUARE_LENGTH-2, GRID_SQUARE_LENGTH-2))
    screen.blit(font.render('= Visited square', True, BLACK), (left + 50, top + 87))

    pygame.draw.rect(screen, BLACK, pygame.Rect(left + 20, top + 110, GRID_SQUARE_LENGTH, GRID_SQUARE_LENGTH))
    pygame.draw.rect(screen, PURPLE, pygame.Rect(left + 21, top + 111, GRID_SQUARE_LENGTH-2, GRID_SQUARE_LENGTH-2))
    screen.blit(font.render('= Shortest path', True, BLACK), (left + 50, top + 117))

    pygame.draw.rect(screen, LIGHTER_GREY, pygame.Rect(left + width // 2 + 10, top + 10, width // 2 - 20, height - 20))

    screen.blit(font.render('Press \'enter\' to start', True, BLACK), (left + width // 2 + 20, top + 27))
    screen.blit(font.render('Press \'c\' to clear all', True, BLACK), (left + width // 2 + 20, top + 57))
    screen.blit(font.render('Press \'v\' to clear visited', True, BLACK), (left + width // 2 + 20, top + 87))
    screen.blit(font.render('Click/drag to toggle maze', True, BLACK), (left + width // 2 + 20, top + 117))



if __name__ == '__main__':
    screen = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption('Maze Solver v1.0')
    G = Grid(GRID_WIDTH, GRID_LENGTH, 50, 250, GRID_SQUARE_LENGTH, (0,0), (GRID_LENGTH-1, GRID_WIDTH-1), screen=screen)
    G.draw_to_screen()
    dragging = False
    drag_color = BRIGHT_RED
    draw_header(screen, 50, 10, 500, 55, 3)
    draw_info(screen, 50, 80, 500, 150, 3)
    pygame.display.flip()

    while True:
        event = pygame.event.wait() # this saves a TON of cpu usage
        #events = pygame.event.get()
        #for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN and event.mod == KMOD_NONE:
            if event.key == K_RETURN:
                G.bfs()
            elif event.key == K_c:
                G.clear()
                G.grid = [[0] * G.width for _ in range(G.length)]
                pygame.display.flip()
            elif event.key == K_v:
                G.clear_non_obstructed()
                pygame.display.flip()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            G.clear_non_obstructed()
            pygame.display.flip()
            tup = G.find_rect(*pygame.mouse.get_pos())
            if tup:
                (r, i, j) = tup
                G.grid[i][j] = not G.grid[i][j]
                dragging = True
                drag_color = BRIGHT_RED if G.grid[i][j] else WHITE
                pygame.draw.rect(screen, BRIGHT_RED if G.grid[i][j] else WHITE, r)
                pygame.display.update(r)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            tup = G.find_rect(*pygame.mouse.get_pos())
            if tup:
                (r, i, j) = tup
                G.grid[i][j] = 1 if drag_color == BRIGHT_RED else 0
                pygame.draw.rect(screen, drag_color, r)
                pygame.display.update(r)
