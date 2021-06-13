import pygame
import sys

BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 900
BLOCK_SIZE = 10
GAME_SPEED = 350

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
horizontal_blocks = int(WINDOW_WIDTH / BLOCK_SIZE)
vertical_blocks = int(WINDOW_HEIGHT / BLOCK_SIZE)
start_button = pygame.Rect(10, 10, 80, 24)
font = pygame.font.SysFont(pygame.font.get_default_font(), 24)
start_button_text = font.render('Start/stop', True, BLACK)
arr = [[False] * vertical_blocks for i in range(horizontal_blocks)]
running = False


def draw_grid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)


def draw_buttons():
    pygame.draw.rect(screen, WHITE, start_button)
    screen.blit(start_button_text, start_button.topleft)


def setBlockColor(x, y, color):
    coordX = x * BLOCK_SIZE
    coordY = y * BLOCK_SIZE
    rect = pygame.Rect(coordX, coordY, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, color, rect)


def toggleBlockState(pos):
    x = int(pos[0] / BLOCK_SIZE)
    y = int(pos[1] / BLOCK_SIZE)
    arr[x][y] = not arr[x][y]


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if start_button.collidepoint(event.pos):
                global running
                running = not running
            else:
                toggleBlockState(pygame.mouse.get_pos())



def draw_lifes():
    for x in range(horizontal_blocks):
        for y in range(vertical_blocks):
            if arr[x][y]:
                setBlockColor(x, y, WHITE)
            else:
                setBlockColor(x, y, BLACK)


def resolve_array():
    array = [[False] * vertical_blocks for i in range(horizontal_blocks)]
    for x in range(horizontal_blocks):
        for y in range(vertical_blocks):
            n = number_of_neighbours(x, y)
            array[x][y] = arr[x][y]
            if n == 3:
                array[x][y] = True
            elif n != 2:
                array[x][y] = False
    return array


def number_of_neighbours(x, y):
    result = 0
    for i in range(3):
        if safe_list_get(arr, x - 1 + i, y - 1, False):
            result += 1
    for i in range(3):
        if safe_list_get(arr, x - 1 + i, y + 1, False):
            result += 1
    if safe_list_get(arr, x - 1, y, False):
        result += 1
    if safe_list_get(arr, x + 1, y, False):
        result += 1
    return result


def safe_list_get(l, x, y, default):
    try:
        return l[x][y]
    except IndexError:
        return default


while True:
    screen.fill(BLACK)
    handle_events()
    draw_lifes()
    draw_grid()
    draw_buttons()
    pygame.display.update()

    if running:
        arr = resolve_array()
        pygame.time.delay(GAME_SPEED)
