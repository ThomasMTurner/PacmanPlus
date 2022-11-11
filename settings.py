import pygame
from PIL import Image

pygame.init()

TILE_WIDTH = 16  # width and height of each individual tile
ROWS = 36
COLUMNS = 28
TOTAL_WIDTH = COLUMNS * TILE_WIDTH
TOTAL_HEIGHT = (ROWS * TILE_WIDTH) + 50
WIN_SIZE = (TOTAL_WIDTH , TOTAL_HEIGHT)  # returns aspect ratio 448 x 576

# direction values, values stored in this way so that when the ghosts want to reverse direction, for example in frightened mode, the program must simply multiply these values by -1 to obtain the opposite direction.
STOP = 0
UP = 1
DOWN = -1
RIGHT = 2
LEFT = -2

#COLOURS AND MISC.
BLACK = (0, 0, 0)  # (R,G,B)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
ORANGE = (255, 127, 0)
TEAL = (0, 128 ,128)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)
GREY = (109, 109, 109)
PURPLE = (255, 0, 255)

#INITIALSING DISPLAY
WIN = pygame.display.set_mode(WIN_SIZE)

#IMAGE MANIPULATION FOR SPRITES.
def get_colorkey(spritesheet):
    ''' Function or Class Name:
        Parameters:
        Return Value:
        Description:
        Author:
        Creation Date:
            '''
    im = Image.open(spritesheet)
    pixels = im.load()
    return pixels[0, 0]


def get_image(spritesheets, width, height, x, y, scale):
    ''' Function or Class Name:
        Parameters:
        Return Value:
        Description:
        Author:
        Creation Date:
            '''
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(spritesheets[1], (0, 0), (x, y, width, height))  # first set of coordinates where to place cut-out, second x and y parameter for where in the sprite-sheet to take width x height cut-out
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(get_colorkey(spritesheets[0]))
    return image


def test_image(image):
    while True:
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        WIN.blit(image, (224, 100))
        pygame.display.update()


#IMAGES ETC.
ghost_sprite_sheet = ["Spritesheets/Ghost-Spritesheet.png", pygame.image.load("Spritesheets/Ghost-Spritesheet.png").convert_alpha()] #[FILE, IMAGE]
pacman_sprite_sheet = ["Spritesheets/Spritesheet-2.png", pygame.image.load("Spritesheets/Spritesheet-2.png").convert_alpha()]
pacman_lives_counter = get_image(pacman_sprite_sheet, 40, 40, 850, 50, 0.6)  #35 x 35
blinky_facing_right = get_image(ghost_sprite_sheet, 16, 16, 0, 0, 1.2)
blinky_facing_left = get_image(ghost_sprite_sheet, 16, 16, 32, 0, 1.2)
blinky_facing_up = get_image(ghost_sprite_sheet, 16, 16, 64, 0, 1.2)
blinky_facing_down = get_image(ghost_sprite_sheet, 16, 16, 96, 0, 1.2)
pinky_facing_right = get_image(ghost_sprite_sheet,16, 16, 0, 16, 1.2)
pinky_facing_left = get_image(ghost_sprite_sheet,16, 16, 32, 16, 1.2)
pinky_facing_up = get_image(ghost_sprite_sheet,16, 16, 64, 16, 1.2)
pinky_facing_down = get_image(ghost_sprite_sheet,16, 16, 96, 16, 1.2)
inky_facing_right = get_image(ghost_sprite_sheet,16, 16, 0, 32, 1.2)
inky_facing_left = get_image(ghost_sprite_sheet,16, 16, 32, 32, 1.2)
inky_facing_up = get_image(ghost_sprite_sheet,16, 16, 64, 32, 1.2)
inky_facing_down = get_image(ghost_sprite_sheet,16, 16, 96, 32, 1.2)
clyde_facing_right = get_image(ghost_sprite_sheet,16, 16, 0, 48,1.2)
clyde_facing_left = get_image(ghost_sprite_sheet,16, 16, 32, 48,1.2)
clyde_facing_up = get_image(ghost_sprite_sheet,16, 16, 64, 48,1.2)
clyde_facing_down = get_image(ghost_sprite_sheet,16, 16, 96, 48,1.2)
super_elroy_facing_right = get_image(ghost_sprite_sheet, 16, 16, 0, 64, 1.2)
super_elroy_facing_left = get_image(ghost_sprite_sheet, 16, 16, 32, 64, 1.2)
super_elroy_facing_up = get_image(ghost_sprite_sheet, 16, 16, 64, 64, 1.2)
super_elroy_facing_down = get_image(ghost_sprite_sheet, 16, 16, 96, 64, 1.2)
brainless_facing_right = get_image(ghost_sprite_sheet, 16, 16, 0, 80, 1.2)
brainless_facing_left = get_image(ghost_sprite_sheet, 16, 16, 32, 80, 1.2)
brainless_facing_up = get_image(ghost_sprite_sheet, 16, 16, 64, 80, 1.2)
brainless_facing_down = get_image(ghost_sprite_sheet, 16, 16, 96, 80, 1.2)
patient_facing_right = get_image(ghost_sprite_sheet, 16, 16, 0, 96, 1.2)
patient_facing_left = get_image(ghost_sprite_sheet, 16, 16, 32, 96, 1.2)
patient_facing_up = get_image(ghost_sprite_sheet, 16, 16, 64, 96, 1.2)
patient_facing_down = get_image(ghost_sprite_sheet, 16, 16, 96, 96, 1.2)
hurricane_facing_right = get_image(ghost_sprite_sheet, 16, 16, 0, 112, 1.2)
hurricane_facing_left = get_image(ghost_sprite_sheet, 16, 16, 32, 112, 1.2)
hurricane_facing_up = get_image(ghost_sprite_sheet, 16, 16, 64, 112, 1.2)
hurricane_facing_down = get_image(ghost_sprite_sheet, 16, 16, 96, 112, 1.2)
frightened_img = get_image(ghost_sprite_sheet,16, 16, 128, 0, 1.2)
frightened_nearly_up = get_image(ghost_sprite_sheet,16, 16, 160, 0, 1.2)
eaten_facing_right = get_image(ghost_sprite_sheet,16, 16, 128, 16, 1.2)
eaten_facing_left = get_image(ghost_sprite_sheet,16, 16, 144, 16,1.2)
eaten_facing_up = get_image(ghost_sprite_sheet,16, 16, 160, 16,1.2)
eaten_facing_down = get_image(ghost_sprite_sheet,16, 16, 176, 16,1.2)
pacman_facing_right_partially_open = get_image(pacman_sprite_sheet, 50, 50, 850, 50, 0.5)
pacman_facing_right_fully_open = get_image(pacman_sprite_sheet, 50, 50, 850, 100, 0.5)
pacman_facing_down_partially_open = get_image(pacman_sprite_sheet, 50, 50, 850, 200, 0.5)
pacman_facing_down_fully_open = get_image(pacman_sprite_sheet, 50, 50, 850, 250, 0.5)
pacman_facing_left_partially_open = get_image(pacman_sprite_sheet, 50, 50, 850, 350, 0.5)
pacman_facing_left_fully_open = get_image(pacman_sprite_sheet, 50, 50, 850, 400, 0.5)
pacman_facing_up_partially_open = get_image(pacman_sprite_sheet, 50, 50, 850, 500, 0.5)
pacman_facing_up_fully_open = get_image(pacman_sprite_sheet, 50, 50, 850, 550, 0.5)
pacman_blank = get_image(pacman_sprite_sheet, 50, 50, 850, 300, 0.5)



