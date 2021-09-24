import sys
import tkinter as tk


class Application(object):
    def __init__(self, win_size=800, radius=220):
        self._root = tk.Tk()
        self._root.title('lab1')

        while win_size <= radius:
            win_size += 10
        self._win_size = win_size
        self.window = tk.Canvas(master=self._root, width=self._win_size, height=self._win_size,
                                borderwidth=0, highlightthickness=0, bg='white')
        self.window.grid()
        self.circle = Circle(win_size=win_size, radius=radius)

    def draw_circle(self) -> None:
        self.window.create_oval(self.circle.top_left[0], self.circle.top_left[1],
                                self.circle.bottom_right[0], self.circle.bottom_right[1],
                                outline='black', width=3)

    def draw_radius(self) -> None:
        self.window.create_line(self.circle.center[0], self.circle.center[1],
                                self.circle.bottom_right[0], self.circle.center[1],
                                fill='black', width=3)

    def draw_square(self) -> None:
        self.window.create_rectangle(self.circle.top_left[0], self.circle.top_left[1],
                                     self.circle.bottom_right[0], self.circle.bottom_right[1],
                                     outline='black', width=3)

    def draw_text(self) -> None:
        self.window.create_text(self.circle.center[0] + self.circle.bottom_right[0] / 8,
                                self.circle.center[1] - self.circle.bottom_right[1] / 32,
                                text=f'r = {self.circle.radius} cm', font=('Segoe UI', 18))

    def run(self):
        self.draw_circle()
        self.draw_radius()
        self.draw_text()
        self.draw_square()
        self._root.mainloop()


class Circle(object):
    def __init__(self, win_size, radius):
        self._win_size = win_size
        self.radius = radius

    @property
    def center(self) -> tuple:
        return self._win_size / 2, self._win_size / 2

    @property
    def top_left(self) -> tuple:
        return self.center[0] - self.radius, self.center[1] - self.radius

    @property
    def bottom_right(self) -> tuple:
        return self.center[0] + self.radius, self.center[1] + self.radius


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app = Application(win_size=int(sys.argv[1]), radius=int(sys.argv[2]))
    else:
        app = Application()
    app.run()
