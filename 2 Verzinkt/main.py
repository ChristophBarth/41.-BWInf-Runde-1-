import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import random as rd
from matplotlib.colors import LinearSegmentedColormap
import copy

custom_cmap = LinearSegmentedColormap.from_list("custom", ["white", "black", "red"])

WIDTH = 100
HEIGHT = 100
seed_num = 3

speed_min = 2
speed_max = 3

spawn_prob = 5000

n_vector = np.array([0, 1])

lightness = 2.5


def get_color_value_from_growth_speed(x_pos, y_pos, x_neg, y_neg):
    growth_vector = np.array([x_pos - x_neg, y_pos - y_neg])
    growth_vector_length = np.sqrt(growth_vector[0] ** 2 + growth_vector[1] ** 2)

    if growth_vector_length == 0: return 1/lightness
    # check for null vector in growth vector, as this would throw an error! no angle with null_vector possible

    angle = np.arccos((np.dot(n_vector, growth_vector)) / (1 * growth_vector_length))
    return angle / (lightness*np.pi)


class Seed:
    def __init__(self):
        self.x_pos_speed = rd.randint(speed_min, speed_max)
        self.y_pos_speed = rd.randint(speed_min, speed_max)
        self.x_neg_speed = rd.randint(speed_min, speed_max)
        self.y_neg_speed = rd.randint(speed_min, speed_max)

        self.color_value = get_color_value_from_growth_speed(self.x_pos_speed, self.y_pos_speed, self.x_neg_speed,
                                                             self.y_neg_speed)
        self.reproduce_in_frame = 1


def prepare_for_plotting(img):
    for y in range(0, len(img)):
        for x in range(0, len(img[y])):
            if isinstance(img[x][y], Seed):
                if img[x][y].reproduce_in_frame == 1:
                    img[x][y] = 2
                else:
                    img[x][y] = img[x][y].color_value

    return img


def plot_image(img):
    img = prepare_for_plotting(img)

    plot = sb.heatmap(img, cmap=custom_cmap, vmin=0, vmax=2).invert_yaxis()

    plt.show()


def generate_next_frame(img, frame):
    for y in range(0, len(img)):
        for x in range(0, len(img[y])):
            if isinstance(img[x][y], Seed) and img[x][y].reproduce_in_frame == frame:
                current_seed = img[x][y]

                for dx in range(-current_seed.x_neg_speed, current_seed.x_pos_speed + 1):
                    if x + dx in range(0, WIDTH) and not isinstance(img[x + dx][y], Seed):
                        img[x + dx][y] = copy.copy(current_seed)
                        img[x + dx][y].reproduce_in_frame = frame + 1

                for dy in range(-current_seed.y_neg_speed, current_seed.y_pos_speed + 1):
                    if y + dy in range(0, HEIGHT) and not isinstance(img[x][y + dy], Seed):
                            img[x][y + dy] = copy.copy(current_seed)
                            img[x][y + dy].reproduce_in_frame = frame + 1
            elif rd.randint(0,spawn_prob) == 0:
                s = Seed()
                img[x][y] = s
                img[x][y].reproduce_in_frame = frame+1
    return img


#TODO: Mit der Zeit neue Seeds einfügen -> beim Reproduzieren 1% Chanche, dass neuer Kristall entsteht
#TODO: Copy.copy Methode ineffizient -> img als Reihungen aus Tupeln (frame, seed)


img = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]

for i in range(0,seed_num):
    img[rd.randint(1,WIDTH-1)][rd.randint(1,HEIGHT-1)] = Seed()

for frame in range(1, 100):
    img = generate_next_frame(img, frame)


new_img = img
old_img = 0
frame = 0
while not old_img == new_img:
    frame += 1
    old_img = new_img
    new_img = generate_next_frame(old_img, frame)

plot_image(new_img)

