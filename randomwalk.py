from tkinter import Tk, BOTH, Frame, Canvas, Button
import numpy as np
import math
import time


class Ant:
    def __init__(self, nest_pos, biased):
        self.nest_pos = nest_pos
        self.curr_pos = self.nest_pos
        self.orientation = 0.0
        self.pers_std = 3
        self.pers_range = 20
        self.noise = 0.1
        self.biased = biased
        self.step_size = 4

    def start_pos(self):
        self.curr_pos = self.nest_pos


class Environment(Frame):
    def __init__(self):
        super().__init__()
        self.master.title("Random Walk Experiment")
        self.canvas = Canvas(self)
        self.obstacles = [(100, 300, 400, 500), (450, 50, 550, 500), (700, 100, 950, 450)]
        self.food_sources = [(50, 100), (600, 500), (900, 40)]
        self.food_amounts = [5, 5, 7]
        self.original_food_amounts = [5, 5, 7]
        self.food_labels = []
        self.food_range = 20
        self.at_std = 3
        self.nest_pos = (300, 250)
        self.limits = (1000, 600)
        self.ant = Ant(self.nest_pos, True)
        self.initUI()
        self.time = 1

        self.bind("<KeyPress>", self.keydown)
        self.bind("<KeyRelease>", self.keyup)

        startButton = Button(self, text="Start", command=self.initUI)
        """
        automaticButton = Button(self, text="Automatic", command=self.automatic_walk)
        automaticButton.place(x=100, y=0)
        """
        startButton.place(x=0, y=0)

        self.pack()
        self.focus_set()

    def initUI(self):
        self.canvas.delete("all")
        self.pack(fill=BOTH, expand=1)
        """
        self.canvas.create_line(15, 25, 200, 25)
        self.canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        self.canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
        """
        self.canvas.create_oval(self.nest_pos[0] - 14, self.nest_pos[1] - 14, self.nest_pos[0] + 14, self.nest_pos[1] + 14,
                                fill="red2")

        for o in self.obstacles:
            self.canvas.create_rectangle(o[0], o[1], o[2], o[3])

        for a, f in zip(self.food_amounts, self.food_sources):
            self.canvas.create_oval(f[0] - 10, f[1] - 10, f[0] + 10, f[1] + 10)
            self.food_labels.append(self.canvas.create_text(f[0], f[1], text=str(a), fill="black", font='Helvetica 15 bold'))

        self.canvas.pack(fill=BOTH, expand=1)

        self.ant.start_pos()
        for i, f in enumerate(self.original_food_amounts):
            self.food_amounts[i] = f
        self.time = 0

    def keyup(self, e):
        pass

    def keydown(self, e):
        if self.ant.biased:
            self.biased_walk_next_step(self.ant.step_size)
        else:
            self.random_walk_next_step(self.ant.step_size)
    """
    def automatic_walk(self):
        for i in range(1000):
            print(i)
            self.after(50, self.biased_walk_next_step(self.ant.step_size))
    """
    def compute_grad(self):
        env_x_derivative = 0
        env_y_derivative = 0
        x = self.ant.curr_pos[0]
        y = self.ant.curr_pos[1]
        for pos, value in zip(self.food_sources, self.food_amounts):
            if value == 0:
                continue
            else:
                exponent = math.exp(-((x - pos[0])**2 + (y - pos[1]))/(2*value*self.food_range*(self.at_std**2)))
                env_x_derivative += (-value/((self.at_std**4)*4*math.pi))*exponent*2*(x-pos[0])
                env_y_derivative += (-value/((self.at_std**4)*4*math.pi))*exponent*2*(y-pos[1])

        for o in self.obstacles:
            pass

        perception = (1/((self.ant.pers_std**2)*2*math.pi))

        return env_x_derivative*perception, env_y_derivative*perception

    def biased_walk_next_step(self, step_size):
        grad = self.compute_grad()
        print(self.time)
        print(grad)
        c = 0  # iteration counter
        n = 1  # factor increasing noise
        while True:
            c += 1
            noise_x = np.random.uniform(-self.ant.noise * n, self.ant.noise * n, size=None)
            noise_y = np.random.uniform(-self.ant.noise * n, self.ant.noise * n, size=None)
            print(noise_x, noise_y)
            comb_vector = (grad[0] + noise_x, grad[1] + noise_y)
            scale_fact = step_size / math.sqrt(comb_vector[0] * comb_vector[0] + comb_vector[1] * comb_vector[1])
            scaled_grad = (scale_fact * comb_vector[0], scale_fact * comb_vector[1])
            new_x = self.ant.curr_pos[0] + int(scaled_grad[0] + noise_x + 0.5)
            new_y = self.ant.curr_pos[1] + int(scaled_grad[1] + noise_y + 0.5)
            print(scaled_grad)
            bad = False
            for o in self.obstacles:
                if inRect((new_x, new_y), o) or lineHitsRect(self.ant.curr_pos, (new_x, new_y), o):
                    bad = True
            if not (0 <= new_x <= self.limits[0] and 0 <= new_y <= self.limits[1]):
                bad = True
            if bad:
                if c % 10 == 0:
                    n += 1  # increase noise if ant get stuck
            else:
                break

        self.canvas.create_line(self.ant.curr_pos[0], self.ant.curr_pos[1], new_x, new_y, dash=(1, 1))
        self.ant.curr_pos = (new_x, new_y)
        self.ant.orientation = 0
        self.update_state_of_food()
        self.time += 1

    def random_walk_next_step(self, step_size):
        while True:
            angle = np.random.uniform(0.0, 2 * math.pi, size=None)
            new_x = self.ant.curr_pos[0] + int(step_size * step_size * math.cos(angle) + 0.5)
            new_y = self.ant.curr_pos[1] + int(step_size * step_size * math.sin(angle) + 0.5)
            bad = False
            for o in self.obstacles:
                if inRect((new_x, new_y), o) or lineHitsRect((self.ant.curr_pos[0], self.ant.curr_pos[1]), (new_x, new_y), o):
                    bad = True
                    print('in')
            if bad:
                continue
            if 0 <= new_x <= self.limits[0] and 0 <= new_y <= self.limits[1]:
                break
        self.canvas.create_line(self.ant.curr_pos[0], self.ant.curr_pos[1], new_x, new_y)
        self.ant.curr_pos = (new_x, new_y)

    def update_state_of_food(self):
        for i, f in enumerate(self.food_sources):
            distance = math.sqrt((self.ant.curr_pos[0] - f[0])*(self.ant.curr_pos[0] - f[0]) +
                                 (self.ant.curr_pos[1] - f[1])*(self.ant.curr_pos[1] - f[1]))
            if distance < 5 and self.food_amounts[i] > 0:
                self.food_amounts[i] -= 1
                self.canvas.itemconfig(self.food_labels[i], text=str(self.food_amounts[i]))
        print(self.food_amounts)
        if self.time % 500 == 0:
            for i in range(len(self.food_amounts)):
                self.food_amounts[i] += 1

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


if __name__ == '__main__':
    main()
