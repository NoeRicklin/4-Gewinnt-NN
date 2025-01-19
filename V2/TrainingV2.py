from Bot_move import bot_move
from copy import deepcopy
import csv
from Generation_creationV2 import next_generation, num_fittest, bot_count, version
from time import time
from Utils import *

initState = [[0 for _ in range(6)] for _ in range(7)]
cur_player = 1


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


def play_game(bot1, bot2):
    # initializes the gameState to an empty board
    gameState = deepcopy(initState)

    # retrieves the parameters for the selected bots
    bot1_parameters = all_parameters[bot1]
    bot2_parameters = all_parameters[bot2]

    cur_player = 1
    moves = 0

    while True:
        # Play the move
        new_stone_pos = do_move(gameState, cur_player, bot1_parameters if cur_player == 1 else bot2_parameters)
        moves += 1

        # Check for draw
        if new_stone_pos == -1:
            win_types["Unentschieden"] += 1
            return moves, 0

        # Check for win
        if test_win(gameState, new_stone_pos, cur_player, win_types):
            return moves, cur_player
        else:
            cur_player *= -1


# Set up statistics-file for writing
statistics_file = open(os.path.dirname(__file__) + f"\\Generation_statistics{version}.csv", "w", newline="")
fieldnames = ["Generation", "Zeit", "Spieldauer", "Stapel", "Flach", "Diagonal", "Unentschieden", "Hoechste Fitness",
              "Durchschnittliche Fitness"]
writer = csv.DictWriter(statistics_file, fieldnames=fieldnames)
writer.writeheader()

# Run through all the generations of evolution
generations = 1000
for cur_generation in range(generations):
    total_moves = 0
    win_types = {"Stapel": 0, "Flach": 0, "Diagonal": 0, "Unentschieden": 0}
    t1 = time()

    # read new parameters from bot files
    all_parameters = parameters_extraction(f"\\{version}\\bot_parameters{version}\\", bot_count)

    # let the games begin!
    bot_fitness = [0 for _ in range(bot_count)]
    for bot1 in range(bot_count):
        for bot2 in range(bot_count):
            if bot1 == bot2: continue
            moves, winner = play_game(bot1, bot2)
            total_moves += moves
            if winner == 1:
                bot_fitness[bot1] += 10 + moves
                bot_fitness[bot2] -= 15 - 0.5 * moves

            elif winner == -1:
                bot_fitness[bot2] += 12 + moves
                bot_fitness[bot1] -= 15 - 0.5 * moves

            elif winner == 0:
                bot_fitness[bot1] -= 30
                bot_fitness[bot2] -= 30

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
    avg_moves = round(total_moves / (bot_count * (bot_count - 1)), 1)
    print(f"Av. number of moves in generation: {avg_moves}")
    print(f"Generation took {round(t2 - t1, 1)} seconds")
    print(win_types)
    print()

    # Save generation statistics to file
    row = {"Generation": cur_generation,
           "Zeit": str(round(t2 - t1, 2)),
           "Spieldauer": avg_moves,
           "Hoechste Fitness": max(bot_fitness),
           "Durchschnittliche Fitness": avg_fitness}
    for type in win_types:
        row[type] = win_types[type]

    writer.writerow(row)

statistics_file.close()
