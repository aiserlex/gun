import random
import tkinter as tk


BOARD_WIDTH = 10
BOARD_HEIGHT = 20

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 400

FPS = 2


class Window:
    def __init__(self):
        self._init_root()
        self._init_canvas()
        self._init_status_bar()

    def _init_root(self):
        self._root = tk.Tk()
        self._root.title("Game Tetris")
        # self._root.resizable(False, False)
        # self._root.geometry(f"{WINDOW_WIDTH+4}x{WINDOW_HEIGHT+23}+500+200")

    def _init_canvas(self):
        self._canvas = tk.Canvas(
            self._root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg="grey",
        )
        self._canvas.pack()
        self._canvas.focus_force()

    def _init_status_bar(self):
        self._statusbar = tk.Label(
            self._root,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W  # текст по левому краю
        )
        self._statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_new_status(self, status):
        self._statusbar.config(text=status)

    @property
    def root(self):
        return self._root

    @property
    def canvas(self):
        return self._canvas


class Board:
    def __init__(self):
        self._data = [[0 for i in range(BOARD_WIDTH)] for j in range(BOARD_HEIGHT)]

    def _set_cell_value(self, x, y, value):
        self._data[y][x] = value

    def _inc_cell_value(self, x, y):
        self._data[y][x] += 1

    def print(self):
        for line in self._data:
            print(*line)

    def get_cell_value(self, x, y):
        if y < 0:
            return 0
        return self._data[y][x]

    def add_tetromino(self, tetromino):
        for segment in tetromino.get_current_coords():
            self._inc_cell_value(segment[0], segment[1])

    def delete_full_lines(self):
        number_of_lines = 0
        for i, line in enumerate(self._data):
            if sum(line) == BOARD_WIDTH:
                self._data.pop(i)
                self._data.insert(0, [0 for i in range(BOARD_WIDTH)])
                number_of_lines += 1
        return number_of_lines

    @property
    def data(self):
        return self._data


class Tetromino:
    def __init__(self, x, y, figure):
        self._x = x
        self._y = y
        self._orientation = 0
        if figure == "S":
            self._data = (
                ((-1, 1), (0, 1), (0, 0), (1, 0)),
                ((1, 1), (1, 0), (0, 0), (0, -1)),
                ((-1, 1), (0, 1), (0, 0), (1, 0)),
                ((1, 1), (1, 0), (0, 0), (0, -1)),
            )
        elif figure == "Z":
            self._data = (
                ((-1, 0), (0, 0), (0, 1), (1, 1)),
                ((-1, 1), (-1, 0), (0, 0), (0, -1)),
                ((-1, 0), (0, 0), (0, 1), (1, 1)),
                ((-1, 1), (-1, 0), (0, 0), (0, -1)),
            )
        elif figure == "L":
            self._data = (
                ((-1, 0), (0, 0), (1, 0), (-1, 1)),
                ((0, 1), (0, 0), (0, -1), (1, 1)),
                ((-1, 0), (0, 0), (1, 0), (1, -1)),
                ((0, 1), (0, 0), (0, -1), (-1, -1)),
            )
        elif figure == "J":
            self._data = (
                ((-1, 0), (0, 0), (1, 0), (1, 1)),
                ((0, 1), (0, 0), (0, -1), (1, -1)),
                ((-1, 0), (0, 0), (1, 0), (-1, -1)),
                ((-1, 1), (0, 1), (0, 0), (0, -1)),
            )
        elif figure == "O":
            self._data = (
                ((-1, 0), (0, 0), (-1, 1), (0, 1)),
                ((-1, 0), (0, 0), (-1, 1), (0, 1)),
                ((-1, 0), (0, 0), (-1, 1), (0, 1)),
                ((-1, 0), (0, 0), (-1, 1), (0, 1)),
            )
        elif figure == "T":
            self._data = (
                ((-1, 0), (0, 0), (1, 0), (0, 1)),
                ((0, 1), (0, 0), (0, -1), (1, 0)),
                ((-1, 0), (0, 0), (1, 0), (0, -1)),
                ((0, 1), (0, 0), (0, -1), (-1, 0)),
            )
        elif figure == "I":
            self._data = (
                ((-2, 0), (-1, 0), (0, 0), (1, 0)),
                ((0, 1), (0, 0), (0, -1), (0, -2)),
                ((-2, 0), (-1, 0), (0, 0), (1, 0)),
                ((0, 1), (0, 0), (0, -1), (0, -2)),
            )

    def _can_move_left(self, board):
        current_coords = self.get_current_coords()
        for segment in current_coords:
            if (
                segment[0] - 1 < 0 or
                board.get_cell_value(segment[0] - 1, segment[1])
            ):
                return False
        return True

    def _can_move_right(self, board):
        current_coords = self.get_current_coords()
        for segment in current_coords:
            if (
                segment[0] + 1 >= BOARD_WIDTH or
                board.get_cell_value(segment[0] + 1, segment[1])
            ):
                return False
        return True

    def _can_turn(self, board):
        current_coords = self.get_current_coords((self._orientation - 1) % 4)
        for segment in current_coords:
            if (
                segment[0] < 0 or
                segment[0] >= BOARD_WIDTH or
                segment[1] >= BOARD_HEIGHT or
                board.get_cell_value(segment[0], segment[1])
            ):
                return False
        return True

    def try_move_left(self, board):
        if self._can_move_left(board):
            self._x -= 1

    def try_move_right(self, board):
        if self._can_move_right(board):
            self._x += 1

    def try_turn(self, board):
        if self._can_turn(board):
            self._orientation = (self._orientation - 1) % 4

    def get_current_coords(self, orientation=None):
        if orientation is None:
            orientation = self._orientation
        current_coords = []
        for segment in self._data[orientation]:
            x = segment[0] + self._x
            y = segment[1] + self._y
            current_coords.append((x, y))
        return current_coords

    def can_move_down(self, board):
        current_coords = self.get_current_coords()
        for segment in current_coords:
            if (
                segment[1] + 1 >= BOARD_HEIGHT or
                board.get_cell_value(segment[0], segment[1] + 1)
            ):
                return False
        return True

    def move_down(self):
        self._y += 1


