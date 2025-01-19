from NN_SetupV1_3 import bot_count, version
from numpy import random
from copy import deepcopy
import os
num_fittest = 30


def next_generation(prev_generation, fitness_list):
    # Creates a list of the bots' indices, sorted by their respective fitness scores
    indices = [i for i in range(bot_count)]
    win_ind = zip(fitness_list, indices)
    sorted_indices = [i[1] for i in sorted(win_ind, reverse=True)]

    fittest = sorted_indices[:num_fittest]

    # Creates a child of one of the fittest bots
    for i in range(bot_count):
        make_child(prev_generation[fittest[i % num_fittest]], i)


def make_child(parent_parameters, bot_index):
    adjusted_parameters = ""
    new_parameters = deepcopy(parent_parameters)
    for layer in new_parameters:
        for node in layer:
            for coefficient in node[0]:
                adjusted_parameters += str(float(coefficient) + random.normal(0, 0.2)) + ","
            adjusted_parameters = adjusted_parameters.rstrip(",") + " "
            adjusted_parameters += str(float(node[1]) + random.normal(0, 0.2)) + "|"
        adjusted_parameters = adjusted_parameters.rstrip("|") + "\n"
    adjusted_parameters = adjusted_parameters.rstrip("\n")

    NN_file = open(os.path.dirname(__file__) + f'\\bot_parameters{version}\\Bot{bot_index}.txt', "w")
    NN_file.write(adjusted_parameters)
    NN_file.close()
