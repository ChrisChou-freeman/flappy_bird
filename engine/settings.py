import os

FPS = 60
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
PIPE_GAP_SIZE = 110
PRO_PATH = os.path.dirname(os.path.abspath(__file__))
NUMBER_IMG_PATH = os.path.join(PRO_PATH, 'content/images/numbers/')
BIRD_IMG_PATHS = os.path.join(PRO_PATH, 'content/images/birds/')
PIPE_IMG_PATH = os.path.join(PRO_PATH, 'content/images/pipe/')
BACKGROUND_IMG_PATH = os.path.join(PRO_PATH, 'content/images/background/day.png')
GROUND_IMG_PATH = os.path.join(PRO_PATH, 'content/images/base.png')
GAME_OVER_IMG_PATH = os.path.join(PRO_PATH, 'content/images/gameover.png')
GAME_START_IMG_PATH = os.path.join(PRO_PATH, 'content/images/start.png')
AUDIO_PATHS = {
    'die': os.path.join(PRO_PATH, 'content/audios/die.wav'),
    'hit': os.path.join(PRO_PATH, 'content/audios/hit.wav'),
    'point': os.path.join(PRO_PATH, 'content/audios/point.wav'),
    'swoosh': os.path.join(PRO_PATH, 'content/audios/swoosh.wav'),
    'wing': os.path.join(PRO_PATH, 'content/audios/wing.wav')
}
