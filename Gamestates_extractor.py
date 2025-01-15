import os

game_data = open(os.path.dirname(__file__) + f'\\connect_4\\connect-4.data')
single_games = game_data.read().split("\n")


def new_gameState(game_index):
    raw_game = single_games[game_index].split(",")[:-1]
    conv_game = [[0 for _ in range(6)] for _ in range(7)]
    for index, element in enumerate(raw_game):
        y = index % 6
        x = index // 6

        if element == "x":
            value = 1
        elif element == "o":
            value = -1
        else:
            value = 0

        conv_game[x][y] = value
    return conv_game