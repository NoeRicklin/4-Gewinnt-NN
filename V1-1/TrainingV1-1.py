from Bot_move import bot_move
from copy import deepcopy
from Generation_creation import next_generation, num_fittest
from time import time
from Utils import *

initState = [[0 for _ in range(6)] for _ in range(7)]
cur_player = 1


def do_move(gameState, cur_player, parameters):
    column = bot_move(gameState, parameters, cur_player)
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

generations = 1000

for _ in range(generations):
    total_moves = 0
    t1 = time()
    # read new parameters from bot files
    all_parameters = parameters_extraction("\\V1-1\\bot_parametersV1-\\")

    # let the games begin!
    bot_fitness = [0 for _ in range(bot_count)]
    for bot1 in range(bot_count):
        for bot2 in range(bot_count):
            moves, winner = play_game(bot1, bot2)
            total_moves += moves
            if winner == 1:
                bot_fitness[bot1] += 1

            elif winner == -1:
                bot_fitness[bot2] += 1

    # it's reproducing time!
    next_generation(all_parameters, bot_fitness)
    t2 = time()

    print(f"Bot-fitness: {bot_fitness}")
    fittest = [i[1] for i in sorted(zip(bot_fitness, [i for i in range(len(bot_fitness))]), reverse=True)[:num_fittest]]
    print(f"Fittest: {fittest}")
    print(f"Av. number of moves in generation: {round(total_moves / bot_count ** 2, 1)}")
    print(f"Generation took {round(t2 - t1, 1)} seconds")
    print()
