from random import random
import os
from time import time

# Format of Bot{i}.txt:
# Each line represents the parameters for one layer (not including the input)
# Individual nodes within one layer are separated by "|"
# Within one node first there are the coefficients to the nodes for the
# previous layer separated by "," and at the end there is the bias for the
# node, separated from the coefficients by a " "
# Example layer: 4,7,5 7|7,10,1 2|10,8,5 7|1,4,6 3|7,10,4 1|10,6,6 10|2,10,6 2

n_input = 42
n_hlayers = [7]
n_output = 7

bot_count = 100

layers = [n_input] + n_hlayers + [n_output]


def create_bot(bot_name):
    NN_file = open(os.path.dirname(__file__) + f'\\bot_parametersV4\\Bot{bot_name}.txt', "w")
    NN_file.close()
    NN_file = open(os.path.dirname(__file__) + f'\\bot_parametersV4\\Bot{bot_name}.txt', "a")
    for layer_ind in range(1, len(layers)):
        layer_params = ""
        cur_layer = layers[layer_ind]
        prev_layer = layers[layer_ind - 1]

        for node in range(cur_layer):
            node_params = ""

            for prev_node in range(prev_layer):
                # Add random value for the coefficients
                node_params += str(random() - 0.5) + ","

            # Add random value for the bias
            node_params = node_params.rstrip(",") + " " + str(random() - 0.5) + "|"

            layer_params += node_params
        if layer_ind != len(layers) - 1:
            layer_params = layer_params.rstrip("|") + "\n"
        else:
            layer_params = layer_params.rstrip("|")
        NN_file.write(layer_params)
    NN_file.close()


# create 100 bots
for i in range(bot_count):
    create_bot(i)
