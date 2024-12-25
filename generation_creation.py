from NN_Setup import bot_count
from random import random
from copy import deepcopy
import os
num_fittest = 20
offset_range = 0.05


def next_generation(prev_generation, win_list):
    indices = [i for i in range(len(win_list))]
    win_ind = zip(win_list, indices)
    sorted_indices = [i[1] for i in sorted(win_ind, reverse=True)]
    fittest = sorted_indices[:num_fittest]
    for i in range(bot_count):
        make_child(prev_generation[fittest[i % num_fittest]], i)


def make_child(parent_parameters, bot_index):
    adjusted_parameters = ""
    new_parameters = deepcopy(parent_parameters)
    for layer in new_parameters:
        for node in layer:
            for coefficient in node[0]:
                adjusted_parameters += str(float(coefficient) + random() * offset_range - offset_range / 2)
                adjusted_parameters += ","
            adjusted_parameters = adjusted_parameters.rstrip(",") + " "
            adjusted_parameters += str(float(node[1]) + random() * offset_range - offset_range / 2)
            adjusted_parameters += "|"
        adjusted_parameters = adjusted_parameters.rstrip("|") + "\n"
    adjusted_parameters = adjusted_parameters.rstrip("\n")

    NN_file = open(os.path.dirname(__file__) + f'\\bot_parameters\\Bot{bot_index}.txt', "w")
    NN_file.write(adjusted_parameters)
    NN_file.close()
