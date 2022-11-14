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
GAME_OVER_BORDER_WIDTH = 5
GAME_OVER_PADDING = 20
HEALTH_BAR_WIDTH = 200
ITEM_BOX_SIZE = 80
ITEM_BOX_MARGIN = 20
ITEM_BOX_BORDER_WIDTH = 5
MANA_BAR_WIDTH = 140
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# colors
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
BAR_VALUE_HEIGHT = 10
BAR_VALUE_WIDTH = 30
BAR_WIDTH = 5
HEALTH_COLOR = 'red'
MANA_COLOR = 'blue'
TEXT_COLOR = '#EEEEEE'
TEXT_COLOR_FORBIDDEN = 'red'
TEXT_COLOR_SELECTED = '#111111'
UI_BG_COLOR = '#555555'
UI_BORDER_COLOR = '#111111'
UI_BORDER_COLOR_ACTIVE = 'gold'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'
WATER_COLOR = '#71DDEE'

# weapons
WEAPONS = {
    'sword': {
        'cooldown': 100,
        'damage': 15,
        'graphic': '../graphics/weapons/sword/full.png',
        'audio': '../audio/player/weapons/sword.wav',
        'name': 'Sword',
    },
    'lance': {
        'cooldown': 400,
        'damage': 30,
        'graphic': '../graphics/weapons/lance/full.png',
        'audio': '../audio/player/weapons/sword.wav',
        'name': 'Lance',
    },
    'axe': {
        'cooldown': 300,
        'damage': 20,
        'graphic': '../graphics/weapons/axe/full.png',
        'audio': '../audio/player/weapons/sword.wav',
        'name': 'Axe',
    },
    'rapier': {
        'cooldown': 50,
        'damage': 8,
        'graphic': '../graphics/weapons/rapier/full.png',
        'audio': '../audio/player/weapons/sword.wav',
        'name': 'Rapier',
    },
    'sai': {
        'cooldown': 80,
        'damage': 10,
        'graphic': '../graphics/weapons/sai/full.png',
        'audio': '../audio/player/weapons/sword.wav',
        'name': 'Sai',
    },
}

# spells
SPELLS = {
    'flame': {
        'type': 'attack',
        'strength': 5,
        'cost': 20,
        'graphic': '../graphics/spells/flame/full.png',
        'audio': '../audio/player/spells/flame.wav',
        'name': 'Flame',
    },
    'heal': {
        'type': 'health',
        'strength': 20,
        'cost': 10,
        'graphic': '../graphics/spells/heal/full.png',
        'audio': '../audio/player/spells/heal.wav',
        'name': 'Heal',
    },
}

# enemies
ENEMIES = {
    'bamboo': {
        'health': 70,
        'exp': 120,
        'damage': 6,
        'attack_type': 'leaf',
        'attack_sound': '../audio/enemies/attacks/slash.wav',
        'speed': 3,
        'resistance': 3,
        'attack_radius': 50,
        'notice_radius': 300,
        'name': 'Bamboo',
    },
    'spirit': {
        'health': 100,
        'exp': 110,
        'damage': 8,
        'attack_type': 'thunder',
        'attack_sound': '../audio/enemies/attacks/fireball.wav',
        'speed': 4,
        'resistance': 3,
        'attack_radius': 60,
        'notice_radius': 350,
        'name': 'Spirit',
    },
    'raccoon': {
        'health': 300,
        'exp': 250,
        'damage': 40,
        'attack_type': 'claw',
        'attack_sound': '../audio/enemies/attacks/claw.wav',
        'speed': 2,
        'resistance': 3,
        'attack_radius': 120,
        'notice_radius': 400,
        'name': 'Raccoon',
    },
    'squid': {
        'health': 100,
        'exp': 100,
        'damage': 20,
        'attack_type': 'slash',
        'attack_sound': '../audio/enemies/attacks/slash.wav',
        'speed': 3,
        'resistance': 3,
        'attack_radius': 80,
        'notice_radius': 360,
        'name': 'Squid',
    },
}
