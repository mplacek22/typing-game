from pygame import QUIT
import re
import logging
from enum_level import Level
from timer import TimerThread
import sys
import editdistance
import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def calculate_accuracy(user_input, expected_input):
    if len(expected_input) == 0:
        raise ZeroDivisionError

    if len(user_input) != len(expected_input):
        raise ValueError(f"Input lengths do not match {len(user_input)}, {len(expected_input)}")

    return round((1 - editdistance.eval(user_input, expected_input) / len(expected_input)) * 100, 2)


def read_sentences_from_file(file_path):
    logger = logging.getLogger(__name__)

    try:
        with open(file_path, 'r') as file:
            text = file.read()
            sentence_delimiters = r'[.!?]+[\n\s]*'
            sentences_list = re.split(sentence_delimiters, text)
            sentences_list = [sentence.strip() for sentence in sentences_list if sentence.strip()]
        return sentences_list
    except FileNotFoundError:
        logger.critical(f"File '{file_path}' does not exist.")
        return []

def get_text_file_path(difficulty_level):
    match difficulty_level:
        case Level.EASY:
            return './texts/easy.txt'
        case Level.MEDIUM:
            return './texts/medium.txt'
        case Level.HARD:
            return './texts/hard.txt'
        case _:
            return './texts/sample.txt'


class TypingGame:
    def __init__(self, difficulty_level):
        self.running = False
        pygame.init()

        # Set up the screen
        self.WIDTH = 900
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Typing Game")

        # Game variables
        self.game_over = False
        self.font = pygame.font.Font(None, 40)
        self.text_file = get_text_file_path(difficulty_level)
        self.sentences = read_sentences_from_file(self.text_file)
        self.sentence_iterator = None
        self.current_sentence = None
        self.user_text = ""
        self.total_user_input = []
        self.total_expected_input = []

        # Timer variables
        self.time = 10
        self.timer_thread = TimerThread(self.time)

    def display_accuracy(self):
        # if len(self.total_user_input) != len(self.total_expected_input):
        #     self.total_expected_input. = self.total_expected_input[]
        accuracy = calculate_accuracy(self.total_user_input, self.total_expected_input)
        accuracy_text = self.font.render(f"Accuracy: {accuracy} %", True, WHITE)
        self.screen.blit(accuracy_text, (10, 10))

    def display_user_input(self):
        if not self.game_over:
            text = self.user_text
            color = WHITE
            pos = 50
        else:
            text = 'GAME OVER!'
            color = RED
            pos = 0

        text_render = self.font.render(text, True, color)
        text_rect = text_render.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + pos))
        self.screen.blit(text_render, text_rect)

    def display_current_sentence(self):
        if not self.game_over:  # Display current sentence if the game is not over
            sentence_text = self.font.render(self.current_sentence, True, WHITE)
            sentence_rect = sentence_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
            letter_x = sentence_rect.left  # Starting x-coordinate

            for i, letter in enumerate(self.current_sentence):
                letter_color = WHITE
                if i < len(self.user_text):
                    if self.user_text[i] == letter:
                        letter_color = GREEN  # Green for correct letter
                    else:
                        letter_color = RED  # Red for incorrect letter

                letter_surface = self.font.render(letter, True, letter_color)
                letter_rect = letter_surface.get_rect(topleft=(letter_x, sentence_rect.bottom))

                self.screen.blit(letter_surface, letter_rect)

                letter_width = self.font.size(letter)[0]  # Width of the current letter
                letter_x += letter_width  # Update x-coordinate for the next letter

    def next_sentence(self):
        self.total_user_input += self.user_text
        self.total_expected_input += self.current_sentence
        self.current_sentence = next(self.sentence_iterator)
        self.user_text = ""

    def adjust_last_sentence(self):
        # first sentence wasn't finished
        if len(self.total_expected_input) == 0:
            self.total_expected_input += self.current_sentence
        # last sentence wasn't finished
        if len(self.total_user_input) != len(self.total_expected_input):
            self.total_user_input += self.user_text
            self.total_expected_input = self.total_expected_input[:len(self.user_text)]

    def display_restart(self):
        restart_text = self.font.render('RESTART GAME', True, RED)
        restart_rect = restart_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 50))
        self.screen.blit(restart_text, restart_rect)
        return restart_rect

    def restart_game(self):
        self.game_over = False
        self.sentence_iterator = iter(self.sentences)
        self.current_sentence = next(self.sentence_iterator)
        self.user_text = ""
        self.total_user_input = []
        self.total_expected_input = []

        self.start_timer()

    def display_timer(self):
        timer_text = self.font.render(f"Time: {self.timer_thread.remaining_time} s", True, WHITE)
        self.screen.blit(timer_text, (self.WIDTH - 150, 10))

    def start_timer(self):
        if not self.timer_thread.is_alive():
            self.timer_thread = TimerThread(self.time)  # Creating a new TimerThread object
            self.timer_thread.start()

    def stop_timer(self):
        self.timer_thread.stop()

    def run(self):
        self.running = True
        self.restart_game()

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    self.stop_timer()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if self.timer_thread.is_running:  # Check if the timer is still running
                        self.user_text += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    restart_rect = self.display_restart()
                    if restart_rect.collidepoint(event.pos):
                        self.restart_game()

            self.screen.fill(BLACK)

            self.display_current_sentence()
            self.display_user_input()
            self.display_timer()

            if len(self.user_text) == len(self.current_sentence):
                if self.timer_thread.is_running:  # Check if the timer is still running
                    self.next_sentence()

            self.end_game()

            pygame.display.update()

        pygame.quit()

    def end_game(self):
        if not self.timer_thread.is_running:
            self.adjust_last_sentence()
            self.display_accuracy()
            self.game_over = True
            self.display_restart()


if __name__ == '__main__':
    game = TypingGame(Level.EASY)
    game.run()
