import pygame
import sys
from pieces import *
from constants import *
from board import *

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

board = Board(screen)


def on_start():
    board.reset()
    screen.fill(BG_COLOR)
    board.update_board()


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
