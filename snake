import tkinter as tk
from random import randint



BOARD_WIDTH = 10
BOARD_HEIGHT = 10

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 300

FPS = 3



class SnakeSegment:
    def __init__(self, x, y, direction):
        self._x = x
        self._y = y
        self._init_direction(direction)

    def _init_direction(self, direction):
        self._direction = direction
        if self._direction == "Up":
            self._dx = 0
            self._dy = -1
        elif self._direction == "Down":
            self._dx = 0
            self._dy = 1
        elif self._direction == "Left":
            self._dx = -1
            self._dy = 0
        elif self._direction == "Right":
            self._dx = 1
            self._dy = 0
        else:
            print('Direction can only be "Up", "Down", "Left" or "Right"')

    def __repr__(self):
        return f'SnakeSegment({self._x}, {self._y}, "{self._direction}")'

    def __eq__(self, other):
        return self._x == other.x and self._y ==other.y

    def turn(self, direction):
        self._init_direction(direction)

    def step(self):
        self._x += self._dx
        self._y += self._dy

    @property
    def direction(self):
        return self._direction

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def dx(self):
        return self._dx

    @property
    def dy(self):
        return self._dy



class Snake:
    def __init__(self):
        initial_direction = "Right"

        head = SnakeSegment(2, BOARD_HEIGHT // 2 - 1, initial_direction)
        body = SnakeSegment(1, BOARD_HEIGHT // 2 - 1, initial_direction)
        tail = SnakeSegment(0, BOARD_HEIGHT // 2 - 1, initial_direction)
        self.segments = [head, body, tail]

        self._new_head_direction = initial_direction

    def __repr__(self):
        output = ""
        for segment in self.segments:
            output += str(segment) + '\n'
        return output

    def turn(self, new_head_direction):
        forbiden_directions = {"Up":"Down", "Down":"Up", "Left":"Right", "Right":"Left"}
        if self.segments[0].direction != forbiden_directions[new_head_direction]:
            self._new_head_direction = new_head_direction
        return self

    def step(self):
        snake_length = len(self.segments)
        for i in reversed(range(1, snake_length)):
            self.segments[i].turn(self.segments[i - 1].direction)
        self.segments[0].turn(self._new_head_direction)

        for segment in self.segments:
            segment.step()

        return self

    def add_segment(self):
        tail = self.segments[-1]
        x = tail.x - tail.dx
        y = tail.y - tail.dy
        new_segment = SnakeSegment(x, y, tail.direction)
        self.segments.append(new_segment)
        return self

    def is_intersecting(self):
        head = self.segments[0]
        for segment in self.segments[1:]:
            if head == segment:
                return True
        return False



class Food:
    def __init__(self):
        self._x = randint(0, BOARD_WIDTH - 1)
        self._y = randint(0, BOARD_HEIGHT - 1)

    def new(self):
        self._x = randint(0, BOARD_WIDTH - 1)
        self._y = randint(0, BOARD_HEIGHT - 1)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y



class Board:
    def __init__(self, event_handler=None):
        self.event_handler = event_handler
        self._init_window()
        self._init_canvas()
        self._init_status_bar()

    def _init_window(self):
        self._root = tk.Tk()
        self._root.geometry(f"{WINDOW_WIDTH + 2}x{WINDOW_HEIGHT + 22}")
        self._root.title("Game Snake")
        self._root.resizable(False, False)

    def _init_canvas(self):
        self._canvas = tk.Canvas(self._root, bg="grey")
        self._canvas.pack(fill=tk.BOTH, expand=1)
        self._canvas.focus_force()
        self._canvas.bind("<Key>", self._onkeypress)

    def _init_status_bar(self):
        self._statusbar = tk.Label(self._root, text="on the way…", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self._statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def _onkeypress(self, event):
        if self.event_handler is not None:
            self.event_handler(event)

    def set_new_status(self, status):
        self._statusbar.config(text=status)

    @property
    def root(self):
        return self._root

    @property
    def canvas(self):
        return self._canvas



class Visualizer:
    def __init__(self, canvas):
        self.canvas = canvas

    def _draw_segment(self, segment, color="green", outline="gray"):
        segment_width = WINDOW_WIDTH / BOARD_WIDTH
        segment_height = WINDOW_HEIGHT / BOARD_HEIGHT
        self.canvas.create_rectangle(segment_width * segment.x,
                                     segment_height * segment.y,
                                     segment_width * segment.x + segment_width,
                                     segment_height * segment.y + segment_height,
                                     fill=color, outline=outline)

    def draw_snake(self, snake_segments):
        snake_body = snake_segments[1:]
        snake_head = snake_segments[0]
        color = 0
        for segment in snake_body:
            color += 10
            if color > 255:
                color = 0
            self._draw_segment(segment, f"#00{hex(color)[2:].rjust(2, '0')}00")
        self._draw_segment(snake_head, "yellow")

    def draw_food(self, food):
        self._draw_segment(food, "red")

    def create_text(self, text):
        self.canvas.create_text(WINDOW_WIDTH // 2,
                                WINDOW_HEIGHT // 2,
                                text=text,
                                justify=tk.CENTER,
                                font="Verdana 14",
                                fill="blue")



class Game(Board):
    def __init__(self):
        self._score = 0
        self._information = ""
        self._current_fps = FPS
        self._board = Board(self._onkeypress)
        self.snake = Snake()
        self.food = Food()
        self.visualizer = Visualizer(self._board.canvas)
        self._update()

    def _onkeypress(self, event):
        if event.keysym in ["Up", "w"]:
            self.snake.turn("Up")
        elif event.keysym in ["Down", "s"]:
            self.snake.turn("Down")
        elif event.keysym in ["Left", "a"]:
            self.snake.turn("Left")
        elif event.keysym in ["Right", "d"]:
            self.snake.turn("Right")
        elif event.keysym in "Nn":
            self.snake.add_segment()
        elif event.keysym in "Ll":
            self._current_fps += 0.5
        elif event.keysym in "Kk":
            self._current_fps -= 0.5

    def _update(self):
        self._board.canvas.delete("all")

        # one step forward
        if not self.snake.is_intersecting():
            self.snake.step()
        else:
            self._information = f"Self-intersection!\nGAME OVER!"
            self._visualize()
            return

        # eat food
        if self.snake.segments[0] == self.food:
            self._score += 1
            self.snake.add_segment()
            self.food.new()
            is_food_on_snake = True
            while is_food_on_snake and len(self.snake.segments) < BOARD_WIDTH * BOARD_HEIGHT:
                for segment in self.snake.segments:
                    if segment == self.food:
                        self.food.new()
                        break
                else:
                    is_food_on_snake = False

        self._board.set_new_status(f"Score: {self._score};   FPS: {self._current_fps}")

        # win
        if len(self.snake.segments) >= BOARD_WIDTH * BOARD_HEIGHT:
            self._information = f"YOU WON!\nYOUR SCORE is {self._score}"
            self._visualize()
            return

        # out of the board
        if (self.snake.segments[0].x < 0 or
                    self.snake.segments[0].x >= BOARD_WIDTH or
                    self.snake.segments[0].y < 0 or
                    self.snake.segments[0].y >= BOARD_HEIGHT):
            self._information = "Out the board.\nGAME OVER!"
            self._visualize()
            return

        self._visualize()
        self._board.root.after(round(1000 / self._current_fps), self._update)

    def _visualize(self):
        self.visualizer.draw_food(self.food)
        self.visualizer.draw_snake(self.snake.segments)
        self.visualizer.create_text(self._information)

    def mainloop(self):
        self._board.root.mainloop()



if __name__ == "__main__":
    s = Game()
    s.mainloop()
