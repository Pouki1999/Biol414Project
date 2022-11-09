from tkinter import Tk, BOTH, Frame, Canvas
import numpy as np
import math


"""
class Ant:

    def __init__(self):
        
"""


class Environment(Frame):

    def __init__(self):
        super().__init__()
        self.canvas = Canvas(self)
        self.initUI()
        self.obstacles = []
        self.limits = [1000, 400]
        self.bind("<KeyPress>", self.keydown)
        self.bind("<KeyRelease>", self.keyup)
        self.curr_pt = (0.0, 0.0)

        self.pack()
        self.focus_set()

    def initUI(self):
        self.master.title("Random Walk Experiment")
        self.pack(fill=BOTH, expand=1)

        self.canvas.create_line(15, 25, 200, 25)
        self.canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        self.canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)

        self.canvas.pack(fill=BOTH, expand=1)

    def keyup(self, e):
        print('up, add new point', e.char)

    def keydown(self, e):
        print('down', e.char)
        self.random_walk_next_step(4)

    def random_walk_next_step(self, step):
        while True:
            angle = np.random.uniform(0.0, 2 * math.pi, size=None)
            new_x = self.curr_pt[0] + int(step * step * math.cos(angle))
            new_y = self.curr_pt[1] + int(step * step * math.sin(angle))
            if 0 <= new_x <= self.limits[0] and 0 <= new_y <= self.limits[1]:
                break
        self.canvas.create_line(self.curr_pt[0], self.curr_pt[1], new_x, new_y)
        self.curr_pt = [new_x, new_y]


def main():
    root = Tk()
    env = Environment()
    limits_string = str(env.limits[0]) + "x" + str(env.limits[1])
    root.geometry(limits_string)
    root.mainloop()


if __name__ == '__main__':
    main()
