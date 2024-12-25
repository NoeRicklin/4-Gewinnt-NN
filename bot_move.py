import os

gameState = [[0 for _ in range(6)] for _ in range(7)]



def bot_move(gameState, parameters):
    prev_layer_activation = []
    # converts the gamestate into a usable format as the input vector
    for column in gameState:
        prev_layer_activation += column

    for layer in parameters:
        # one layer
        cur_prev_layer_activation = []
        for node in layer:
            # one node
            node_activation = float(node[1]) # Adds bias
            for prev_nodes_index in range(len(prev_layer_activation)):
                # Adds linear combination of previous layer
                node_activation += prev_layer_activation[prev_nodes_index] * float(node[0][prev_nodes_index])
            cur_prev_layer_activation.append(node_activation)
        prev_layer_activation = cur_prev_layer_activation

    # get the column with the highest activation of the output nodes
    column_move = prev_layer_activation.index(max(prev_layer_activation))

    # ensures no move into filled columns
    while gameState[column_move][-1] != 0:
        prev_layer_activation[prev_layer_activation.index(max(prev_layer_activation))] = -9999
        column_move = prev_layer_activation.index(max(prev_layer_activation))
        if max(prev_layer_activation) == -9999:
            return -1

    return column_move
