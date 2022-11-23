from tkinter import Tk, BOTH, Frame, Canvas, Button
import numpy as np
import math

"""
class Ant:
    def __init__(self):
        pass
"""

class Environment(Frame):
    def __init__(self):
        super().__init__()
        self.master.title("Random Walk Experiment")
        self.canvas = Canvas(self)
        self.obstacles = [(100, 300, 400, 500), (450, 50, 550, 500), (700, 100, 950, 450)]
        self.food_sources = [(50, 100), (600, 500), (900, 40)]
        self.nest_pos = (300.0, 250.0)
        self.curr_pos = self.nest_pos
        self.limits = (1000, 600)
        self.initUI()

        self.pack()
        self.focus_set()

        self.bind("<KeyPress>", self.keydown)
        self.bind("<KeyRelease>", self.keyup)

        startButton = Button(self, text="Start", command=self.initUI)
        startButton.place(x=0, y=0)

    def initUI(self):
        self.canvas.delete("all")
        self.pack(fill=BOTH, expand=1)
        """
        self.canvas.create_line(15, 25, 200, 25)
        self.canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        self.canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
        """
        self.curr_pos = self.nest_pos
        self.canvas.create_oval(self.nest_pos[0] - 6, self.nest_pos[1] - 6, self.nest_pos[0] + 6, self.nest_pos[1] + 6,
                                fill="#fb0")

        for o in self.obstacles:
            self.canvas.create_rectangle(o[0], o[1], o[2], o[3])

        for f in self.food_sources:
            self.canvas.create_oval(f[0] - 3, f[1] - 3, f[0] + 3, f[1] + 3)

        self.canvas.pack(fill=BOTH, expand=1)

        self.curr_pos = self.nest_pos



    def keyup(self, e):
        pass

    def keydown(self, e):
        self.random_walk_next_step(3)

    def random_walk_next_step(self, step):
        while True:
            angle = np.random.uniform(0.0, 2 * math.pi, size=None)
            new_x = self.curr_pos[0] + int(step * step * math.cos(angle) + 0.5)
            new_y = self.curr_pos[1] + int(step * step * math.sin(angle) + 0.5)
            bad = False
            for o in self.obstacles:
                if inRect((new_x, new_y), o) or lineHitsRect((self.curr_pos[0], self.curr_pos[1]), (new_x, new_y), o):
                    bad = True
            if bad:
                continue
            if 0 <= new_x <= self.limits[0] and 0 <= new_y <= self.limits[1]:
                break
        self.canvas.create_line(self.curr_pos[0], self.curr_pos[1], new_x, new_y)
        self.curr_pos = (new_x, new_y)


def inRect(p, rect):
    """ Return 1 in p is inside rect, dilated by dilation (for edge cases). """
    if rect[2] >= p[0] >= rect[0] and rect[3] >= p[1] >= rect[1]:
        return True
    else:
        return False


def lineHitsRect(p1, p2, r):
    if (p1[0] - p2[0]) == 0:
        m = 100000
    else:
        m = (p1[1] - p2[1])/(p1[0] - p2[0])
    b = p1[1] - m*p1[0]
    y1 = m*r[0] + b
    y2 = m*r[2] + b
    if m != 0:
        x1 = (r[1] - b) / m
        x2 = (r[3] - b) / m
    else:
        x1 = 100000
        x2 = 100000

    if (p1[0] <= r[0] <= p2[0] or p2[0] <= r[0] <= p1[0]) and (r[1] <= y1 <= r[3]):
        return True
    if (p1[0] <= r[2] <= p2[0] or p2[0] <= r[2] <= p1[0]) and (r[1] <= y2 <= r[3]):
        return True
    if (r[0] <= x1 <= r[2]) and (p1[1] <= r[1] <= p2[1] or p2[1] <= r[1] <= p1[1]):
        return True
    if (r[0] <= x2 <= r[2]) and (p1[1] <= r[3] <= p2[1] or p2[1] <= r[3] <= p1[1]):
        return True
    return False

def main():
    root = Tk()
    env = Environment()
    limits_string = str(env.limits[0]) + "x" + str(env.limits[1])
    root.geometry(limits_string)
    root.mainloop()
    print('we are in the main loop')


if __name__ == '__main__':
    main()
