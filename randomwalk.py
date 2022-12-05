import random
from tkinter import Tk, BOTH, Frame, Canvas, Button
import numpy as np
import math
from matplotlib import pyplot as plt

class Ant:
    def __init__(self, nest_pos, biased):
        self.nest_pos = nest_pos
        self.curr_pos = self.nest_pos
        self.orientation = 0.0
        self.noise = 5
        self.biased = biased
        self.step_size = 10

        self.carries_food = False

        self.curr_vector = (0.0, 0.0)
        self.vector_memory = []
        self.already_visited_in_run = set()

        self.curr_destination = None
        self.give_up_counter = 0
        self.give_up_threshold = 150

    def start_pos(self):
        self.curr_pos = self.nest_pos
        self.orientation = 0.0

        self.carries_food = False

        self.curr_vector = (0.0, 0.0)
        self.vector_memory = []
        self.already_visited_in_run = set()

        self.curr_destination = None
        self.give_up_counter = 0
        self.give_up_threshold = 20

    def change_pos(self, x, y):
        self.curr_pos = (x, y)

    def update_curr_vector(self):
        heading = self.orientation
        dx = int(self.step_size*math.cos(heading) + 0.5)
        dy = int(self.step_size*math.sin(heading) + 0.5)
        self.curr_vector = (self.curr_vector[0] - dx, self.curr_vector[1] - dy)

    def get_a_destination(self):
        if len(self.vector_memory) > len(self.already_visited_in_run):
            while True:
                i = random.randrange(len(self.vector_memory))
                if i not in self.already_visited_in_run:
                    print('new destination:', self.vector_memory[i])
                    self.curr_destination = (self.vector_memory[i][2][0], self.vector_memory[i][2][1])
                    break

        else:
            print('No destination')
            self.curr_destination = None

    def add_vector_to_memory(self, i, nature):
        self.vector_memory.append((nature, i, (self.curr_vector[0], self.curr_vector[1])))
        print(self.vector_memory)


