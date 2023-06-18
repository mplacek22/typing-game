import sys
import pygame
from pygame.locals import *

from enum_level import Level
from typing_game import TypingGame


def start_game(difficulty_level):
    game = TypingGame(difficulty_level)
    game.run()


class TypingGameGUI:
    def __init__(self):
        pygame.init()

        # Set up the screen
        self.WIDTH = 900
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Typing Game")
        self.font_title = pygame.font.Font(None, 60)
        self.font_button = pygame.font.Font(None, 40)

        self.button_width = 200
        self.button_height = 80
        self.button_x = (self.WIDTH - self.button_width) // 2
        self.button_y = (self.HEIGHT - self.button_height) // 2

        # Set up the buttons
        self.start_button_rect = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        self.difficulty_buttons = []
        difficulty_button_y = self.button_y + self.button_height

        for difficulty in Level:
            difficulty_button_rect = pygame.Rect(self.button_x, difficulty_button_y, self.button_width,
                                                 self.button_height)
            self.difficulty_buttons.append((difficulty_button_rect, difficulty))
            difficulty_button_y += self.button_height + 20

        self.game_state = "menu"  # Game state: "menu", "difficulty", "game"
        self.difficulty_level = None  # Selected difficulty level

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if self.game_state == "menu":
                        if self.start_button_rect.collidepoint(event.pos):
                            self.game_state = "difficulty"

                    for button_rect, difficulty in self.difficulty_buttons:
                        if button_rect.collidepoint(event.pos):
                            self.difficulty_level = difficulty
                            self.game_state = "game"  # Update game state, but don't start the game immediately
                            start_game(difficulty)

            self.screen.fill((0, 0, 0))

            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "difficulty":
                self.draw_difficulty_selection()

            pygame.display.update()

    def draw_heading(self, typed_text):
        text = self.font_title.render(typed_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.WIDTH // 2, 150))
        self.screen.blit(text, text_rect)

    def draw_button(self, text, color, used_button):
        pygame.draw.rect(self.screen, color, used_button)
        button_text = self.font_button.render(text, True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=used_button.center)
        self.screen.blit(button_text, button_text_rect)

    def draw_menu(self):
        self.draw_heading("TYPING GAME")
        self.draw_button("Start Game", "#00CED1", self.start_button_rect)

    def draw_difficulty_selection(self):
        self.draw_heading("SELECT DIFFICULTY")

        for button_rect, difficulty in self.difficulty_buttons:
            self.draw_button(difficulty.name.capitalize(), (255, 140, 0), button_rect)

        pygame.display.flip()


if __name__ == "__main__":
    game_gui = TypingGameGUI()
    game_gui.run()
