import os


def get_diag_states(gameState, stone_pos, dir):
    diagonal = []
    cur_pos = stone_pos
    while True:
        offset_pos = (cur_pos[0] - dir[0], cur_pos[1] - dir[1])
        if not (0 <= offset_pos[0] <= 6 and 0 <= offset_pos[1] <= 5):
            break
        cur_pos = offset_pos
    while True:
        diagonal.append(gameState[cur_pos[0]][cur_pos[1]])
        offset_pos = (cur_pos[0] + dir[0], cur_pos[1] + dir[1])
        if not (0 <= offset_pos[0] <= 6 and 0 <= offset_pos[1] <= 5):
            break
        cur_pos = offset_pos
    return diagonal


def test_win(game_state, new_stone_pos, new_type, win_types={"Stapel": 0, "Flach": 0, "Diagonal": 0, "Unentschieden": 0}):
    ver_line = game_state[new_stone_pos[0]]
    hor_line = [game_state[i][new_stone_pos[1]] for i in range(7)]
    d1_line = get_diag_states(game_state, new_stone_pos, (1, 1))
    d2_line = get_diag_states(game_state, new_stone_pos, (1, -1))
    for type, line in enumerate([ver_line, hor_line, d1_line, d2_line]):
        in_row_amount = 0
        for chip_type in line:
            if chip_type == new_type:
                in_row_amount += 1
            else:
                in_row_amount = 0
            if in_row_amount == 4:
                if type == 0:
                    win_types["Stapel"] += 1
                elif type == 1:
                    win_types["Flach"] += 1
                else:
                    win_types["Diagonal"] += 1
                return True
    return False


def parameters_extraction(path, bot_count):
    all_parameters = []
    for i in range(bot_count):
        parameters = open(os.path.dirname(__file__) + f'{path}Bot{i}.txt', "r").read()
        # converts the parameters into a usable format
        # parameters[layer][node][constant]([coefficient])
        parameters = parameters.split("\n")
        parameters = [layer.split("|") for layer in parameters]
        parameters = [[node.split(" ") for node in layer] for layer in parameters]
        parameters = [[[node[0].split(","), node[1]] for node in layer] for layer in parameters]
        all_parameters.append(parameters)
    return all_parameters
