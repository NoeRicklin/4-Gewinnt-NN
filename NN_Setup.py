from random import random
import os

# Format of Bot_Paramters.txt:
# Each line represents the parameters for one layer (not including the input)
# Individual nodes within one layer are seperated by "|"
# Within one node first there are the coefficients to the nodes for the
# previous layer seperated by "," and at the end there is the bias for the
# node, seperated from the coefficients by a " "
# Example layer: 4,7,5 7|7,10,1 2|10,8,5 7|1,4,6 3|7,10,4 1|10,6,6 10|2,10,6 2

n_input = 42
n_hlayers = [3]
n_output = 7

layers = [n_input] + n_hlayers + [n_output]

# clears current parameters file
NN_file = open(os.path.dirname(__file__) + '\\Bot_Parameters.txt', "w")
NN_file.close()

# open parameters file to write
NN_file = open(os.path.dirname(__file__) + '\\Bot_Parameters.txt', "a")

for layer_ind in range(1, len(layers)):
    layer_params = ""
    cur_layer = layers[layer_ind]
    prev_layer = layers[layer_ind - 1]

    for node in range(cur_layer):
        node_params = ""

        for prev_node in range(prev_layer):
            # Add random value for the coefficients
            node_params += str(random()) + ","

        # Add random value for the bias
        node_params = node_params.rstrip(",") + " " + str(random()) + "|"

        layer_params += node_params

    layer_params = layer_params.rstrip("|") + "\n"
    NN_file.write(layer_params)

NN_file.close()