class Visual:
    def __init__(self, canvas):
        self._canvas = canvas

    def _draw_segment(self, x, y):
        width = WINDOW_WIDTH / BOARD_WIDTH
        height = WINDOW_HEIGHT / BOARD_HEIGHT
        self._canvas.create_rectangle(
            x * width,
            y * height,
            (x + 1) * width,
            (y + 1) * height,
            fill="green",
            outline="black",
        )

    def draw_tetromino(self, tetromino):
        for segment in tetromino.get_current_coords():
            self._draw_segment(segment[0], segment[1])

    def draw_board(self, board):
        for y, row in enumerate(board.data):
            for x, val in enumerate(row):
                if val == 1:
                    self._draw_segment(x, y)

    def add_text(self, text):
        self._canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            text=text,
            justify=tk.CENTER,
            font="Verdana 14",
            fill="blue",
        )


class Game:
    def __init__(self):
        self._fps = FPS
        self._score = 0
        self._deletions = 0
        self._next_figure = [random.choice("SZLJOTI") for i in range(1)]

        self._window = Window()
        self._window.canvas.bind("<Key>", self._onkeypress)

        self._board = Board()
        self._visual = Visual(self._window.canvas)


        self._new_tetromino()

        self._update()

    def _onkeypress(self, event):
        if event.keysym in ["Left", "a", "A"]:
            self._tetromino.try_move_left(self._board)

        elif event.keysym in ["Right", "d", "D"]:
            self._tetromino.try_move_right(self._board)

        elif event.keysym in ["Up", "w", "W"]:
            self._tetromino.try_turn(self._board)

        elif event.keysym in ["Down", "s", "S"]:
            self._move_tetromino_down()

        elif event.keysym in ["space"]:
            while self._tetromino.can_move_down(self._board):
                self._tetromino.move_down()

        self._visualize()

    def _update(self):
        self._move_tetromino_down()
        if (score := self._board.delete_full_lines()):
            self._score += score
            self._deletions += 1
            if self._deletions == 16 * (self._fps + 1 - FPS):
                self._fps += 1

        self._visualize()

        if sum(self._board.data[0]) != 0:
            self._visual.add_text("GAME OVER")
            return

        self._window.root.after(round(1000 / self._fps), self._update)

    def _visualize(self):
        self._window.canvas.delete("all")

        self._visual.draw_tetromino(self._tetromino)
        self._visual.draw_board(self._board)

        status = f"Score: {self._score}; "
        status += f"FPS: {self._fps}; "
        status += f"Next: {' '.join(self._next_figure)}"
        self._window.set_new_status(status)

    def _move_tetromino_down(self):
        if self._tetromino.can_move_down(self._board):
            self._tetromino.move_down()
        else:
            self._board.add_tetromino(self._tetromino)
            self._new_tetromino()

    def _new_tetromino(self):
        self._tetromino = Tetromino(BOARD_WIDTH // 2, 0, self._next_figure.pop(0))
        self._next_figure.append(random.choice("SZLJOTI"))

    def mainloop(self):
        self._window.root.mainloop()


if __name__ == "__main__":
    game = Game()
    game.mainloop()
