from pygame import QUIT
from enums import Color
from functions import get_text_file_path, read_sentences_from_file, calculate_accuracy
from timer import TimerThread
import sys
import pygame
from random import randint
from guI import game_gui_handler


class TypingGame:
    def __init__(self, difficulty_level):
        pygame.init()

        # Set up the screen
        self.WIDTH = 900
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Typing Game")
        self.font = pygame.font.Font(None, 40)

        # Game variables
        self.game_over = False
        self.text_file = get_text_file_path(difficulty_level)
        self.sentences = read_sentences_from_file(self.text_file)
        self.no_sentences = len(self.sentences)
        self.current_sentence = None
        self.user_text = ""
        self.total_user_input = []
        self.total_expected_input = []

        # Timer variables
        self.game_duration = 10
        self.timer_thread = TimerThread(self.game_duration)

        self.running = False

    def display_accuracy(self):
        # if user did not type any letter accuracy = 0
        if self.user_text == "" and self.total_user_input == []:
            accuracy = 0
        else:
            accuracy = calculate_accuracy(self.total_user_input, self.total_expected_input)
        accuracy_text = self.font.render(f"Accuracy: {accuracy} %", True, Color.WHITE.value)
        self.screen.blit(accuracy_text, (10, 10))

    def display_center(self, text, color, pos):
        text_render = self.font.render(text, True, color)
        text_rect = text_render.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + pos))
        self.screen.blit(text_render, text_rect)

    def display_user_input(self):
        self.display_center(self.user_text, Color.WHITE.value, 50)

    def display_game_over(self):
        self.display_center('GAME OVER!', Color.RED.value, 0)

    def display_current_sentence(self):
        sentence_text = self.font.render(self.current_sentence, True, Color.WHITE.value)
        sentence_rect = sentence_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
        letter_x = sentence_rect.left  # Starting x-coordinate

        for i, letter in enumerate(self.current_sentence):
            letter_color = Color.WHITE.value
            if i < len(self.user_text):
                if self.user_text[i] == letter:
                    letter_color = Color.GREEN.value  # Green for correct letter
                else:
                    letter_color = Color.RED.value  # Red for incorrect letter

            letter_surface = self.font.render(letter, True, letter_color)
            letter_rect = letter_surface.get_rect(topleft=(letter_x, sentence_rect.bottom))

            self.screen.blit(letter_surface, letter_rect)

            letter_width = self.font.size(letter)[0]  # Width of the current letter
            letter_x += letter_width  # Update x-coordinate for the next letter

    def next_sentence(self):
        self.total_user_input += self.user_text
        self.total_expected_input += self.current_sentence
        self.current_sentence = self.sentences[randint(0, self.no_sentences)]
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
        restart_text = self.font.render('RESTART GAME', True, Color.RED.value)
        restart_rect = restart_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 50))
        self.screen.blit(restart_text, restart_rect)
        return restart_rect

    def restart_game(self):
        self.current_sentence = self.sentences[randint(0, self.no_sentences)]
        self.user_text = ""
        self.total_user_input = []
        self.total_expected_input = []
        self.game_over = False
        self.start_timer()

    def display_timer(self):
        timer_text = self.font.render(f"Time: {self.timer_thread.remaining_time} s", True, Color.WHITE.value)
        self.screen.blit(timer_text, (self.WIDTH - 150, 10))

    def start_timer(self):
        if not self.timer_thread.is_alive():
            self.timer_thread = TimerThread(self.game_duration)  # Creating a new TimerThread object
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
                        self.running = False
                        game_gui_handler.run_select_difficulties()

            self.screen.fill(Color.BLACK.value)
            self.display_timer()

            if not self.game_over:
                self.display_current_sentence()
                self.display_user_input()

                if len(self.user_text) == len(self.current_sentence):
                    self.next_sentence()
            else:
                self.display_game_over()

            if not self.timer_thread.is_running:
                self.end_game()

            pygame.display.update()

        pygame.quit()

    def end_game(self):
        self.adjust_last_sentence()
        self.display_accuracy()
        self.display_restart()
        self.game_over = True
