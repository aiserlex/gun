import random
import tkinter as tk


BOARD_WIDTH = 10
BOARD_HEIGHT = 20

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 400

FPS = 1

cheat = 0


class Board:
    def __init__(self):
        self._array = [[0 for i in range(BOARD_WIDTH)] for j in range(BOARD_HEIGHT)]

    def print(self):
        for i in self._array:
            print(*i)

    def get_cell_value(self, x, y):
        if y < 0:
            return 0
        return self._array[y][x]

    def set_cell_value(self, x, y, value):
        self._array[y][x] = value

    def inc_cell_value(self, x, y):
        self._array[y][x] += 1

    def del_line(self, i):
        self._array.pop(i)
        self._array.insert(0, [0 for i in range(BOARD_WIDTH)])

    def add_tetromino(self, tetromino):
        deleted = 0
        for box in tetromino:
            self.inc_cell_value(box[0], box[1])
        for i, line in enumerate(self._array):
            if sum(line) == BOARD_WIDTH:
                self.del_line(i)
                deleted += 1
        return deleted

    @property
    def array(self):
        return self._array


class Tetromino:
    def __init__(self, x, y):
        global cheat
        if cheat:
            self._figure = "I"
            cheat = 0
        else:
            self._figure = random.choice("SZLJOTI")
        self._x = x
        self._y = y
        if self._figure == "S":
            self._fig_data = (
                                ((-1, 1), (0, 1), (0, 0), (1, 0)),
                                ((1, 1), (1, 0), (0, 0), (0, -1)),
                                ((-1, 1), (0, 1), (0, 0), (1, 0)),
                                ((1, 1), (1, 0), (0, 0), (0, -1)),
                             )
        elif self._figure == "Z":
            self._fig_data = (
                                ((-1, 0), (0, 0), (0, 1), (1, 1)),
                                ((-1, 1), (-1, 0), (0, 0), (0, -1)),
                                ((-1, 0), (0, 0), (0, 1), (1, 1)),
                                ((-1, 1), (-1, 0), (0, 0), (0, -1)),
                             )
        elif self._figure == "L":
            self._fig_data = (
                                ((-1, 0), (0, 0), (1, 0), (-1, 1)),
                                ((0, 1), (0, 0), (0, -1), (1, 1)),
                                ((-1, 0), (0, 0), (1, 0), (1, -1)),
                                ((0, 1), (0, 0), (0, -1), (-1, -1)),
                             )
        elif self._figure == "J":
            self._fig_data = (
                                ((-1, 0), (0, 0), (1, 0), (1, 1)),
                                ((0, 1), (0, 0), (0, -1), (1, -1)),
                                ((-1, 0), (0, 0), (1, 0), (-1, -1)),
                                ((-1, 1), (0, 1), (0, 0), (0, -1)),
                             )
        elif self._figure == "O":
            self._fig_data = (
                                ((-1, 0), (0, 0), (-1, 1), (0, 1)),
                                ((-1, 0), (0, 0), (-1, 1), (0, 1)),
                                ((-1, 0), (0, 0), (-1, 1), (0, 1)),
                                ((-1, 0), (0, 0), (-1, 1), (0, 1)),
                             )
        elif self._figure == "T":
            self._fig_data = (
                                ((-1, 0), (0, 0), (1, 0), (0, 1)),
                                ((0, 1), (0, 0), (0, -1), (1, 0)),
                                ((-1, 0), (0, 0), (1, 0), (0, -1)),
                                ((0, 1), (0, 0), (0, -1), (-1, 0)),
                             )
        elif self._figure == "I":
            self._fig_data = (
                                ((-2, 0), (-1, 0), (0, 0), (1, 0)),
                                ((0, 1), (0, 0), (0, -1), (0, -2)),
                                ((-2, 0), (-1, 0), (0, 0), (1, 0)),
                                ((0, 1), (0, 0), (0, -1), (0, -2)),
                              )

        self._turn = 0
        self._init_data = self._fig_data[self._turn]

    def get_current_data(self):
        curr_coords = []
        for box in self._init_data:
            curr_coords.append((box[0] + self._x, box[1] + self._y))
        return curr_coords

    def move_down(self):
        self._y += 1

    def can_move_down(self, board):
        curr_data = self.get_current_data()
        for box in curr_data:
            if (
                    box[1] + 1 >= BOARD_HEIGHT or
                    board.get_cell_value(box[0], box[1] + 1)
                ):
                return False
        return True

    def move_left(self):
        self._x -= 1

    def can_move_left(self, board):
        curr_data = self.get_current_data()
        for box in curr_data:
            if (
                    box[0] - 1 < 0 or
                    board.get_cell_value(box[0] - 1, box[1])
                ):
                return False
        return True

    def move_right(self):
        self._x += 1

    def can_move_right(self, board):
        curr_data = self.get_current_data()
        for box in curr_data:
            if (
                    box[0] + 1 >= BOARD_WIDTH or
                    board.get_cell_value(box[0] + 1, box[1])
                ):
                return False
        return True

    def turn_left(self):
        self._turn = (self._turn - 1) % 4
        self._init_data = self._fig_data[self._turn]

    def can_turn_left(self, board):
        turned_fig = self._fig_data[(self._turn - 1) % 4]
        for point in turned_fig:
            if (
                    point[0] + self._x < 0 or
                    point[0] + self._x >= BOARD_WIDTH or
                    point[1] + self._y >= BOARD_HEIGHT or
                    board.get_cell_value(point[0] + self._x, point[1] + self._y)
               ):
                return False
        return True

    def turn_right(self):
        self._turn = (self._turn + 1) % 4
        self._init_data = self._fig_data[self._turn]

    def can_turn_right(self, board):
        turned_fig = self._fig_data[(self._turn + 1) % 4]
        for point in turned_fig:
            if (
                    point[0] + self._x < 0 or
                    point[0] + self._x >= BOARD_WIDTH or
                    point[1] + self._y >= BOARD_HEIGHT or
                    board.get_cell_value(point[0] + self._x, point[1] + self._y)
               ):
                return False
        return True

    @property
    def data(self):
        return self.get_current_data()


