import sys

import pygame
from pygame import QUIT, MOUSEBUTTONDOWN

from enum_level import Level
from gui_functions import draw_heading, draw_button
from start_game import start_game


class SelectDifficultiesGUI:
    def __init__(self):
        pygame.init()

        # Set up the screen
        self.WIDTH = 900
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Typing Game")

        self.button_width = 200
        self.button_height = 80
        self.button_x = (self.WIDTH - self.button_width) // 2
        self.button_y = (self.HEIGHT - self.button_height) // 2

        # Set up the buttons
        self.difficulty_buttons = []

        difficulty_button_y = self.button_y + 200

        for difficulty in reversed(Level):
            difficulty_button_rect = pygame.Rect(self.button_x, difficulty_button_y, self.button_width,
                                                 self.button_height)
            self.difficulty_buttons.append((difficulty_button_rect, difficulty))
            difficulty_button_y -= self.button_height + 20

        self.difficulty_level = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                for button_rect, difficulty in self.difficulty_buttons:
                    if button_rect.collidepoint(event.pos):
                        self.difficulty_level = difficulty
                        start_game(difficulty)

    def draw(self):
        self.screen.fill((0, 0, 0))
        draw_heading(self.screen, "SELECT DIFFICULTY")

        for button_rect, difficulty in self.difficulty_buttons:
            draw_button(self.screen, difficulty.name.capitalize(), (255, 140, 0), button_rect)

        pygame.display.flip()
