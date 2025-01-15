from Bot_move import bot_move
from NN_Setup import bot_count
from Generation_creation import next_generation, num_fittest
from copy import deepcopy
import os
from time import time

initState = [[0 for _ in range(6)] for _ in range(7)]
cur_player = 1


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


def test_win(game_state, new_stone_pos, new_type):
    ver_line = game_state[new_stone_pos[0]]
    hor_line = [game_state[i][new_stone_pos[1]] for i in range(7)]
    d1_line = get_diag_states(game_state, new_stone_pos, (1, 1))
    d2_line = get_diag_states(game_state, new_stone_pos, (1, -1))
    for line in [hor_line, ver_line, d1_line, d2_line]:
        in_row_amount = 0
        for chip_type in line:
            if chip_type == new_type:
                in_row_amount += 1
            else:
                in_row_amount = 0
            if in_row_amount == 4:
                return True
    return False


def do_move(gameState, cur_player, parameters):
    column = bot_move(gameState, parameters)
    if column is None:
        return -1
    for tile_index, tile in enumerate(gameState[column]):
        if tile == 0:
            gameState[column][tile_index] = cur_player
            new_stone_pos = (column, tile_index)
            return new_stone_pos


def play_game(bot1, bot2):
    gameState = deepcopy(initState)
    bot1_parameters = all_parameters[bot1]
    bot2_parameters = all_parameters[bot2]
    cur_player = 1
    moves = 0
    while True:
        # Play the move
        new_stone_pos = do_move(gameState, cur_player, bot1_parameters if cur_player == 1 else bot2_parameters)
        moves += 1
        if new_stone_pos == -1:
            return moves, 0
        if test_win(gameState, new_stone_pos, cur_player):
            return moves, cur_player
        else:
            cur_player *= -1


all_parameters = [[] for _ in range(bot_count)]

generation = 1050
while True:
    total_moves = 0
    t1 = time()
    # read new parameters from bot files
    for i in range(bot_count):
        parameters = open(os.path.dirname(__file__) + f'\\bot_parameters\\Bot{i}.txt', "r").read()
        # converts the parameters into a usable format
        # parameters[layer][node][constant]([coefficient])
        parameters = parameters.split("\n")
        parameters = [layer.split("|") for layer in parameters]
        parameters = [[node.split(" ") for node in layer] for layer in parameters]
        parameters = [[[node[0].split(","), node[1]] for node in layer] for layer in parameters]
        all_parameters[i] = parameters

    # let the games begin!
    bot_score = [0 for _ in range(bot_count)]
    for bot1 in range(bot_count):
        for bot2 in range(bot_count):
            moves, winner = play_game(bot1, bot2)
            total_moves += moves
            if winner == 1:
                bot_score[bot1] += 10 + moves
                bot_score[bot2] -= 20 - 0.5 * moves

            elif winner == -1:
                bot_score[bot2] += 12 + moves
                bot_score[bot1] -= 20 - 0.5 * moves

            elif winner == 0:
                bot_score[bot1] -= 30
                bot_score[bot2] -= 30

    # it's reproducing time!
    next_generation(all_parameters, bot_score)
    t2 = time()

    print(f"Generation {generation} summary")
    print(f"Bot-Score: {bot_score}")
    fittest = [i[1] for i in sorted(zip(bot_score, [i for i in range(len(bot_score))]), reverse=True)[:num_fittest]]
    print(f"Fittest: {fittest}")
    print(f"Av. number of moves in generation: {round(total_moves / bot_count ** 2, 1)}", flush=True)
    print(f"Generation took {round(t2 - t1, 1)} seconds")
    print()

    generation += 1
