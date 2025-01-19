import pygame
import os
from Bot_moveV4 import bot_move
from time import sleep

bot_count = 100
# pygame setup
pygame.init()
width, height = 700, 600
tile_size = int(width / 7)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

all_parameters = [[] for _ in range(bot_count)]

for i in range(bot_count):
    parameters = open(os.path.dirname(__file__) + f'\\V1-1\\bot_parametersV1-1\\Bot{i}.txt', "r").read()
    # converts the parameters into a usable format
    # parameters[layer][node][constant]([coefficient])
    parameters = parameters.split("\n")
    parameters = [layer.split("|") for layer in parameters]
    parameters = [[node.split(" ") for node in layer] for layer in parameters]
    parameters = [[[node[0].split(","), node[1]] for node in layer] for layer in parameters]
    all_parameters[i] = parameters

gameState = [[0 for _ in range(6)] for _ in range(7)]
cur_player = 1


def drawGrid():
    screen.fill("purple")
    for x in range(0, width, tile_size):
        for y in range(0, height, tile_size):
            rect = pygame.Rect(x, y, tile_size, tile_size)
            pygame.draw.rect(screen, "black", rect, 1)


def display_chip(position, type):
    real_position = [position[0] * tile_size + tile_size / 2, height - position[1] * tile_size - tile_size / 2]
    if type == 1:
        pygame.draw.circle(screen, "red", real_position, 40)
    if type == -1:
        pygame.draw.circle(screen, "blue", real_position, 40)


def put_chip(position, type):
    gameState[position[0]][position[1]] = type


def draw_game(list):
    for x in range(0, 7):
        for y in range(0, 6):
            display_chip([x, y], list[x][y])


def get_diag_states(game_state, stone_pos, dir):
    diagonal = []
    cur_pos = stone_pos

    while True:
        offset_pos = (cur_pos[0] - dir[0], cur_pos[1] - dir[1])
        if not (0 <= offset_pos[0] <= 6 and 0 <= offset_pos[1] <= 5):
            break
        cur_pos = offset_pos

    while True:
        diagonal.append(game_state[cur_pos[0]][cur_pos[1]])
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
    column = play_move(cur_player, parameters)
    if column is None: return

    for index, tile in enumerate(gameState[column]):
        if tile == 0:
            gameState[column][index] = cur_player
            new_stone_pos = (column, index)
            return new_stone_pos


# held variable to make sure one click isn't counted for multiple inputs
held = False


def player_move():
    global held
    if pygame.mouse.get_pressed()[0]:
        if held:
            return
        held = True
        pos = pygame.mouse.get_pos()
        column = pos[0] // 100
        return column
    else:
        held = False


def play_move(cur_player, parameters):
    # return player_move()
    if cur_player == -1:
        return bot_move(gameState, parameters, cur_player)
    else:
        player_move()


rounds = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
            running = False
            pygame.quit()
            exit()

    # Draw Game
    drawGrid()
    draw_game(gameState)

    # Play the move
    new_stone_pos = do_move(gameState, cur_player, all_parameters[0])
    sleep(0.2)

    # Check if someone won with the last move
    if new_stone_pos is not None:
        if test_win(gameState, new_stone_pos, cur_player):
            print(f"Player {cur_player} has won!!!")
            running = False
        else:
            cur_player *= -1

    pygame.display.flip()
    dt = clock.tick(20) / 100