class Window:
    def __init__(self):
        self._init_root()
        self._init_canvas()
        self._init_status_bar()

    def _init_root(self):
        self._root = tk.Tk()
        self._root.geometry(f"{WINDOW_WIDTH+2}x{WINDOW_HEIGHT+21}+500+200")
        self._root.title("Game Tetris")

    def _init_canvas(self):
        self._canvas = tk.Canvas(self._root, bg="grey")
        self._canvas.pack(fill=tk.BOTH, expand=1)
        self._canvas.focus_force()

    def _init_status_bar(self):
        self._statusbar = tk.Label(self._root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self._statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_new_status(self, status):
        self._statusbar.config(text=status)

    @property
    def root(self):
        return self._root

    @property
    def canvas(self):
        return self._canvas


class Vizual:
    def __init__(self, canvas):
        self._canvas = canvas

    def draw_block(self, block_x, block_y):
        block_width = WINDOW_WIDTH / BOARD_WIDTH
        block_height = WINDOW_HEIGHT / BOARD_HEIGHT
        self._canvas.create_rectangle(block_x * block_width,
                                      block_y * block_height,
                                      block_x * block_width + block_width,
                                      block_y * block_height + block_height,
                                      fill = "green", outline="black")

    def draw_tetromino(self, tetromino):
        curr_data = tetromino.get_current_data()
        for box in curr_data:
            self.draw_block(box[0], box[1])

    def draw_board(self, board):
        for y, row in enumerate(board):
            for x, val in enumerate(row):
                if val == 1:
                    self.draw_block(x, y)


class Game:
    def __init__(self):
        self._window = Window()
        self._window.canvas.bind("<Key>", self._onkeypress)
        self._board = Board()
        self._vizual = Vizual(self._window.canvas)
        self._tetromino = Tetromino(5, 0)
        self._lines = 0
        self._score = 0
        self._update()

    def _onkeypress(self, event):
        global cheat
        if event.keysym in ["Up", "w", "W"]:
            if self._tetromino.can_turn_left(self._board):
                self._tetromino.turn_left()
        elif event.keysym in ["Left", "a", "A"]:
            if self._tetromino.can_move_left(self._board):
                self._tetromino.move_left()
        elif event.keysym in ["Right", "d", "D"]:
            if self._tetromino.can_move_right(self._board):
                self._tetromino.move_right()
        elif event.keysym in ["Down", "s", "S"]:
            if self._tetromino.can_turn_right(self._board):
                self._tetromino.turn_right()
        elif event.keysym == "space":
            if self._tetromino.can_move_down(self._board):
                self._tetromino.move_down()
            else:
                lines = self._board.add_tetromino(self._tetromino.data)
                self._lines += lines
                self._score += lines * 4
                self._tetromino = Tetromino(5, 0)
        elif event.keysym in "oO":
            cheat = 1

        self._visualize()


    def _update(self):
        if self._tetromino.can_move_down(self._board):
            self._tetromino.move_down()
        else:
            lines = self._board.add_tetromino(self._tetromino.data)
            self._lines += lines
            self._score += lines * 4
            self._tetromino = Tetromino(5, 0)

        self._visualize()

        self._window.root.after(round(1000 / FPS), self._update)

    def _visualize(self):
        global cheat
        self._window.canvas.delete("all")
        self._vizual.draw_board(self._board.array)
        self._vizual.draw_tetromino(self._tetromino)

        status = f"Score: {self._score}; Lines: {self._lines}; FPS: {FPS}"
        if cheat:
            status += " (cheat on)"
        self._window.set_new_status(status)

    def mainloop(self):
        self._window.root.mainloop()


if __name__ == "__main__":
    game = Game()
    game.mainloop()
