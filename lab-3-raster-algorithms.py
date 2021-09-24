import sys
import string
from math import radians, cos, sin
import tkinter as tk


class Application(object):
    def __init__(self, win_size=800, green_px_size=10, red_px_size=20):
        self._win_size = win_size

        self.main_window = Panel(title='lab3', size=win_size, geometry='+600+0')
        self.control_window = Panel(title='control panel', size=win_size)
        self.control_window.add_element(el_type=tk.Button, el_id='start', command=self.draw_star, text='Draw')
        self.control_window.add_element(el_type=EntryWithPlaceholder, el_id='colors', text='green,red')
        self.control_window.add_element(el_type=EntryWithPlaceholder, el_id='sizes',
                                        text=f'{green_px_size},{red_px_size}')

        self.star = None

    def draw_star(self):
        self.main_window.canvas.delete('all')
        colors, sizes = self.control_window.get_inputs()

        self.star = Star(win_size=self._win_size, green_px_size=sizes[0], red_px_size=sizes[1])
        self.draw_triangle(self.star.green_triangle.points, color=colors[0], size=sizes[0])
        self.draw_triangle(self.star.red_triangle.points, color=colors[1], size=sizes[1])

    def draw_bresenham_line(self, point0, point1, color, size):
        x0, y0 = int(point0[0]), int(point0[1])
        x1, y1 = int(point1[0]), int(point1[1])
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        delta_x = x1 - x0
        delta_y = abs(y1 - y0)
        error = -delta_x / 2

        # direction == '+': y increases or is constant for any x
        # direction == '-': y decreases for any x
        direction = '+' if y0 <= y1 else '-'

        y = y0
        for x in range(x0, x1 + 1, size):
            if steep:
                self.main_window.canvas.create_rectangle(y, x, y + size if direction == '+' else y - size, x + size,
                                                         outline=color, fill=color)
            else:
                self.main_window.canvas.create_rectangle(x, y, x + size, y + size, outline=color, fill=color)

            error += delta_y
            if error > 0:
                if direction == '+':
                    y += size
                else:
                    y -= size
                error -= delta_x

    def draw_triangle(self, points, color='black', size=10):
        # side AC
        self.draw_bresenham_line(points[0], points[2], color=color, size=size)
        # side AB
        self.draw_bresenham_line(points[0], points[1], color=color, size=size)
        # side BC
        self.draw_bresenham_line(points[1], points[2], color=color, size=size)

    def run(self):
        self.main_window.root.mainloop()


class Panel(object):
    def __init__(self, title='window', size=800, geometry=None):
        self.root = tk.Tk()
        self.root.title(title)
        self._win_size = size
        if geometry:
            self.root.geometry(geometry)
        self.canvas = tk.Canvas(master=self.root, width=self._win_size, height=self._win_size,
                                borderwidth=0, highlightthickness=0, bg='white')
        self.canvas.grid()
        self.buttons = {}
        self.inputs = {}

    def add_element(self, el_type, el_id, command=None, height=2, width=20, text='Placeholder'):
        if el_type == tk.Button:
            self.buttons[el_id] = tk.Button(master=self.canvas, command=command, height=height, width=width, text=text)
            self.buttons[el_id].pack()
        elif el_type == EntryWithPlaceholder:
            self.inputs[el_id] = EntryWithPlaceholder(master=self.canvas, width=width + 5, placeholder=text)
            self.inputs[el_id].pack()
        else:
            raise Exception(f'Cannot create an element of this type: {el_type}')

    def get_inputs(self):
        inputs_data = []
        for idx, inp in self.inputs.items():
            curr_inp = []
            if inp.get():
                if idx == 'sizes':
                    curr_inp = [int(s) for s in
                                inp.get().translate({ord(c): None for c in string.whitespace}).split(',')]
                elif idx == 'colors':
                    curr_inp = inp.get().translate({ord(c): None for c in string.whitespace}).split(',')
                else:
                    raise Exception(f'Unimplemented input index: {idx}')
                # if only one parameter was provided
                if len(curr_inp) == 1:
                    curr_inp.append(curr_inp[0])
            else:
                # use default values
                if idx == 'colors':
                    curr_inp = ['green', 'red']
                elif idx == 'sizes':
                    curr_inp = [10, 20]
            inputs_data.append(curr_inp)
        return inputs_data


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, width=25, placeholder='PLACEHOLDER', color='grey'):
        super().__init__(master=master, width=width)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind('<FocusIn>', self.foc_in)
        self.bind('<FocusOut>', self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


class Star(object):
    def __init__(self, win_size, green_px_size, red_px_size):
        side = int((win_size * pow(base=3, exp=0.5)) / 2)
        while side % green_px_size > 0 and side % red_px_size > 0:
            side -= 1
        self.green_triangle = Triangle(side=side, color='green', px_size=green_px_size, rot=False, win_size=win_size)
        self.red_triangle = Triangle(side=side, color='red', px_size=red_px_size, rot=True, win_size=win_size)


class Triangle(object):
    def __init__(self, side, color='black', px_size=10, rot=False, win_size=800):
        self._win_size = win_size
        self._points = None

        self.side = side
        self.color = color
        self.px_size = px_size

        self.R = self.side / pow(base=3, exp=0.5)
        self.r = self.side / (2 * pow(base=3, exp=0.5))

        self.a = [(self._win_size - self.side) / 2, self._win_size / 2 + self.R / 2]
        self.b = [self._win_size / 2, (self._win_size - 2 * self.R) / 2]
        self.c = [(self._win_size + self.side) / 2, self._win_size / 2 + self.R / 2]
        self.o = [self._win_size / 2, self.a[1] - self.r]

        if rot:
            self.points = self.rotate()

    @property
    def points(self) -> list:
        return [self.a, self.b, self.c]

    @points.setter
    def points(self, points: list):
        self.a = points[0]
        self.b = points[1]
        self.c = points[2]

    def rotate(self, angle=180):
        angle = radians(angle)
        x_center, y_center = self.o
        new_points = []
        for x_old, y_old in self.points:
            x_old -= x_center
            y_old -= y_center
            x_new = x_old * cos(angle) - y_old * sin(angle)
            y_new = x_old * sin(angle) + y_old * cos(angle)
            new_points.append([x_new + x_center, y_new + y_center])
        return new_points


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app = Application(win_size=int(sys.argv[1]), green_px_size=int(sys.argv[1]), red_px_size=int(sys.argv[2]))
    else:
        app = Application()
    app.run()
