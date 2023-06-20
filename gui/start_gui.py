import sys
import pygame
from pygame import QUIT, MOUSEBUTTONDOWN
from game_logic.functions import draw_heading, draw_button
from game_logic.values import BLUE, BLACK
from gui import game_gui_handler


class StartGUI:
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

        self.start_button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        self.running = False

    def run(self):
        self.running = True
        self.screen.fill(BLACK)
        self.draw_start()
        pygame.display.update()

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if self.start_button_rect.collidepoint(event.pos):
                        self.running = False
                        game_gui_handler.run_select_difficulties()

    def draw_start(self):
        draw_heading(self.screen, "TYPING GAME")
        draw_button(self.screen, "Start Game", BLUE, self.start_button_rect)

