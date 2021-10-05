from math import sin, cos, radians, hypot
import tkinter as tk
import sys


class CircularPath(object):
    def __init__(self, x: int, y: int, radius: float):
        self.xc = x
        self.yc = y
        self.radius = radius

    def bounds(self) -> tuple:
        return (self.xc + self.radius * cos(radians(0)),
                self.yc + self.radius * sin(radians(270)),
                self.xc + self.radius * cos(radians(180)),
                self.yc + self.radius * sin(radians(90)))


class Square(object):
    def __init__(self, xc: int, yc: int, side: int):
        self.xc = xc
        self.yc = yc
        self.side = side
        self.R = (side * pow(base=2, exp=0.5)) / 2
        self.r = side / 2

        self._a = [self.xc - self.r, self.yc - self.r]   # A -- -- B
        self._b = [self.xc + self.r, self.yc - self.r]   # |       |
        self._c = [self.xc + self.r, self.yc + self.r]   # |       |
        self._d = [self.xc - self.r, self.yc + self.r]   # D -- -- C

    @property
    def center(self) -> tuple:
        return self.xc, self.yc

    @center.setter
    def center(self, values: list[int]) -> None:
        self.xc, self.yc = values

    def coords(self) -> tuple:
        return self._a, self._b, self._c, self._d

    def update_coords(self, a=None, b=None, c=None, d=None) -> None:
        if a and b and c and d:
            self._a, self._b, self._c, self._d = a, b, c, d
        else:
            self._a = [self.xc - self.r, self.yc - self.r]
            self._b = [self.xc + self.r, self.yc - self.r]
            self._c = [self.xc + self.r, self.yc + self.r]
            self._d = [self.xc - self.r, self.yc + self.r]


class Line(object):
    def __init__(self, x0: int, y0: int, x1: int, y1: int):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def coords(self) -> tuple:
        return [self.x0, self.y0], [self.x1, self.y1]


class Application(object):
    DELAY = 100
    CIRCULAR_PATH_INCR = 5

    def __init__(self, win_size=400, side=32, radius=70):
        self._win_size = win_size
        self._win_center = self._win_size // 2

        self.angle = Application.CIRCULAR_PATH_INCR

        self.root = tk.Tk()
        self.root.title('lab4')

        self.canvas = tk.Canvas(self.root, bg='black', height=self._win_size, width=self._win_size)
        self.canvas.pack()

        self.circle_obj = CircularPath(x=self._win_center, y=self._win_center, radius=radius)
        self.square_obj = Square(xc=self._win_center + radius, yc=self._win_center, side=side)
        self.line_obj = Line(x0=self._win_center, y0=self._win_center,
                             x1=self._win_center + radius, y1=self._win_center)

    def update_position(self, canvas: tk.Canvas, square_id: int, square_obj: Square,
                        line_id: int, line_obj: Line, path_iter) -> None:
        # iterate path and set new position
        self.square_obj.center = next(path_iter)
        self.angle += Application.CIRCULAR_PATH_INCR

        # radius movement
        # (x0, y0) is the center of the circular path so it's immutable.
        # (x1, y1) is the point on the circle that coincides with the square center
        self.line_obj.x1, self.line_obj.y1 = self.square_obj.center
        # re-render the line
        self.canvas.delete(line_id)
        line_id = self.canvas.create_line(self.line_obj.coords(), fill='white', width=1)

        # rectangle rotation
        updated_coords = self.rotate(self.square_obj.coords(), self.square_obj.center, angle=self.angle)
        # calculate the new position relatively to the center
        self.square_obj.update_coords(updated_coords)
        # re-render the rectangle
        self.canvas.delete(square_id)
        # rectangle movement
        square_id = self.canvas.create_polygon(updated_coords, outline='white', width=1)

        # repeat after delay
        canvas.after(Application.DELAY, self.update_position, self.canvas,
                     square_id, square_obj, line_id, line_obj, path_iter)

    @staticmethod
    def circular_path(x: int, y: int, radius: float, delta_ang: int, start_ang=0):
        # generate coords of a circular path every delta angle
        ang = start_ang % 360
        while True:
            yield x + radius * cos(radians(ang)), y + radius * sin(radians(ang))
            ang = (ang + delta_ang) % 360

    @staticmethod
    def rotate(coords: tuple, center: tuple, angle=CIRCULAR_PATH_INCR) -> tuple:
        angle = radians(angle)
        x_center = center[0]
        y_center = center[1]
        for point in coords:
            x_val = point[0] - x_center
            y_val = point[1] - y_center
            point[0] = x_val * cos(angle) - y_val * sin(angle) + x_center
            point[1] = x_val * sin(angle) + y_val * cos(angle) + y_center
        return coords

    def run(self) -> None:
        # draw path
        self.canvas.create_oval(self.circle_obj.bounds(), outline='grey', width=1, dash=(5, 5))
        # draw initial square
        square = self.canvas.create_polygon(self.square_obj.coords(), outline='white', width=0)
        # draw initial radius
        radius = self.canvas.create_line(self.line_obj.coords(), fill='white', width=1)

        # get multidimensional Euclidean distance from the origin to a point
        orbital_radius = hypot(self.circle_obj.xc - self.square_obj.xc,
                               self.circle_obj.yc - self.square_obj.yc)

        # prime generator
        path_iter = self.circular_path(self.circle_obj.xc, self.circle_obj.yc,
                                       orbital_radius, Application.CIRCULAR_PATH_INCR)
        next(path_iter)

        self.root.after(Application.DELAY, self.update_position, self.canvas,
                        square, self.square_obj, radius, self.line_obj, path_iter)
        self.root.mainloop()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app = Application(win_size=int(sys.argv[1]), side=int(sys.argv[2]), radius=int(sys.argv[3]))
    else:
        app = Application()
    app.run()
