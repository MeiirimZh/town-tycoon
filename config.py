import pygame

pygame.init()

SCREENWIDTH = 1366
SCREENHEIGHT = 768
FPS = 60

MONOCRAFT_FONT = "data/fonts/Monocraft.otf"

BUTTON_COL = (255, 255, 255)
BUTTON_COL_H = (200, 200, 200)
BUTTON_COL_P = (100, 100, 100)

ANIMAL_HUNT_COOLDOWN_TIME = 30
CHOP_TREE_COOLDOWN_TIME = 20

images = {'crosshair': pygame.image.load('images/crosshair.png'),
          'axe': pygame.image.load('images/axe.png'),
          'gui_main_menu': pygame.image.load('images/gui/panels/doska.png'),
          'gui_resources_panel': pygame.image.load('images/gui/panels/doska2.png'),
          'food_icon': pygame.image.load('images/gui/icons/eda.png'),
          'stone_icon': pygame.image.load('images/gui/icons/kamen.png'),
          'wood_icon': pygame.image.load('images/gui/icons/drova.png'),
          'water_icon': pygame.image.load('images/gui/icons/voda.png'),
          'small_house': pygame.image.load('images/houses/small_house.png'),
          'ct_bg': pygame.image.load('images/backgrounds/chop_tree_bg.png'),
          'ah_bg': pygame.image.load('images/backgrounds/an_hunt_bg.png'),
          'animal': pygame.image.load('images/taksa_s_rogami.png')}

sounds = {'cancel1': pygame.mixer.Sound('sounds/Cancel 1.mp3')}
