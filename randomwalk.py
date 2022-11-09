from tkinter import Tk, BOTH, Frame, Canvas
import numpy as np
import math


"""
class Ant:

    def __init__(self):
        
"""


def random_walk_next_step(obstacles, curr, limits, canvas, step):
    while True:
        angle = np.random.uniform(0.0, 2*math.pi, size=None)
        new_x = curr[0] + int(step*step*math.cos(angle))
        new_y = curr[1] + int(step*step*math.sin(angle))
        if 0 <= new_x <= limits[0] and 0 <= new_y <= limits[1]:
            break
    canvas.create_line(curr[0], curr[1], new_x, new_y)

    return [new_x, new_y]


class Environment(Frame):

    def __init__(self):
        super().__init__()
        self.canvas = Canvas(self)
        self.initUI()

    def initUI(self):
        self.master.title("Random Walk Experiment")
        self.pack(fill=BOTH, expand=1)
        """
        self.canvas.create_line(15, 25, 200, 25)
        self.canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        self.canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
        """
        self.canvas.pack(fill=BOTH, expand=1)


def main():

    root = Tk()
    env = Environment()
    root.geometry("400x250+300+300")
    curr = (0.0, 0.0)
    limits = [400, 250]
    for i in range(1000):
        print(i)
        curr = random_walk_next_step([], curr, limits, env.canvas, 4)
    root.mainloop()



if __name__ == '__main__':
    main()
