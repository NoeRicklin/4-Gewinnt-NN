game_data = open(r"Documents\Schule\AngewandteMathematik\RegressionUndNeuronaleNetzwerke\VierGewinnt\connect_4\connect-4.data")
single_game = game_data.read().split("\n")[1889].split(",")[:-1]

conv_game = [[0 for _ in range(6)] for _ in range(7)]
for index, element in enumerate(single_game):
    y = index % 6
    x = index // 7

    if element == "x": value = 1
    elif element == "o": value = -1
    else: value = 0

    conv_game[x][y] = value

assignments = {1:"x",
               -1:"o",
               0:" "}

for y in range(6):
    line = ""
    for x in range(7):
        line += assignments[conv_game[x][y]]
