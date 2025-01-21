from Bot_move import bot_move
from copy import deepcopy
import csv
from Generation_creationV4 import next_generation, num_fittest, bot_count, version
from random import randint
from time import time
from Utils import *

initState = [[0 for _ in range(6)] for _ in range(7)]
cur_player = 1
win_types = {"Stapel": 0, "Flach": 0, "Diagonal": 0, "Unentschieden": 0}


def do_move(gameState, cur_player, parameters):
    column = bot_move(gameState, parameters, cur_player)

    # On Draw
    if column is None:
        return -1

    # Puts the stone in the correct position in the selected column
    for tile_index, tile in enumerate(gameState[column]):
        if tile == 0:
            gameState[column][tile_index] = cur_player
            new_stone_pos = (column, tile_index)
            return new_stone_pos


# Plays a random move to quickly set up a random Gamestate
def random_move(gameState, current_player):
    column = randint(0, 6)
    count = 0

    # If the random bot doesn't find any open columns anymore, assume it's resulted in a draw
    while gameState[column][-1] != 0:
        column = randint(0, 6)
        count += 1
        if count > 10:
            return -1, gameState

    # If column isn't filled, put stone on the top of the stack
    height = 0
    while gameState[column][height] != 0:
        height += 1
    new_stone_pos = (column, height)
    gameState[column][height] = current_player

    return new_stone_pos, gameState


# Create random gamestate with one move to win
def random_game():
    current_player = 1
    moves = 0
    gameState_random = deepcopy(initState)

    while True:
        # Play a random move
        new_stone_pos_random, gameState_random = random_move(gameState_random, current_player)
        moves += 1

        # Try again if this randomly generated game resulted in a draw
        if new_stone_pos_random == -1:
            gameState_random = deepcopy(initState)
            current_player = 1
            moves = 0
            continue

        # Test for a won game
        if test_win(gameState_random, new_stone_pos_random, current_player, win_types):
            if current_player == 1 and moves <= 20:
                gameState_random[new_stone_pos_random[0]][new_stone_pos_random[1]] = 0
                return gameState_random
            gameState_random = deepcopy(initState)
            moves = 0
        current_player *= -1


# Set up statistics-file for writing
statistics_file = open(os.path.dirname(__file__) + f"\\Generation_statistics{version}.csv", "w", newline="")
fieldnames = ["Generation", "Zeit", "Hoechste Fitness", "Durchschnittliche Fitness"]
writer = csv.DictWriter(statistics_file, fieldnames=fieldnames)
writer.writeheader()

# Run through all the generations of evolution
generations = 10000
for cur_generation in range(generations):
    t1 = time()

    # read new parameters from bot files
    all_parameters = parameters_extraction(f"\\{version}\\bot_parameters{version}\\", bot_count)

    # let the games begin!
    bot_fitness = [0 for _ in range(bot_count)]

    # Let each bot try to find the winning move on 100 boards
    for test in range(100):
        testState = random_game()
        for bot in range(bot_count):
            gameState = deepcopy(testState)
            bot_params = all_parameters[bot]
            new_stone_pos = do_move(gameState, 1, bot_params)
            gameState[new_stone_pos[0]][new_stone_pos[1]] = 1
            if test_win(gameState, new_stone_pos, 1, win_types):
                bot_fitness[bot] += 1

    # it's reproducing time!
    next_generation(all_parameters, bot_fitness)
    t2 = time()

    # Print generation statistics
    print(f"Generation {cur_generation}")
    print(f"Bot-fitness: {bot_fitness}")
    fittest = [i[1] for i in sorted(zip(bot_fitness, [i for i in range(len(bot_fitness))]), reverse=True)[:num_fittest]]
    print(f"Fittest: {fittest}")
    avg_fitness = sum(bot_fitness) / bot_count
    print(f"Avg. Fitness: {avg_fitness}")
    print(f"Generation took {round(t2 - t1, 1)} seconds")
    print()

    # Save generation statistics to file
    row = {"Generation": cur_generation,
           "Zeit": str(round(t2 - t1, 2)),
           "Hoechste Fitness": max(bot_fitness),
           "Durchschnittliche Fitness": avg_fitness}

    writer.writerow(row)

statistics_file.close()