blinky_sheet = [blinky_facing_right, blinky_facing_left, blinky_facing_up, blinky_facing_down]  # RIGHT, LEFT, UP, DOWN AT 0, 1, 2, 3
pinky_sheet = [pinky_facing_right, pinky_facing_left, pinky_facing_up, pinky_facing_down]
inky_sheet = [inky_facing_right, inky_facing_left, inky_facing_up, inky_facing_down]
clyde_sheet = [clyde_facing_right, clyde_facing_left, clyde_facing_up, clyde_facing_down]
super_elroy_sheet = [super_elroy_facing_right, super_elroy_facing_left, super_elroy_facing_up, super_elroy_facing_down]
brainless_sheet = [brainless_facing_right, brainless_facing_left, brainless_facing_up, brainless_facing_down]
patient_sheet = [patient_facing_right, patient_facing_left, patient_facing_up, patient_facing_down]
hurricane_sheet = [hurricane_facing_right, hurricane_facing_left, hurricane_facing_up, hurricane_facing_down]
frightened_sheet = [frightened_img, frightened_nearly_up]
eaten_sheet = [eaten_facing_right, eaten_facing_left, eaten_facing_up, eaten_facing_down]
pacman_movingleft_sheet = [pacman_blank, pacman_facing_left_fully_open, pacman_facing_left_partially_open]
pacman_movingright_sheet = [pacman_blank, pacman_facing_right_fully_open, pacman_facing_right_partially_open]
pacman_movingup_sheet = [pacman_blank, pacman_facing_up_fully_open, pacman_facing_up_partially_open]
pacman_movingdown_sheet = [pacman_blank, pacman_facing_down_fully_open, pacman_facing_down_partially_open]


ready_text = pygame.font.SysFont('arial', 24).render("READY!", True, YELLOW)  # STATIC TEXT OBJECTS IN ATTRIBUTES, DOESNT UPDATE IN THE MAIN GAME LOOP SO STORED HERE
ready_rect = ready_text.get_rect(center=(224, 350))
go_text = pygame.font.SysFont('arial', 24).render("GO!", True, YELLOW)
go_rect = go_text.get_rect(center=(224, 350))
game_over_text = pygame.font.SysFont('arial', 24).render("GAME OVER!", True, YELLOW)
game_over_rect = game_over_text.get_rect(center=(224, 250))