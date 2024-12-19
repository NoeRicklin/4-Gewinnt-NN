import pygame

# pygame setup
pygame.init()
width, height = 700, 600
tile_size = int(width / 7)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

# gameState = [[0 for _ in range(6)] for _ in range(7)]
gameState = [[0, 0, 0, 0, 0, 0], [1, -1, 0, 0, 0, 0], [1, -1, -1, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
 
def drawGrid():
    for x in range(0, width, tile_size):
        for y in range(0, height, tile_size):
            rect = pygame.Rect(x, y, tile_size, tile_size)
            pygame.draw.rect(screen, "black", rect, 1)

def put_thing(position, type):
    real_position = [position[0]*tile_size + tile_size/2, height-position[1]*tile_size - tile_size/2]
    if type == -1:
        pygame.draw.circle(screen, "red", real_position, 40)
    if type == 1:
        pygame.draw.circle(screen, "blue", real_position, 40)


def draw_game(list):
    for x in range(0, 7):
        for y in range(0, 6):
            put_thing([x, y], list[x][y])


def test_win(game_state, new_pos, new_type):
    ver_line = game_state[new_pos[0]]
    hor_line = [game_state[i][new_pos[1]] for i in range(7)]

    d1_line = []
    cur_pos = new_pos
    while True:
        offset_pos = (cur_pos[0]-1, cur_pos[1]-1)
        if not offset_pos[0] >= 0 and offset_pos[1] >= 0:
            break
        cur_pos = offset_pos
    print(cur_pos)
    while True:
        d1_line.append(cur_pos)
        offset_pos = (cur_pos[0]+1, cur_pos[1]+1)

    print(d1_line, flush=True)
    

test_win(gameState, (1, 2), 0)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            z = pos[0] // 100
            for i in range (0, 6):
                if gameState[z][i] == 0:
                    gameState[z][i] = -1
                    break

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
