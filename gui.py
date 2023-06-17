import sys
from enum import Enum
import pygame
from pygame.locals import *


class Level(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2


class TypingGameGUI:
    def __init__(self):
        pygame.init()
        self.WIDTH = 900
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Typing Game")
        self.font_title = pygame.font.Font(None, 60)
        self.font_button = pygame.font.Font(None, 40)

        button_width = 200
        button_height = 80
        button_x = (self.WIDTH - button_width) // 2
        button_y = (self.HEIGHT - button_height) // 2
        self.start_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        self.difficulty_buttons = []
        difficulty_button_y = button_y + button_height + 50
        for i, difficulty in enumerate(Level):
            difficulty_button_rect = pygame.Rect(button_x, difficulty_button_y, button_width, button_height)
            self.difficulty_buttons.append(difficulty_button_rect)
            difficulty_button_y += button_height + 20

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

                    elif self.game_state == "difficulty":
                        for i, button in enumerate(self.difficulty_buttons):
                            if button.collidepoint(event.pos):
                                self.difficulty_level = Level(i)
                                self.game_state = "game"  # Dodane przypisanie stanu "game"
                                self.start_game()

            self.screen.fill((0, 0, 0))

            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "difficulty":
                self.draw_difficulty_selection()
            elif self.game_state == "game":
                self.start_game()

            pygame.display.update()

    def draw_menu(self):
        # Draw title
        title_text = self.font_title.render("TYPING GAME", True, (255, 255, 255))
        title_text_rect = title_text.get_rect(center=(self.WIDTH // 2, 50))
        self.screen.blit(title_text, title_text_rect)

        pygame.draw.rect(self.screen, ("#00CED1"), self.start_button_rect)
        start_text = self.font_button.render("Start Game", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(start_text, start_text_rect)

    def draw_difficulty_selection(self):
        # Draw title
        title_text = self.font_title.render("SELECT DIFFICULTY", True, (255, 255, 255))
        title_text_rect = title_text.get_rect(center=(self.WIDTH // 2, 150))
        self.screen.blit(title_text, title_text_rect)

        button_width = 200
        button_height = 80
        button_x = (self.WIDTH - button_width) // 2
        total_height = len(self.difficulty_buttons) * (button_height + 20)
        button_y = (self.HEIGHT - total_height) // 2 + 100

        for i, button in enumerate(self.difficulty_buttons):
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, (255, 140, 0), button_rect)
            difficulty_text = self.font_button.render([level.name.capitalize() for level in Level][i], True, (255, 255, 255))
            difficulty_text_rect = difficulty_text.get_rect(center=button_rect.center)
            self.screen.blit(difficulty_text, difficulty_text_rect)

            button_y += button_height + 20

    def start_game(self):
        from typing_game import TypingGame
        game = TypingGame(self.difficulty_level)
        game.run()


if __name__ == "__main__":
    game_gui = TypingGameGUI()
    game_gui.run()