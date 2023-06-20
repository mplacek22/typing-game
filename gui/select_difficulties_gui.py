import sys
import pygame
from pygame import QUIT, MOUSEBUTTONDOWN
from game_logic.values import Level, BLACK, ORANGE
from game_logic.functions import draw_heading, draw_button
from gui import game_gui_handler


class SelectDifficultiesGUI:
    def __init__(self):
        pygame.init()

        self.WIDTH = 900
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Typing Game")

        self.button_width = 200
        self.button_height = 80
        self.button_x = (self.WIDTH - self.button_width) // 2
        self.button_y = (self.HEIGHT - self.button_height) // 2

        self.difficulty_buttons = []
        for difficulty in reversed(Level):
            difficulty_button_rect = pygame.Rect(self.button_x, self.button_y + 200, self.button_width,
                                                 self.button_height)
            self.difficulty_buttons.append((difficulty_button_rect, difficulty))
            self.button_y -= self.button_height + 20

        self.difficulty_level = None
        self.running = False

    def run(self):
        self.running = True
        self.screen.fill(BLACK)
        self.draw_menu()
        pygame.display.update()

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for button_rect, difficulty in self.difficulty_buttons:
                        if button_rect.collidepoint(event.pos):
                            self.difficulty_level = difficulty
                            self.running = False
                            game_gui_handler.run_game(difficulty)

    def draw_menu(self):
        draw_heading(self.screen, "SELECT DIFFICULTY")

        for button_rect, difficulty in self.difficulty_buttons:
            draw_button(self.screen, difficulty.name.capitalize(), ORANGE, button_rect)
