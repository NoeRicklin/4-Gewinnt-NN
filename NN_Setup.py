from random import random
import os

n_input = 42
n_hlayers = [3,]
n_output = 7

NN_file = open(os.path.dirname(__file__) + '\\Bot_Parameters.txt', "w")
NN_file.close()

NN_file = open(os.path.dirname(__file__) + '\\Bot_Parameters.txt', "a")

for hlayer in n_hlayers:
    layer_parameters = ""
    for node in range(hlayer):
        for input in range(n_input):
            layer_parameters += str(random()) + ","
        layer_parameters = layer_parameters.rstrip(",") + "|"
        for input in range(n_input):
            layer_parameters += str(random()) + ","
        layer_parameters = layer_parameters.rstrip(",") + " "
    NN_file.write(layer_parameters)


NN_file.close()
NN_file = open(os.path.dirname(__file__) + '\\Bot_Parameters.txt', "r")
print(NN_file.read())
NN_file.close()