class Environment(Frame):
    def __init__(self):
        super().__init__()
        self.master.title("Path Integration Experiment")
        self.canvas = Canvas(self)
        self.obstacles = [(100, 300, 200, 390), (100, 410, 200, 500), (300, 300, 400, 500),
                          (450, 50, 550, 250), (500, 300, 550, 550),
                          (700, 100, 815, 260), (835, 290, 950, 450),
                          (100, 70, 140, 170), (220, 40, 303, 90), (307, 40, 390, 90),
                          (715, 316, 800, 380), (840, 30, 880, 170)]
        self.food_sources = [(50, 340), (600, 500), (900, 40), (120, 550), (815, 290), (900, 500), (500, 25),
                             (100, 30), (980, 580), (350, 560), (305, 20)]
        self.food_amounts = [2, 3, 4, 2, 3, 4, 3, 2, 4, 3, 5]
        #self.landmarks = [(270, 70), (400, 550), (900, 200), (700, 450)]
        #self.landmark_radius = 20
        self.original_food_amounts = [2, 3, 4, 2, 3, 4, 3, 2, 4, 3, 5]
        self.food_labels = []
        self.food_scalling = 500
        self.food_range = 20
        self.food_radius = 10
        self.at_std = 3
        self.nest_pos = (300, 250)
        self.nest_hunger = -1
        self.initial_nest_hunger = -1
        self.nest_label = None
        self.nest_scalling = 500
        self.nest_range = 20
        self.nest_radius = 14
        self.limits = (1000, 600)
        self.ant = Ant(self.nest_pos, True)
        self.initUI()
        self.time = 1

        self.time_steps = []
        self.distance_list = []
        self.nest_hunger_list = []
        self.max_dist = math.sqrt(self.limits[0]**2 + self.limits[1]**2)

        self.bind("<KeyPress>", self.keydown)
        self.bind("<KeyRelease>", self.keyup)

        startButton = Button(self, text="Restart", command=self.initUI)
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
        self.time = 0
        self.ant.start_pos()
        for i, f in enumerate(self.original_food_amounts):
            self.food_amounts[i] = f
        self.nest_hunger = self.initial_nest_hunger

        self.canvas.create_oval(self.nest_pos[0] - self.nest_radius, self.nest_pos[1] - self.nest_radius,
                                self.nest_pos[0] + self.nest_radius, self.nest_pos[1] + self.nest_radius,
                                fill="red2")
        self.nest_label = self.canvas.create_text(self.nest_pos[0], self.nest_pos[1], text=str(self.nest_hunger), fill="black", font='Helvetica 15 bold')

        for o in self.obstacles:
            self.canvas.create_rectangle(o[0], o[1], o[2], o[3])

        for a, f in zip(self.food_amounts, self.food_sources):
            self.canvas.create_oval(f[0] - self.food_radius, f[1] - self.food_radius,
                                    f[0] + self.food_radius, f[1] + self.food_radius)
            self.food_labels.append(self.canvas.create_text(f[0], f[1], text=str(a), fill="black",
                                                            font='Helvetica 15 bold'))
        """
        for l in self.landmarks:
            self.canvas.create_oval(l[0] - self.landmark_radius, l[1] - self.landmark_radius, l[0] + self.landmark_radius, l[1] + self.landmark_radius)
        """

        self.canvas.pack(fill=BOTH, expand=1)

    def keyup(self, e):
        pass

    def keydown(self, e):
        #if self.ant.biased:
        self.biased_walk_next_step()
        """
        else:
            self.random_walk_next_step(self.ant.step_size)
        """

    def compute_exploration_vector(self):
        env_x_derivative = 0.0
        env_y_derivative = 0.0
        x = self.ant.curr_pos[0]
        y = self.ant.curr_pos[1]
        # compute attraction from food sources
        for pos, value in zip(self.food_sources, self.food_amounts):
            if value == 0:
                continue
            else:
                exponent = math.exp(-((x - pos[0])**2 + (y - pos[1])**2)/(2*value*self.food_range*(self.at_std**2)))
                env_x_derivative += (-value*self.food_scalling/((self.at_std**4)*4*math.pi))*exponent*2*(x-pos[0])
                env_y_derivative += (-value*self.food_scalling/((self.at_std**4)*4*math.pi))*exponent*2*(y-pos[1])
            #print('distance:', math.sqrt((self.ant.curr_pos[0] - pos[0]) ** 2 + (self.ant.curr_pos[1] - pos[1]) ** 2))
        print(env_x_derivative, env_y_derivative)
        # compute repulsion from nest
        exponent = math.exp(
            -((x - self.nest_pos[0]) ** 2 + (y - self.nest_pos[1]) ** 2) / (2 * self.nest_range * (self.at_std ** 2)))
        env_x_derivative -= (-self.nest_scalling / ((self.at_std ** 4) * 4 * math.pi)) * exponent * 2 * (
                    x - self.nest_pos[0])
        env_y_derivative -= (-self.nest_scalling / ((self.at_std ** 4) * 4 * math.pi)) * exponent * 2 * (
                    y - self.nest_pos[1])
        #print('distance:', math.sqrt((self.ant.curr_pos[0] - self.nest_pos[0]) ** 2 + (self.ant.curr_pos[1] - self.nest_pos[1]) ** 2))
        print(env_x_derivative, env_y_derivative)

        print(self.ant.curr_destination)
        print(self.ant.curr_vector)
        if self.ant.curr_destination is not None:
            env_x_derivative += self.ant.curr_vector[0] - self.ant.curr_destination[0]
            env_y_derivative += self.ant.curr_vector[1] - self.ant.curr_destination[1]

        return env_x_derivative, env_y_derivative

    def compute_homing_vector(self):
        x = self.ant.curr_pos[0]
        y = self.ant.curr_pos[1]
        # compute attraction from nest
        env_x_derivative = 0.0
        env_y_derivative = 0.0
        exponent = math.exp(-((x - self.nest_pos[0]) ** 2 + (y - self.nest_pos[1]) ** 2) / (
                2 * self.nest_range * (self.at_std ** 2)))

        env_x_derivative += (self.nest_scalling / ((self.at_std ** 4) * 4 * math.pi)) * exponent * 2 * (
                    x - self.nest_pos[0])
        env_y_derivative += (self.nest_scalling / ((self.at_std ** 4) * 4 * math.pi)) * exponent * 2 * (
                    y - self.nest_pos[1])
        print(self.ant.curr_destination)
        print(self.ant.curr_vector)
        env_x_derivative += self.ant.curr_vector[0]
        env_y_derivative += self.ant.curr_vector[1]

        return env_x_derivative, env_y_derivative

    def biased_walk_next_step(self):
        print('time', self.time)
        if self.ant.carries_food:
            print('homing')
            vector = self.compute_homing_vector()
        else:
            print('exploration')
            vector = self.compute_exploration_vector()

        print(vector)
        c = 0  # iteration counter
        n = 1 # noise increase
        lower_bound = self.ant.orientation - (math.pi / 4)
        upper_bound = self.ant.orientation + (math.pi / 4)
        while True:
            c += 1
            noise_angle = np.random.uniform(lower_bound, upper_bound, size=None)
            noise_x = n*self.ant.noise*math.cos(noise_angle)
            noise_y = n*self.ant.noise*math.sin(noise_angle)
            #print(noise_x, noise_y)
            comb_vector = (vector[0] + noise_x, vector[1] + noise_y)
            scale_fact = self.ant.step_size / math.sqrt(comb_vector[0] * comb_vector[0] + comb_vector[1] * comb_vector[1])
            scaled_vector = (scale_fact * comb_vector[0], scale_fact * comb_vector[1])
            new_x = self.ant.curr_pos[0] + int(scaled_vector[0] + 0.5)
            new_y = self.ant.curr_pos[1] + int(scaled_vector[1] + 0.5)
            #print(scaled_vector)
            bad = False
            for o in self.obstacles:
                if inRect((new_x, new_y), o) or lineHitsRect(self.ant.curr_pos, (new_x, new_y), o):
                    bad = True
                    print('in rect')
            if not (0 <= new_x <= self.limits[0] and 0 <= new_y <= self.limits[1]):
                bad = True
                print('out of frame')
            if bad:
                if c == 10:
                    lower_bound = 0.0
                    upper_bound = 2*math.pi
                    self.ant.give_up_counter += 1
                    if self.ant.give_up_counter == self.ant.give_up_threshold:
                        self.ant.curr_destination = None
                        self.ant.give_up_counter = 0
                if c % 10 == 0:
                    n += 1
            else:
                break
        #print(new_x, new_y)
        print(scaled_vector)
        self.ant.orientation = math.atan(scaled_vector[1]/scaled_vector[0])
        if scaled_vector[0] < 0:
            if scaled_vector[1] > 0:
                self.ant.orientation += math.pi
            else:
                self.ant.orientation -= math.pi
        #print(self.ant.orientation)
        self.canvas.create_line(self.ant.curr_pos[0], self.ant.curr_pos[1], new_x, new_y, dash=(1, 1))
        self.ant.curr_pos = (new_x, new_y)

        self.ant.update_curr_vector()
        self.check_position()

        self.time_steps.append(self.time)
        self.nest_hunger_list.append(self.nest_hunger)
        self.distance_list.append(math.sqrt(self.ant.curr_vector[0]**2 + self.ant.curr_vector[1]**2)/self.max_dist)

        self.time += 1

        if self.time == 1000:
            print(self.time_steps)
            print(self.nest_hunger_list)
            print(self.distance_list)
            plt.plot(self.time_steps, self.distance_list, 'r')  # plotting distance from nest
            plt.plot(self.time_steps, self.nest_hunger_list, 'b')  # plotting nest hunger
            plt.show()

    def check_position(self):
        # For food sources
        for i, f in enumerate(self.food_sources):
            distance = math.sqrt((self.ant.curr_pos[0] - f[0])*(self.ant.curr_pos[0] - f[0]) +
                                 (self.ant.curr_pos[1] - f[1])*(self.ant.curr_pos[1] - f[1]))
            if distance <= self.food_radius:
                print('Found a food source!')
                self.got_to_food_source(i)
        """
        # For landmarks
        for i, l in enumerate(self.landmarks):
            distance = math.sqrt((self.ant.curr_pos[0] - l[0]) * (self.ant.curr_pos[0] - l[0]) +
                                 (self.ant.curr_pos[1] - l[1]) * (self.ant.curr_pos[1] - l[1]))
            if distance <= self.landmark_radius:
                print('Found a landmark!')
                self.got_to_landmark(i)
        """
        # For nest
        distance = math.sqrt((self.ant.curr_pos[0] - self.nest_pos[0]) * (self.ant.curr_pos[0] - self.nest_pos[0]) +
                             (self.ant.curr_pos[1] - self.nest_pos[1]) * (self.ant.curr_pos[1] - self.nest_pos[1]))
        if distance <= self.nest_radius and self.ant.carries_food:
            print('Got to the nest!')
            self.got_to_nest()

        if self.ant.curr_destination is not None:
            if math.sqrt((self.ant.curr_vector[0] - self.ant.curr_destination[0])**2 + (self.ant.curr_vector[1] - self.ant.curr_destination[1])**2) < self.ant.step_size:
                self.ant.curr_destination = None

        # ----Increase hunger of the nest as time passes----
        if self.time % 300 == 0:
            self.nest_hunger -= 1
            self.canvas.itemconfig(self.nest_label, text=str(self.nest_hunger))

        # ----Increase amount of food at sources as time passes----
        if self.time % 300 == 0:
            for i in range(len(self.food_amounts)):
                will_food_appear = random.randrange(5)
                if will_food_appear == 0:
                    self.food_amounts[i] += 1

    def got_to_nest(self):
        self.nest_hunger += 1
        self.canvas.itemconfig(self.nest_label, text=str(self.nest_hunger))
        self.ant.carries_food = False
        self.ant.already_visited_in_run = set()
        self.ant.get_a_destination()

    def got_to_food_source(self, i):
        if self.food_amounts[i] > 0 and not self.ant.carries_food:
            self.food_amounts[i] -= 1
            self.canvas.itemconfig(self.food_labels[i], text=str(self.food_amounts[i]))
            self.ant.carries_food = True
            self.ant.curr_destination = None

        if self.food_amounts[i] == 0 and not self.ant.carries_food:
            self.ant.already_visited_in_run.add(i)
            self.ant.get_a_destination()

        already_known = False
        for v in self.ant.vector_memory:
            if v[1] == i and v[0] == 'food_source':
                already_known = True
        if not already_known:
            self.ant.add_vector_to_memory(i, 'food_source')
    """
    def got_to_landmark(self, i):
        already_known = False
        for v in self.ant.vector_memory:
            if v[1] == i and v[0] == 'landmark':
                already_known = True
        if not already_known:
            self.ant.add_vector_to_memory(i, 'landmark')
    """
    """
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
    """


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
