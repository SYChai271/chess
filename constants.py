# constants for the project

BG_COLOR = (0, 74, 158)
WIDTH, HEIGHT = 640, 640
WHITE_SQUARE = (232, 235, 239)
BLACK_SQUARE = (125, 135, 150)
SELECTED_SQUARE_COLOR = (128, 128, 255)
SQUARE_SIZE = 80
PIECE_PADDING = 10

def get_piece_img(color, piece):
    return 'images/{}_{}.png'.format(color.upper(), piece)