import pygame
from Utils import *
from time import sleep

# pygame setup
pygame.init()
width, height = 700, 600
tile_size = int(width / 7)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

# game setup
gameState = [[0 for _ in range(6)] for _ in range(7)]
cur_player = 1

# choose bot infos
bot_count = 100
against_bot = True
bot_player = -1  # Whether bot goes first or not
version = "V6"
bot_index = 24
all_parameters = parameters_extraction(f'\\{version}\\bot_parameters{version}\\', bot_count)

# import correct bot_move version
if version == "V5":
    from V5.Bot_moveV5 import bot_move
else:
    from Bot_move import bot_move


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
    if cur_player == bot_player and against_bot:
        return bot_move(gameState, parameters, cur_player)
    else:
        return player_move()


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
    new_stone_pos = do_move(gameState, cur_player, all_parameters[bot_index])

    # Check if someone won with the last move
    if new_stone_pos is not None:
        if test_win(gameState, new_stone_pos, cur_player):
            if cur_player == bot_player and against_bot:
                print(f"Bot{bot_index} has won!!!")
            else:
                print(f"Player {cur_player} has won!!!")
            # Draw Game
            drawGrid()
            draw_game(gameState)
            running = False
        else:
            cur_player *= -1
    pygame.display.flip()
    dt = clock.tick(20) / 100
