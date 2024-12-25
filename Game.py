from bot_move import bot_move
from time import time

initState = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

# gameState = [[0, 0, 0, 0, 0, 0], [1, -1, 0, 0, 0, 0], [1, -1, -1, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
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
        offset_pos = (cur_pos[0]+dir[0], cur_pos[1]+dir[1])
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


def do_move(gameState, cur_player):
    column = bot_move(gameState)

    for tile_index, tile in enumerate(gameState[column]):
        if tile == 0:
            gameState[column][tile_index] = cur_player
            new_stone_pos = (column, tile_index)
            return new_stone_pos


t0 = time()

rounds = 0
gameState = [initState_column[:] for initState_column in initState]
while rounds < 50:
    # Play the move
    new_stone_pos = do_move(gameState, cur_player)
    
    if test_win(gameState, new_stone_pos, cur_player):
        rounds += 1
        gameState = [initState_column[:] for initState_column in initState]
    else:
        cur_player *= -1
print(rounds)
print(time() - t0)
