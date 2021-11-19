import os

from pygame import Vector2

FPS = 60
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
PIPE_GAP_SIZE = 110
PRO_PATH = os.path.dirname(os.path.abspath(__file__))
NUMBER_IMG_PATH = os.path.join(PRO_PATH, 'content/images/numbers/')
BIRD_IMG_PATHS = os.path.join(PRO_PATH, 'content/images/birds/')
BACKGROUND_IMG_PATH = os.path.join(PRO_PATH, 'content/images/background/')
GROUND_IMG_PATH = os.path.join(PRO_PATH, 'content/images/base.png')
PIPE_IMG_PATH = os.path.join(PRO_PATH, 'content/images/pipe/g.png')
GAME_OVER_IMG_PATH = os.path.join(PRO_PATH, 'content/images/gameover.png')
GAME_START_IMG_PATH = os.path.join(PRO_PATH, 'content/images/start.png')
RGB_BLACK = (0, 0, 0)
GOUND_POS = Vector2(0, SCREEN_HEIGHT*0.79)
DIE_AUDIO = os.path.join(PRO_PATH, 'content/audios/die.wav')
HIT_AUDIO = os.path.join(PRO_PATH, 'content/audios/hit.wav')
POINT_AUDIO = os.path.join(PRO_PATH, 'content/audios/point.wav')
SWOOSH_AUDIO = os.path.join(PRO_PATH, 'content/audios/swoosh.wav')
WING_AUDIO = os.path.join(PRO_PATH, 'content/audios/wing.wav')
