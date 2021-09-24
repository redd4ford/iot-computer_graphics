import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys
from math import sin, cos, tan


class Application(object):
    def __init__(self, win_size=500, min_t=1, max_t=2, step=0.01):
        self._root = tk.Tk()
        self._root.title('lab2')
        self._root.geometry(f'{win_size}x{win_size}')
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self._canvas = FigureCanvasTkAgg(self.fig, master=self._root)
        self._toolbar = NavigationToolbar2Tk(self._canvas, self._root)

        self.min_t = min_t
        self.max_t = max_t
        self.step = step
        self.x_coordinates = []
        self.y_coordinates = []

    @staticmethod
    def x(t):
        return 0.3 * tan(t**4) - 0.15 * sin(t)

    @staticmethod
    def y(t):
        return 0.3 * (tan(t**4))**(-1) + 0.15 * cos(t)

    def plot(self):
        current_t = self.min_t
        while current_t <= self.max_t:
            print(current_t, Application.x(current_t), Application.y(current_t))
            self.x_coordinates.append(Application.x(current_t))
            self.y_coordinates.append(Application.y(current_t))
            current_t += self.step

        plot1 = self.fig.add_subplot(111)
        plot1.plot(self.x_coordinates, self.y_coordinates)
        self._canvas.draw()
        self._canvas.get_tk_widget().pack()
        self._toolbar.update()
        self._canvas.get_tk_widget().pack()
        self._root.mainloop()

    def run(self):
        self.plot()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app = Application(min_t=int(sys.argv[1]), max_t=int(sys.argv[2]), step=int(sys.argv[3]))
    else:
        app = Application()
    app.run()
