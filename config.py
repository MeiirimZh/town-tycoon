import pygame

pygame.init()

SCREENWIDTH = 1366
SCREENHEIGHT = 768
FPS = 60

MONOCRAFT_FONT = "data/fonts/Monocraft.otf"

BUTTON_COL = (255, 255, 255)
BUTTON_COL_H = (200, 200, 200)
BUTTON_COL_P = (100, 100, 100)

ANIMAL_HUNT_COOLDOWN_TIME = 1
CHOP_TREE_COOLDOWN_TIME = 1
MINING_STONE_COOLDOWN_TIME = 1

images = {'crosshair': pygame.image.load('images/crosshair.png'),
          'axe': pygame.image.load('images/axe.png'),
          'gui_main_menu': pygame.image.load('images/gui/panels/doska.png'),
          'gui_resources_panel': pygame.image.load('images/gui/panels/doska2.png'),
          'food_icon': pygame.image.load('images/gui/icons/eda.png'),
          'stone_icon': pygame.image.load('images/gui/icons/kamen.png'),
          'wood_icon': pygame.image.load('images/gui/icons/drova.png'),
          'water_icon': pygame.image.load('images/gui/icons/voda.png'),
          'small_house': pygame.image.load('images/houses/small_house.png'),
          'small_house_icon': pygame.image.load('images/houses/icons/small_house_icon.png'),
          'medium_house': pygame.image.load('images/houses/medium_house.png'),
          'medium_house_icon': pygame.image.load('images/houses/icons/medium_house_icon.png'),
          'large_house': pygame.image.load('images/houses/large_house.png'),
          'large_house_icon': pygame.image.load('images/houses/icons/large_house_icon.png'),
          'school': pygame.image.load('images/houses/school.png'),
          'ct_bg': pygame.image.load('images/backgrounds/chop_tree_bg.png'),
          'ah_bg': pygame.image.load('images/backgrounds/an_hunt_bg.png'),
          'animal': pygame.image.load('images/taksa_s_rogami.png'),
          'gui_build_menu': pygame.image.load('images/gui/panels/build_menu.png'),
          'grass' : pygame.image.load('images/backgrounds/grass_tile.png'),
          'ct_tree': pygame.image.load('images/ct_minigame/ct_tree.png'),
          'ct_leaves' : pygame.image.load('images/ct_minigame/ct_leaves.png'),
          'ct_strike_indicator': pygame.image.load('images/ct_minigame/ct_strike_indicator.png'),
          'ct_aim': pygame.image.load('images/ct_minigame/ct_aim.png'),
          'ct_strike': pygame.image.load('images/ct_minigame/ct_strike.png'),
          'm_pickaxe': pygame.image.load('images/mine_minigame/pickaxe.png'),
          'm_stone': pygame.image.load('images/mine_minigame/kamen_yo.png'),
          'm_shards': pygame.image.load('images/mine_minigame/shattered_stone.png'),
          'm_bg': pygame.image.load('images/mine_minigame/bg_mine.png')}

sounds = {'cancel1': pygame.mixer.Sound('sounds/Cancel 1.mp3'),
          'build': pygame.mixer.Sound('sounds/Build.wav')}
