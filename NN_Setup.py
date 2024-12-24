from random import random
import os

n_input = 42
n_hlayers = [3]
n_output = 7

layers = [n_input] + n_hlayers + [n_output]

NN_file = open(os.path.dirname(__file__) + '\\Bot_Parameters.txt', "w")
NN_file.close()

NN_file = open(os.path.dirname(__file__) + '\\Bot_Parameters.txt', "a")

for layer_ind in range(1, len(layers)):
    cur_layer = layers[layer_ind]
    prev_layer = layers[layer_ind - 1]
    layer_params = ""
    for node in range(cur_layer):
        node_params = ""
        for prev_node in range(prev_layer):
            node_params += str(random()) + ","
        node_params = node_params.rstrip(",") + " " + str(random()) + "|"

        layer_params += node_params

    layer_params = layer_params.rstrip("|") + "\n"
    NN_file.write(layer_params)



NN_file.close()
