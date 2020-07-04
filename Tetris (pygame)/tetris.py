import pygame
import random
from config import *
from data import DATA


class Tetraminoe:
    def new(self):
        self.figure = random.choice("SZJLOIIIT")
        self.data = DATA[self.figure]
        self.orientation = 0
        self.x0 = BOARD_WIDTH // 2
        self.y0 = 0
        self.update_coords()
        self.state = {'turn':False, 'move_left':False, 'move_right':False, 'move_down':False, 'fall':False}
        return self

    def update_coords(self):
        self.coords = [(self.x0 + i, self.y0 + j) for i, j in self.data[self.orientation]]

    def draw(self, screen):
        block_width = WINDOW_WIDTH // BOARD_WIDTH
        block_height = WINDOW_HEIGHT // BOARD_HEIGHT
        for vertex in self.coords:
            rect = pygame.Rect(vertex[0] * block_width + 1, vertex[1] * block_height + 1, block_width - 1, block_height - 1)
            pygame.draw.rect(screen, RED, rect)

    def move_down(self):
        self.y0 += 1
        self.update_coords()

    def move_left(self):
        self.x0 -= 1
        self.update_coords()

    def move_right(self):
        self.x0 += 1
        self.update_coords()

    def turn(self):
        self.orientation = (self.orientation - 1) % len(self.data)
        self.update_coords()


class Board:
    def __init__(self):
        self.data = [0] * (BOARD_WIDTH * BOARD_HEIGHT)

    def __str__(self):
        rezult = ""
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                rezult += str(self.data[i * BOARD_WIDTH + j]) + " "
            rezult += "\n"
        return rezult

    __repr__ = __str__

    def get_cell(self, x, y):
        if x >= 0 and y >= 0:
            return self.data[y * BOARD_WIDTH + x]
        else:
            return 0

    def set_cell(self, x, y, value):
        if x >= 0 and y >= 0:
            self.data[y * BOARD_WIDTH + x] = value

    def get_line(self, y):
        return self.data[y * BOARD_WIDTH:(y + 1) * BOARD_WIDTH]

    def del_line(self, y):
        self.data[y * BOARD_WIDTH:(y + 1) * BOARD_WIDTH] = []
        self.data = [0]*BOARD_WIDTH + self.data

    def draw(self, screen):
        block_width = WINDOW_WIDTH // BOARD_WIDTH
        block_height = WINDOW_HEIGHT // BOARD_HEIGHT
        for i in range(BOARD_WIDTH):
            pygame.draw.line(screen, GREY, (i * block_width, 0), (i * block_width, WINDOW_HEIGHT))
        for i in range(BOARD_HEIGHT):
            pygame.draw.line(screen, GREY, (0, i * block_height), (WINDOW_WIDTH, i * block_height))
        for index, cell in enumerate(self.data):
            if cell:
                y0, x0 = divmod(index, BOARD_WIDTH)
                rect = pygame.Rect(x0 * block_width+1, y0 * block_height+1, block_width-1, block_height-1)
                pygame.draw.rect(screen, GREEN, rect)

    def add_tetraminoe(self, tetraminoe):
        for x, y in tetraminoe.coords:
            self.set_cell(x, y, 1)

    def can_move_down(self, tetraminoe):
        for vertex in tetraminoe.coords:
            if vertex[1] >= BOARD_HEIGHT - 1:
                return False
            elif self.get_cell(vertex[0], vertex[1] + 1):
                return False
        return True

    def can_move_left(self, tetraminoe):
        for vertex in tetraminoe.coords:
            if vertex[0] <= 0:
                return False
            elif self.get_cell(vertex[0] - 1, vertex[1]):
                return False
        return True

    def can_move_right(self, tetraminoe):
        for vertex in tetraminoe.coords:
            if vertex[0] >= BOARD_WIDTH - 1:
                return False
            elif self.get_cell(vertex[0] + 1, vertex[1]):
                return False
        return True

    def can_turn(self, tetraminoe):
        data = tetraminoe.data[tetraminoe.orientation - 1]
        coords = [(tetraminoe.x0 + i, tetraminoe.y0 + j) for i, j in data]
        for vertex in coords:
            if vertex[0] < 0:
                return False
            if vertex[0] >= BOARD_WIDTH:
                return False
            if vertex[1] >= BOARD_HEIGHT:
                return False
            if self.get_cell(*vertex):
                return False
        return True

    def del_full_lines(self):
        full_lines_number = 0
        for y in range(BOARD_HEIGHT):
            if all(self.get_line(y)):
                full_lines_number += 1
                self.del_line(y)
        return full_lines_number


class Game():
    def __init__(self):
        pygame.init()
        # pygame.mixer.init()  # for sounds
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.tetraminoe = Tetraminoe().new()
        self.board = Board()
        self.frame_counter = 0
        self.speeds = [120, 60, 40, 30, 24, 20, 15, 12, 10, 8, 6, 5, 4, 3, 2, 1]  # for FPS=120
        self.game_speed = 1
        self.score = 0

    def mainloop(self):
        self.running = True
        while self.running:
            self.frame_counter = (self.frame_counter + 1) % FPS
            self.clock.tick(FPS)
            pygame.display.flip()
            self.screen.fill(BLACK)

            self.process_events()
            self.update()
            self.draw()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (119, 273):  # w or up key
                    self.tetraminoe.state['turn'] = True

                if event.key in (115, 274):  # s or down key
                    self.tetraminoe.state['move_down'] = True

                if event.key in (97, 276):  # a or left key
                    self.tetraminoe.state['move_left'] = True

                if event.key in (100, 275):  # d or right key
                    self.tetraminoe.state['move_right'] = True

                if event.key in (32, ):  # space key
                    self.tetraminoe.state['fall'] = True

    def update(self):
        ''' process key events '''
        if self.tetraminoe.state['turn']:
            if self.board.can_turn(self.tetraminoe):
                self.tetraminoe.turn()
            self.tetraminoe.state['turn'] = False

        if self.tetraminoe.state['move_down']:
            if self.board.can_move_down(self.tetraminoe):
                self.tetraminoe.move_down()
            self.tetraminoe.state['move_down'] = False

        if self.tetraminoe.state['move_left']:
            if self.board.can_move_left(self.tetraminoe):
                self.tetraminoe.move_left()
            self.tetraminoe.state['move_left'] = False

        if self.tetraminoe.state['move_right']:
            if self.board.can_move_right(self.tetraminoe):
                self.tetraminoe.move_right()
            self.tetraminoe.state['move_right'] = False

        if self.tetraminoe.state['fall']:
            while self.board.can_move_down(self.tetraminoe):
                self.tetraminoe.move_down()
            self.tetraminoe.state['fall'] = False

        ''' next step '''
        if self.frame_counter % self.speeds[self.game_speed] == 0:
            if self.board.can_move_down(self.tetraminoe):
                self.tetraminoe.move_down()
            else:
                self.board.add_tetraminoe(self.tetraminoe)
                delta = self.board.del_full_lines()
                if delta:
                    self.score += delta
                    print(f"Score: {self.score}")
                if any(self.board.get_line(0)):
                    self.running = False
                    print("Game over!")
                self.tetraminoe.new()

    def draw(self):
        self.tetraminoe.draw(self.screen)
        self.board.draw(self.screen)

    def quit(self):
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.mainloop()
    game.quit()
