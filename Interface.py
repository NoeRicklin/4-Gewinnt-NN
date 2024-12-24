import pygame
from bot_test import bot_move

# pygame setup
pygame.init()
width, height = 700, 600
tile_size = int(width / 7)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

gameState = [[0 for _ in range(6)] for _ in range(7)]
# gameState = [[0, 0, 0, 0, 0, 0], [1, -1, 0, 0, 0, 0], [1, -1, -1, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
player = 1
 
def drawGrid():
    for x in range(0, width, tile_size):
        for y in range(0, height, tile_size):
            rect = pygame.Rect(x, y, tile_size, tile_size)
            pygame.draw.rect(screen, "black", rect, 1)

def display_chip(position, type):
    real_position = [position[0]*tile_size + tile_size/2, height-position[1]*tile_size - tile_size/2]
    if type == 1:
        pygame.draw.circle(screen, "red", real_position, 40)
    if type == -1:
        pygame.draw.circle(screen, "blue", real_position, 40)


def put_board(position, type):
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
        offset_pos = (cur_pos[0]+dir[0], cur_pos[1]+dir[1])
        if not (0 <= offset_pos[0] <= 6 and 0 <= offset_pos[1] <= 5):
            break
        cur_pos = offset_pos
    return diagonal


# print(get_diag_states(gameState, (0, 0), (1,1)))
def test_win(game_state, stone_pos, new_type):
    ver_line = game_state[stone_pos[0]]
    hor_line = [game_state[i][stone_pos[1]] for i in range(7)]
    d1_line = get_diag_states(game_state, stone_pos, (1, 1))
    d2_line = get_diag_states(game_state, stone_pos, (1, -1))

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


def do_move(event):
    global player, running
    column = get_move(player, event)
    if column is None: return
    for i in range (0, 6):
        if gameState[column][i] == 0:
            gameState[column][i] = player
            put_pos = (column, i)
            if test_win(gameState, put_pos, player):
                print(f"Player {player} has won!!!")
                running = False
            player *= -1
            break


def get_move(player, event):
    if player == -1:
        return bot_move(gameState)
    else:
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            column = pos[0] // 100
            return column


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
            running = False
        do_move(event)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    drawGrid()
    draw_game(gameState)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
