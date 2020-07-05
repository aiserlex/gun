import pickle
import pygame
import random

from collections import defaultdict


FPS = 60

BOARD_WIDTH = 100
BOARD_HEIGHT = 80

BLOCK_WIDTH = 10
BLOCK_HEIGHT = 10

BLACK =     (0, 0, 0)
DARK_GRAY = (50, 50, 50)
GRAY = (127, 127, 127)
LITE_GRAY = (200, 200, 200)
WHITE = (255, 255, 255)


class Cells:
    def __init__(self):
        self._cells = set()

    def __str__(self):
        return str(self._cells)

    def clear(self):
        self._cells.clear()

    def add(self, new_cell):
        self._cells.add(new_cell)

    def discard(self, cell):
        self._cells.discard(cell)

    def draw(self, screen):
        for cell in self._cells:
            rect = pygame.Rect(
                    cell[0] * BLOCK_WIDTH + 1,
                    cell[1] * BLOCK_HEIGHT + 1,
                    BLOCK_WIDTH - 1,
                    BLOCK_HEIGHT - 1
            )
            pygame.draw.rect(screen, WHITE, rect)

    def _get_all_neighbours(self):
        self._neighbours = defaultdict(int)
        for cell in self._cells:
            self._neighbours[(cell[0] - 1, cell[1] - 1)] += 1
            self._neighbours[(cell[0] - 1, cell[1] + 1)] += 1
            self._neighbours[(cell[0] + 1, cell[1] - 1)] += 1
            self._neighbours[(cell[0] + 1, cell[1] + 1)] += 1
            self._neighbours[(cell[0] - 1, cell[1])] += 1
            self._neighbours[(cell[0] + 1, cell[1])] += 1
            self._neighbours[(cell[0], cell[1] - 1)] += 1
            self._neighbours[(cell[0], cell[1] + 1)] += 1

    def get_new_generation(self):
        self._get_all_neighbours()
        self._new_generation_cells = set()
        for cell, amount in self._neighbours.items():
            if amount == 3:
                self._new_generation_cells.add(cell)
            elif amount == 2 and cell in self._cells:
                self._new_generation_cells.add(cell)
        self._cells = set(self._new_generation_cells)


class Board:
    @staticmethod
    def get_board_coords(window_x, window_y):
        board_x = window_x // BLOCK_WIDTH
        board_y = window_y // BLOCK_HEIGHT
        return board_x, board_y

    @staticmethod
    def draw(screen):
        for i in range(BOARD_WIDTH + 1):
            pygame.draw.line(
                    screen,
                    GRAY,
                    (i * BLOCK_WIDTH, 0),
                    (i * BLOCK_WIDTH, BOARD_HEIGHT * BLOCK_HEIGHT),
                    1
            )
        for i in range(BOARD_HEIGHT + 1):
            pygame.draw.line(
                    screen,
                    GRAY,
                    (0, i * BLOCK_HEIGHT),
                    (BOARD_WIDTH * BLOCK_WIDTH, i * BLOCK_HEIGHT),
                    1
            )


class Game():
    def __init__(self):
        pygame.init()
        # pygame.mixer.init()  # for sounds
        pygame.display.set_caption("Game of Life")
        window_width = BOARD_WIDTH * BLOCK_WIDTH + 1
        window_height = BOARD_HEIGHT * BLOCK_HEIGHT + 1
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.cells = Cells()
        self.frames = 0
        self.speed = FPS // 2
        self.pause = True

    def mainloop(self):
        self.running = True
        while self.running:
            self.frames += 1
            self.clock.tick(FPS)
            pygame.display.flip()
            self.screen.fill(LITE_GRAY)

            self.process_events()
            self.update()
            self.draw()

    def change_speed(self, acceleration):
        if acceleration == "up":
            self.speed = self.speed // 2
            if self.speed < 1:
                self.speed = 1
            else: print("Speed up")
        elif acceleration == "down":
            self.speed = self.speed * 2
            if self.speed > 2 * FPS:
                self.speed = 2 * FPS
            else: print("Speed down")

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
                elif event.key == pygame.K_c:
                    self.cells.clear()
                elif event.key == pygame.K_s:
                    pickle.dump(self.cells, open("save.txt", "wb"))
                elif event.key == pygame.K_l:
                    self.cells = pickle.load(open("save.txt", "rb"))
                elif event.key == pygame.K_g:
                    self.cells = pickle.load(open("gun.txt", "rb"))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x0, y0 = self.board.get_board_coords(*event.pos)
                    self.cells.add((x0, y0))
                elif event.button == 3:
                    x0, y0 = self.board.get_board_coords(*event.pos)
                    self.cells.discard((x0, y0))
                elif event.button == 4:
                    self.change_speed("up")
                    # print("Speed up")
                elif event.button == 5:
                    self.change_speed("down")
                    # print("Speed down")
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] == 1:
                    x0, y0 = self.board.get_board_coords(*event.pos)
                    self.cells.add((x0, y0))
                elif event.buttons[2] == 1:
                    x0, y0 = self.board.get_board_coords(*event.pos)
                    self.cells.discard((x0, y0))

    def update(self):
        if not self.pause and self.frames % self.speed == 0:
            self.cells.get_new_generation()

    def draw(self):
        self.board.draw(self.screen)
        self.cells.draw(self.screen)

    def quit(self):
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.mainloop()
    game.quit()
