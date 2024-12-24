import os

gameState = [[0 for _ in range(6)] for _ in range(7)]

# parameters[layer][node][constant]([coefficient])
parameters = open(os.path.dirname(__file__) + '\\Bot_Parameters.txt', "r").read()
parameters = parameters.split("\n")[:-1]
parameters = [layer.split("|") for layer in parameters]
parameters = [[node.split(" ") for node in layer] for layer in parameters]
parameters = [[[node[0].split(","), node[1]] for node in layer] for layer in parameters]

# print(parameters)

intercept = 2
n_hlayers = [3]
n_values = [0, 0, 0]
# n_values = [[0 for _ in range(i)] for i in n_hlayers]

inputs = [0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def bot_move(gameState):
    layer_activation = []
    for column in gameState:
        layer_activation += column

    for layer in parameters:
        # print(f"layer_activation: {layer_activation}")
        # one layer
        cur_layer_activation = []
        for node in layer:
            # one node
            node_activation = float(node[1])
            for prev_nodes_index in range(len(layer_activation)):
                node_activation += layer_activation[prev_nodes_index] * float(node[0][prev_nodes_index])
            cur_layer_activation.append(node_activation)
        layer_activation = cur_layer_activation

    column_move = layer_activation.index(max(layer_activation))
    while gameState[column_move][-1] != 0:
        layer_activation[layer_activation.index(max(layer_activation))] = -999
        column_move = layer_activation.index(max(layer_activation))
    return column_move
