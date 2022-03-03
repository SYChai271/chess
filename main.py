import pygame
import sys
from constants import *
from board import *

pygame.init()
pygame.font.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

board = Board(screen)


def on_start():
    board.reset()
    screen.fill(BG_COLOR)
    board.update_board()


def game_over(color):
    game_over_message = 'Checkmate! ' + color + ' wins!'
    font = pygame.font.SysFont('Arial', 30, bold=True)
    text = font.render(game_over_message, True, (255, 255, 255)
                       if color == 'White' else (0, 0, 0))
    screen.blit(text, (WIDTH/2 - text.get_width() /
                2, HEIGHT/2 - text.get_height()/2))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    main()


def main():
    on_start()
    _running = True
    while _running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.handle_click()
                if board.game_over:
                    game_over(board.get_winner())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    _running = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    on_start()
                if event.key == pygame.K_u:
                    board.take_back()

        pygame.display.flip()


if __name__ == "__main__":
    main()
