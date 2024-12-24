gameState = [[0 for _ in range(6)] for _ in range(7)]
parameter = -1
intercept = 2
n_hlayers = [3]
n_values = [0, 0, 0]
# n_values = [[0 for _ in range(i)] for i in n_hlayers]


for nodes in range(n_hlayers[0]):
    n_values[nodes] = intercept
    for column in gameState:
        for tile in column:
            n_values[nodes] += parameter*tile

print(n_values)