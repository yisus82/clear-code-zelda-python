# game setup
FPS = 60
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
TILESIZE = 64

# ui
BAR_BORDER_WIDTH = 5
BAR_HEIGHT = 20
BAR_MARGIN = 10
EXP_BORDER_WIDTH = 5
EXP_MARGIN = 20
EXP_PADDING = 20
HEALTH_BAR_WIDTH = 200
ITEM_BOX_SIZE = 80
ITEM_BOX_MARGIN = 20
ITEM_BOX_BORDER_WIDTH = 5
MANA_BAR_WIDTH = 140
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# colors
HEALTH_COLOR = 'red'
MANA_COLOR = 'blue'
TEXT_COLOR = '#EEEEEE'
UI_BG_COLOR = '#555555'
UI_BORDER_COLOR = '#111111'
UI_BORDER_COLOR_ACTIVE = 'gold'
WATER_COLOR = '#71DDEE'

# weapons
WEAPONS = {
    'sword': {
        'cooldown': 100,
        'damage': 15,
        'graphic': '../graphics/weapons/sword/full.png',
        'name': 'Sword',
    },
    'lance': {
        'cooldown': 400,
        'damage': 30,
        'graphic': '../graphics/weapons/lance/full.png',
        'name': 'Lance',
    },
    'axe': {
        'cooldown': 300,
        'damage': 20,
        'graphic': '../graphics/weapons/axe/full.png',
        'name': 'Axe',
    },
    'rapier': {
        'cooldown': 50,
        'damage': 8,
        'graphic': '../graphics/weapons/rapier/full.png',
        'name': 'Rapier',
    },
    'sai': {
        'cooldown': 80,
        'damage': 10,
        'graphic': '../graphics/weapons/sai/full.png',
        'name': 'Sai',
    }
}

# spells
SPELLS = {
    'flame': {
        'strength': 5,
        'cost': 20,
        'graphic': '../graphics/spells/flame/full.png',
        'name': 'Flame',
    },
    'heal': {
        'strength': 20,
        'cost': 10,
        'graphic': '../graphics/spells/heal/full.png',
        'name': 'Heal',
    }}
