import copy
import pygame
import random


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                pygame.draw.rect(screen, pygame.Color('green'),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size))

    def get_cell(self, pos):
        x = (pos[0] - self.left) // self.cell_size
        y = (pos[1] - self.top) // self.cell_size
        if x < 0 or x >= self.width or \
                y < 0 or y >= self.height:
            return None
        else:
            return x, y

    def on_click(self, cell):
        pass

    def get_click(self, pos):
        cell = self.get_cell(pos)
        self.on_click(cell)


class Lines(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.selected_cell = None

    def has_path(self, x1, y1, x2, y2):
        d = {(x1, y1): 0}
        v = [(x1, y1)]
        while len(v) > 0:
            x, y = v.pop(0)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx * dy != 0:
                        continue
                    if self.board[y + dy][x + dx] == 0:
                        dn = d.get((x + dx, y + dy), -1)
                        if dn == -1:
                            d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                            v.append((x + dx, y + dy))
        dist = d.get((x2, y2), -1)
        return dist >= 0

    def on_click(self, cell):
        x = cell[0]
        y = cell[1]
        if self.selected_cell is None:
            if self.board[y][x] == 1:
                self.selected_cell = x, y
            else:
                self.board[y][x] = 1
        else:
            if self.selected_cell == (x, y):
                self.selected_cell = None

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    color = pygame.Color('blue')
                    if self.selected_cell == (x, y):
                        color = pygame.Color('red')
                    pygame.draw.ellipse(screen, color,
                                        (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                         self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, pygame.Color('white'),
                                     (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                      self.cell_size, self.cell_size), 1)


def main():
    pygame.init()
    size = 420, 470
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('g')

    board = Lines(10, 10)
    board.set_view(10, 10, 40)
    ticks = 0

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)

            screen.fill((0, 0, 0))
            board.render(screen)
            if ticks == 50:
                ticks = 0
            pygame.display.flip()
            clock.tick(100)
            ticks += 1
    pygame.quit()


if __name__ == '__main__':
    main()
