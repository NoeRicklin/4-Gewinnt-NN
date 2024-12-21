from random import random

n_input = 42
n_hlayers = [3,]
n_output = 7

NN_file = open("C:/Users/noeri/Documents/Schule/AngewandteMathematik/RegressionUndNeuronaleNetzwerke/VierGewinnt/Bot_Parameters.txt", "w")
NN_file.close()

NN_file = open("C:/Users/noeri/Documents/Schule/AngewandteMathematik/RegressionUndNeuronaleNetzwerke/VierGewinnt/Bot_Parameters.txt", "a")

for hlayer in n_hlayers:
    layer_parameters = ""
    for _ in range(hlayer):
        layer_parameters += str(random()) + ","
    layer_parameters = layer_parameters.rstrip(",") + "|"

    for _ in range(hlayer):
        layer_parameters += str(random()) + ","
    layer_parameters = layer_parameters.rstrip(",")
    NN_file.write(layer_parameters)


NN_file.close()
NN_file = open("C:/Users/noeri/Documents/Schule/AngewandteMathematik/RegressionUndNeuronaleNetzwerke/VierGewinnt/Bot_Parameters.txt", "r")
print(NN_file.read())
NN_file.close()
