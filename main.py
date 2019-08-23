import game
import pygame

if __name__ == "__main__":
    new_game = game.Game(6, 6, 0)
    new_game.menuStart()
    pygame.quit()
