import pygame

# pygame setup
pygame.init()
width, height = 700, 600
tile_size = int(width / 7)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

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

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
            running = False

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
